# **SISTEM PERANGKINGAN BEASISWA METODE WEIGHTED PRODUCT**

## 1. Deskripsi Umum

### EN
This application is a **web-based system** designed to perform **ranking of scholarship candidates** using the **Weighted Product (WP) method**.
The system is developed using the **Flask (Python)** framework, supporting **CSV data upload**, **dynamic adjustment of criteria weights**, and **customizable eligibility threshold**.


### ID
Aplikasi ini merupakan **sistem berbasis web** yang digunakan untuk melakukan **perangkingan calon penerima beasiswa** menggunakan **metode Weighted Product (WP)**.
Sistem dikembangkan dengan framework **Flask (Python)**, mendukung **upload data CSV**, **penyesuaian bobot kriteria secara dinamis**, serta **penentuan ambang kelayakan (threshold)**.

---

## 2. Tujuan Sistem

Tujuan utama sistem ini adalah membantu proses **seleksi dan perangkingan calon penerima beasiswa** secara objektif berdasarkan kriteria-kriteria tertentu, menggunakan perhitungan matematis yang konsisten (Weighted Product Method).

---

## 3. Metodologi Weighted Product

Metode **Weighted Product (WP)** merupakan salah satu metode **Multi-Criteria Decision Making (MCDM)** yang mengalikan setiap nilai kriteria yang telah dinormalisasi dengan pangkat bobot kriterianya.

Rumus utama WP:

<img width="143" height="107" alt="image" src="https://github.com/user-attachments/assets/bf2f2bf3-469d-405a-8eac-7d358a699616" />


Dimana:

<img width="388" height="111" alt="image" src="https://github.com/user-attachments/assets/8d29acde-279c-4782-9d12-52cc63ea0890" />

Kemudian hasil ( S_i ) dinormalisasi menjadi ( V_i ):

<img width="154" height="76" alt="image" src="https://github.com/user-attachments/assets/c7b87432-214b-4072-bffe-9a32b48e085c" />


---

## 4. Arsitektur Sistem

### 4.1 Komponen Utama

| Komponen                 | Fungsi                                           |
| ------------------------ | ------------------------------------------------ |
| `main.py`                | Entry point utama Flask App                      |
| `templates/index.html`   | Halaman utama (form upload dan pengaturan bobot) |
| `templates/results.html` | Halaman hasil perangkingan                       |
| `uploads/`               | Folder penyimpanan file CSV yang diunggah        |
| `hasil_wp_beasiswa.csv`  | File hasil perhitungan akhir yang bisa diunduh   |

### 4.2 Struktur Folder

```
wheighted_product_ui/
│
├── main.py
├── uploads/
│    └── (file CSV upload)
├── templates/
│    ├── index.html
│    └── results.html
└── hasil_wp_beasiswa.csv
```

---

## 5. Konfigurasi Sistem

| Parameter            | Nilai Default             | Deskripsi                                 |
| -------------------- | ------------------------- | ----------------------------------------- |
| `UPLOAD_FOLDER`      | `"uploads"`               | Folder penyimpanan file CSV yang diunggah |
| `RESULT_FILE`        | `"hasil_wp_beasiswa.csv"` | Nama file hasil yang akan diekspor        |
| `ALLOWED_EXTENSIONS` | `{ "csv" }`               | Format file yang diizinkan                |
| `SECRET_KEY`         | `"secret-key-123"`        | Kunci enkripsi session Flask              |
| `threshold`          | `0.3`                     | Nilai ambang batas kelayakan (0–1)        |

---

## 6. Kriteria dan Bobot Default

| Kriteria        | Tipe    | Bobot Awal | Keterangan                  |
| --------------- | ------- | ---------- | --------------------------- |
| Gaji_Ortu       | Cost    | 4          | Semakin kecil semakin baik  |
| Cicilan_Ortu    | Cost    | 3          | Semakin kecil semakin baik  |
| Jumlah_Saudara  | Benefit | 2          | Semakin banyak semakin baik |
| Nilai_Rata_rata | Benefit | 4          | Semakin tinggi semakin baik |

Bobot akan **dinormalisasi otomatis** agar totalnya = 1.

---

## 7. Alur Proses Sistem

### 7.1 Alur Utama

1. **User mengakses halaman utama (`/`)**
   Menampilkan form upload file CSV dan form pengisian bobot kriteria.
2. **User mengunggah file CSV atau menggunakan default `data_beasiswa.csv`**
3. **Sistem membaca dan memvalidasi data**

   * Pastikan kolom sesuai kriteria.
   * Konversi ke tipe numerik.
4. **Proses perhitungan Weighted Product**

   * Normalisasi bobot.
   * Penanganan nilai nol (ε = 1e-6).
   * Perhitungan nilai S dan V.
   * Normalisasi nilai V ke rentang 0–1.
5. **Penentuan status kelayakan**

   * Jika `V_Normalized ≥ threshold` → “Layak”
   * Jika `V_Normalized < threshold` → “Tidak Layak”
6. **Perangkingan**

   * Berdasarkan `V_Normalized` tertinggi.
7. **Tampilkan hasil di halaman `results.html`**

   * Dapat diunduh dalam format CSV (`/download`).

---

## 8. Penjelasan Fungsi Utama

### 8.1 `run_weighted_product(df, kriteria, bobot_awal, threshold)`

Melakukan proses utama perhitungan Weighted Product dan menghasilkan DataFrame dengan kolom tambahan:

| Kolom          | Deskripsi                                    |
| -------------- | -------------------------------------------- |
| `S`            | Hasil perkalian nilai ter-bobot              |
| `V`            | Nilai preferensi alternatif                  |
| `V_Normalized` | Nilai preferensi dalam skala 0–1             |
| `Kelayakan`    | Status hasil evaluasi (Layak/Tidak Layak)    |
| `Ranking`      | Urutan prioritas berdasarkan nilai tertinggi |

---

## 9. Dependensi dan Instalasi

### 9.1 Instalasi Lingkungan

Gunakan virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 9.2 Instalasi Dependensi

```bash
pip install flask pandas numpy openpyxl
```

---

## 10. Cara Menjalankan Aplikasi

1. Pastikan file `main.py` dan folder `templates/` sudah ada.

2. Jalankan aplikasi dengan:

   ```bash
   python main.py
   ```

3. Akses melalui browser:

   ```
   http://127.0.0.1:5000
   ```

4. Unggah file CSV dengan struktur kolom seperti:

   ```
   Nama,Gaji_Ortu,Cicilan_Ortu,Jumlah_Saudara,Nilai_Rata_rata
   Andi,1500000,1000000,3,85
   Budi,4000000,2500000,2,80
   ```

---

## 11. Output Sistem

Setelah perhitungan selesai, sistem menghasilkan file `hasil_wp_beasiswa.csv` dengan kolom:

| Nama | Gaji_Ortu | Cicilan_Ortu | Jumlah_Saudara | Nilai_Rata_rata | S | V | V_Normalized | Kelayakan | Ranking |

Data ini juga ditampilkan di halaman hasil (HTML table) dan bisa diunduh dengan tombol **Download Hasil**.

---

## 12. Penanganan Error dan Validasi

| Jenis Error                              | Penyebab                                                      | Solusi                                          |
| ---------------------------------------- | ------------------------------------------------------------- | ----------------------------------------------- |
| `ValueError: Kolom tidak ditemukan`      | Kolom CSV tidak sesuai dengan kriteria yang didefinisikan     | Periksa header CSV                              |
| `TemplateNotFound: results.html`         | File template belum dibuat                                    | Tambahkan `results.html` ke folder `templates/` |
| `FileNotFoundError`                      | Tidak ada file upload dan `data_beasiswa.csv` tidak ditemukan | Upload file CSV baru                            |
| `TypeError: unsupported operand type(s)` | Nilai string di kolom numerik                                 | Sistem otomatis konversi ke numerik dan isi 0   |

---

## 13. Rencana Pengembangan (Opsional)

1. **Integrasi Database (MySQL/PostgreSQL)** untuk penyimpanan hasil.
2. **Visualisasi Grafik (Plotly/Chart.js)** untuk nilai preferensi.
3. **Autentikasi User (Flask-Login)** untuk admin dan operator.
4. **Fitur Export PDF** untuk laporan resmi hasil seleksi.
5. **Penyimpanan History Perhitungan**.

---

## 14. Referensi

* Kusumadewi, S., Hartati, S., Harjoko, A., & Wardoyo, R. (2006). *Fuzzy Multi-Attribute Decision Making (Fuzzy MADM)*. Yogyakarta: Graha Ilmu.
* Turban, E., Aronson, J.E., & Liang, T.-P. (2005). *Decision Support Systems and Intelligent Systems*.
* Dokumentasi Flask: [https://flask.palletsprojects.com](https://flask.palletsprojects.com)
