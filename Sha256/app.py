from flask import Flask, render_template, request, redirect, url_for, session
import hashlib
from Database.database import db_conn, init_db
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret_key_ganti_ini"


# =========================
# HASH FUNCTION (SHA-256)
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


# =========================
# ROUTES
# =========================
@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    hashed = hash_password(password)

    conn = db_conn()
    c = conn.cursor()
    c.execute(
        "SELECT * FROM users WHERE username=? AND password_hash=?",
        (username, hashed)
    )
    user = c.fetchone()
    conn.close()

    if user:
        session["user"] = {
            "id": user["id"],
            "username": user["username"],
            "nama": user["nama"]
        }
        return redirect(url_for("dashboard"))
    else:
        return render_template("login.html", error="Username atau password salah!")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        nama = request.form["nama"]
        password = request.form["password"]
        confirm = request.form["confirm"]

        if password != confirm:
            return render_template("register.html", error="Password tidak cocok")

        hashed = hash_password(password)

        conn = db_conn()
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO users (username, nama, password_hash) VALUES (?, ?, ?)",
                (username, nama, hashed)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("index"))
        except:
            conn.close()
            return render_template("register.html", error="Username sudah terdaftar")

    return render_template("register.html")


@app.route("/forgot", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        username = request.form["username"]

        conn = db_conn()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        conn.close()

        if user:
            session["reset_user"] = username
            return redirect(url_for("reset_password"))
        else:
            return render_template("forgot.html", error="Username tidak ditemukan")

    return render_template("forgot.html")


@app.route("/reset", methods=["GET", "POST"])
def reset_password():
    if "reset_user" not in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        password = request.form["password"]
        confirm = request.form["confirm"]

        if password != confirm:
            return render_template("reset.html", error="Password tidak cocok")

        hashed = hash_password(password)

        conn = db_conn()
        c = conn.cursor()
        c.execute(
            "UPDATE users SET password_hash=? WHERE username=?",
            (hashed, session["reset_user"])
        )
        conn.commit()
        conn.close()

        session.pop("reset_user")
        return redirect(url_for("index"))

    return render_template("reset.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("index"))
    return render_template("dashboard.html", user=session["user"])

@app.route("/transaksi", methods=["POST"])
def transaksi():
    if "user" not in session:
        return redirect(url_for("index"))

    koin = request.form["koin"]
    jumlah = int(request.form["jumlah"])

    btc_diterima = jumlah * 0.000005162

    raw_data = f"{session['user']['username']}{koin}{btc_diterima}{datetime.now()}"
    hash_transaksi = hashlib.sha256(raw_data.encode()).hexdigest()

    return render_template(
        "transaksi_berhasil.html",
        koin=koin,
        btc=btc_diterima,
        hash=hash_transaksi
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# =========================
# RUN
# =========================
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
