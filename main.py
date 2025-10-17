import os
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename

# Konfigurasi
UPLOAD_FOLDER = "uploads"
RESULT_FILE = "hasil_wp_beasiswa.csv"
ALLOWED_EXTENSIONS = {"csv"}

app = Flask(__name__)
app.secret_key = "secret-key-123"   # ganti untuk produksi
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def run_weighted_product(df,
                         kriteria = {"Gaji_Ortu":"cost","Cicilan_Ortu":"cost","Jumlah_Saudara":"benefit","Nilai_Rata_rata":"benefit"},
                         bobot_awal = {"Gaji_Ortu":4,"Cicilan_Ortu":3,"Jumlah_Saudara":2,"Nilai_Rata_rata":4},
                         threshold = 0.3):
    # Pastikan kolom numerik
    for col in kriteria.keys():
        if col not in df.columns:
            raise ValueError(f"Kolom '{col}' tidak ditemukan di CSV.")
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Normalisasi bobot
    total_bobot = sum(bobot_awal.values())
    bobot_norm = {k: (v / total_bobot) for k, v in bobot_awal.items()}

    # Hitung S
    epsilon = 1e-6
    S = []
    for _, row in df.iterrows():
        nilai = 1.0
        for k in kriteria.keys():
            x = row[k]
            if x == 0:
                x = epsilon
            if kriteria[k] == "benefit":
                nilai *= x ** bobot_norm[k]
            else:  # cost
                nilai *= x ** (-bobot_norm[k])
        S.append(nilai)
    df["S"] = S

    # V dan normalisasi 0-1
    df["V"] = df["S"] / df["S"].sum()
    v_min, v_max = df["V"].min(), df["V"].max()
    if v_max - v_min == 0:
        df["V_Normalized"] = 0.0
    else:
        df["V_Normalized"] = (df["V"] - v_min) / (v_max - v_min)

    # Kelayakan dan Ranking
    df["Kelayakan"] = df["V_Normalized"].apply(lambda x: "Layak" if x >= threshold else "Tidak Layak")
    df = df.sort_values(by="V_Normalized", ascending=False).reset_index(drop=True)
    df["Ranking"] = df.index + 1

    return df

@app.route("/", methods=["GET", "POST"])
def index():
    # Bobot default (sama seperti yang kamu pakai)
    default_bobot = {"Gaji_Ortu":4,"Cicilan_Ortu":3,"Jumlah_Saudara":2,"Nilai_Rata_rata":4}
    default_threshold = 0.3

    if request.method == "POST":
        # Ambil bobot dari form
        try:
            bobot_awal = {
                "Gaji_Ortu": float(request.form.get("b_gaji", default_bobot["Gaji_Ortu"])),
                "Cicilan_Ortu": float(request.form.get("b_cicilan", default_bobot["Cicilan_Ortu"])),
                "Jumlah_Saudara": float(request.form.get("b_saudara", default_bobot["Jumlah_Saudara"])),
                "Nilai_Rata_rata": float(request.form.get("b_nilai", default_bobot["Nilai_Rata_rata"]))
            }
        except ValueError:
            flash("Bobot harus angka.", "danger")
            return redirect(url_for("index"))

        # Threshold
        try:
            threshold = float(request.form.get("threshold", default_threshold))
        except ValueError:
            threshold = default_threshold

        # Gunakan file upload jika ada, kalau tidak gunakan data_beasiswa.csv di root
        file = request.files.get("csv_file", None)
        if file and file.filename != "":
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)
                df = pd.read_csv(filepath)
            else:
                flash("Format file tidak didukung. Gunakan CSV.", "danger")
                return redirect(url_for("index"))
        else:
            # Coba baca default data_beasiswa.csv
            default_path = "data_beasiswa.csv"
            if not os.path.exists(default_path):
                flash("Tidak ada file CSV yang di-upload dan 'data_beasiswa.csv' tidak ditemukan di folder aplikasi.", "danger")
                return redirect(url_for("index"))
            df = pd.read_csv(default_path)

        # Kriteria tetap (kamu bisa ubah jika butuh)
        kriteria = {"Gaji_Ortu":"cost","Cicilan_Ortu":"cost","Jumlah_Saudara":"benefit","Nilai_Rata_rata":"benefit"}

        try:
            hasil = run_weighted_product(df, kriteria=kriteria, bobot_awal=bobot_awal, threshold=threshold)
        except Exception as e:
            flash(f"Terjadi kesalahan saat memproses data: {e}", "danger")
            return redirect(url_for("index"))

        # Simpan hasil ke CSV untuk didownload
        hasil.to_csv(RESULT_FILE, index=False)

        # Kirim ke template hasil
        return render_template("results.html", tables=[hasil.to_html(classes="table table-striped table-sm", index=False, justify="center")], result_count=len(hasil), threshold=threshold)

    # GET
    return render_template("index.html", default_bobot=default_bobot, default_threshold=default_threshold)

@app.route("/download")
def download():
    if not os.path.exists(RESULT_FILE):
        flash("File hasil belum tersedia. Jalankan proses dulu.", "warning")
        return redirect(url_for("index"))
    return send_file(RESULT_FILE, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
