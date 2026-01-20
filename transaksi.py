from flask import Flask, render_template, request
import hashlib
from datetime import datetime

app = Flask(__name__)

@app.route("/transaksi", methods=["POST"])
def transaksi():
    koin = request.form["koin"]
    jumlah = request.form["jumlah"]

    # simulasi hasil BTC
    btc_diterima = float(jumlah) * 0.000005162

    # data transaksi
    raw_data = f"{koin}{btc_diterima}{datetime.now()}"
    hash_transaksi = hashlib.sha256(raw_data.encode()).hexdigest()

    return render_template(
        "transaksi_berhasil.html",
        koin=koin,
        btc=btc_diterima,
        hash=hash_transaksi
    )

if __name__ == "__main__":
    app.run(debug=True)
