# 🦠 COVID-19 X-Ray AI Diagnoser

Sistem kecerdasan buatan berbasis **MobileNetV2 Transfer Learning** untuk mendeteksi COVID-19 dari citra X-Ray paru-paru secara *real-time*.

> **Kelompok 4 — Pengolahan Citra Digital**

| Nama | NIM |
|------|-----|
| Najihatul Wilda | 2404130031 |
| Pinkan Sofia Zahra | 2404130037 |
| Najwa Zakia | 2404130040 |
| Najwa Putri Aulia | 2404130152 |

---

## 📋 Prasyarat (Requirement)

Pastikan perangkat Anda sudah terinstal:

1. **Python** versi 3.8 atau lebih baru *(Jika belum ada, silakan unduh dan instal dari situs resmi [python.org](https://www.python.org/downloads/))*
2. **pip** (package manager Python)
3. Library yang dibutuhkan:
   - `Flask`
   - `TensorFlow`
   - `OpenCV (cv2)`
   - `NumPy`

### Instalasi Library

Buka terminal/command prompt, lalu jalankan:

```bash
pip install flask tensorflow opencv-python numpy
```

---

## 🚀 Langkah-Langkah Menjalankan Aplikasi

### Langkah 1 — Clone Repository GitHub

Buka **Command Prompt** atau **Terminal**, lalu jalankan perintah berikut untuk mengunduh proyek:

```bash
git clone https://github.com/pinkansoza/PendeteksiCovid-19.git
```

### Langkah 2 — Masuk ke Folder Proyek

Arahkan terminal ke folder proyek yang baru saja diunduh:

```bash
cd PendeteksiCovid-19
```

### Langkah 3 — Jalankan Server

Ketik perintah berikut untuk memulai server:

```bash
python app.py
```

Jika berhasil, akan muncul pesan:

```
Membuka server web di http://127.0.0.1:5000
```

### Langkah 4 — Buka Aplikasi di Browser

Buka browser (Chrome, Edge, Firefox, dll.), lalu akses alamat:

```
http://127.0.0.1:5000
```

Halaman utama aplikasi akan tampil.

---

## 🔍 Langkah-Langkah Menggunakan Aplikasi

### Langkah 1 — Siapkan Gambar X-Ray

Siapkan file gambar rontgen dada (Chest X-Ray) dalam format **JPG**, **JPEG**, atau **PNG**.

### Langkah 2 — Unggah Gambar

Ada dua cara untuk mengunggah gambar:

- **Cara 1 (Klik):** Klik area unggah bertuliskan *"Unggah Citra X-Ray"*, lalu pilih file gambar dari komputer Anda.
- **Cara 2 (Drag & Drop):** Tarik file gambar dari folder, lalu lepaskan ke area unggah.

Setelah berhasil, preview gambar akan ditampilkan di layar.

### Langkah 3 — Mulai Analisis

Klik tombol **"🔬 Mulai Analisis Citra"** untuk memulai proses deteksi. Tunggu beberapa saat hingga proses selesai (animasi *scanning* akan berjalan selama proses berlangsung).

### Langkah 4 — Lihat Hasil Diagnosis

Setelah proses selesai, hasil diagnosis akan tampil berupa:

| Komponen | Keterangan |
|----------|------------|
| **Status** | Menampilkan apakah terdeteksi *COVID-19* atau *Normal* |
| **Tingkat Keyakinan AI** | Persentase keyakinan model AI terhadap hasil prediksi |
| **Interpretasi Medis** | Penjelasan detail dari hasil analisis beserta saran tindak lanjut |

#### Contoh Hasil:

- ✅ **Normal** — Citra rontgen tidak menunjukkan pola infeksi COVID-19. Paru-paru terdeteksi normal.
- ⚠️ **Covid19 Detected** — Model AI mendeteksi adanya pola abnormalitas yang konsisten dengan infeksi COVID-19. Segera konsultasikan dengan tenaga medis.

### Langkah 5 — Analisis Gambar Lain (Opsional)

Untuk menganalisis gambar lain:

1. Klik tombol **✕** (silang) pada pojok kanan atas preview gambar untuk menghapus gambar saat ini.
2. Unggah gambar baru dan ulangi proses dari **Langkah 2**.

---

## ⚠️ Catatan Penting

- Aplikasi ini **bukan pengganti diagnosis medis profesional**. Hasil analisis hanya bersifat sebagai alat bantu skrining awal.
- Gambar yang diunggah akan **dihapus otomatis** dari server setelah proses prediksi selesai demi menjaga privasi.
- Model AI menggunakan arsitektur **MobileNetV2** yang telah dilatih menggunakan dataset citra X-Ray paru-paru.
- Skor prediksi mendekati **1** mengindikasikan kemungkinan infeksi, sedangkan mendekati **0** mengindikasikan kondisi normal.

---

## 📁 Struktur Proyek

```
SMART-CT-SCAN_BASED-COVID19_VIRUS_DETECTOR/
├── app.py                      # Server Flask utama
├── covid19_ai_diagnoser.py     # Modul inferensi AI
├── covid_mobilenet_model.h5    # Model MobileNetV2 yang sudah dilatih
├── train_covid_model.ipynb     # Notebook untuk melatih model
├── templates/
│   └── index.html              # Halaman antarmuka web
├── static/
│   └── css/
│       └── style.css           # Stylesheet
│   └── js/
│       └── script.js           # Script (pemrosesan JS)
└── README.md                   # Dokumentasi ini
```