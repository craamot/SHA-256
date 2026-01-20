from flask import Flask, render_template, request, redirect, url_for, flash
import hashlib
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret_key_anda_disini'   # ganti dengan sesuatu yg aman

# Inisialisasi DB jika belum ada
def init_db():
    conn = sqlite3.connect('cryptodb.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        password TEXT,
        tempat_lahir TEXT,
        tanggal_lahir TEXT,
        alamat TEXT,
        no_telpon TEXT,
        email TEXT,
        no_rekening TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        alamat = request.form['alamat']
        no_telpon = request.form['no_telpon']
        no_rekening = request.form['no_rekening']

        if password != password_confirm:
            flash("Password dan konfirmasi password tidak cocok!", "error")
            return redirect(url_for('register'))

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect('cryptodb.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (nama, password, tempat_lahir, tanggal_lahir, alamat, no_telpon, email, no_rekening) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (nama, hashed_password, tempat_lahir, tanggal_lahir, alamat, no_telpon, email, no_rekening))
            conn.commit()
            conn.close()
            flash("Registrasi berhasil! Silakan login.", "success")
            return redirect(url_for("register"))
        except Exception as e:
            conn.close()
            flash(f"Terjadi kesalahan: {e}", "error")

    return render_template('register.html')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
