from flask import Flask, render_template, request, redirect, url_for, session
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret-key-dashboard"  # wajib untuk session


# ======================
# DASHBOARD
# ======================
@app.route("/")
def dashboard():
    # simulasi user login
    user = {
        "nama": "Awa"
    }
    return render_template("dashboard.html", user=user)


# ======================
# TRANSAKSI
# ======================
@app.route("/transaksi", methods=["POST"])
def transaksi():
    koin = request.form.get("koin")
    jumlah = float(request.form.get("jumlah"))

    # simulasi konversi ke BTC
    btc_diterima = jumlah * 0.000005162

    # hash transaksi
    raw_data = f"{koin}{btc_diterima}{datetime.now()}"
    hash_transaksi = hashlib.sha256(raw_data.encode()).hexdigest()

    return render_template(
        "transaksi_berhasil.html",
        koin=koin,
        btc=btc_diterima,
        hash=hash_transaksi
    )


# ======================
# LOGOUT
# ======================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
