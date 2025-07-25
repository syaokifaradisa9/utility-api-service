# Utility REST API Service

![version](https://img.shields.io/badge/version-1.3.0-blue)

**Utility REST API Service** adalah aplikasi backend yang dibuat menggunakan bahasa pemrograman **Python** dengan framework **FastAPI**. Aplikasi ini dirancang untuk menyediakan berbagai utilitas dan tools melalui antarmuka REST API, termasuk fitur konversi file PDF ke gambar atau teks, penggantian template teks dengan gambar di PDF, tandatangan dokumen PDF, pemisahan/split dokumen PDF, autentikasi menggunakan API key, dan pembatasan request (rate limiting).

Aplikasi ini cocok digunakan sebagai layanan mandiri di VPS dan bisa diintegrasikan ke berbagai frontend atau sistem lainnya melalui endpoint HTTP.

## 🚀 Fitur

- **Konversi PDF ke Gambar**: Mengubah file PDF menjadi satu gambar PNG yang digabungkan secara vertikal
- **Konversi PDF ke Teks**: Ekstraksi teks dari file PDF dengan dukungan untuk dokumen yang dapat dicari
- **Tandatangan Dokumen PDF**: Menandatangani dokumen PDF dengan menyisipkan gambar tanda tangan pada template ${sign}
- **Split/Pemisahan PDF**: Memisahkan dokumen PDF menjadi beberapa bagian berdasarkan rentang halaman tertentu
- **Hapus Halaman Kosong**: Menghapus halaman yang tidak memiliki konten isi (body) dari sebuah PDF.
- **Konversi DOCX ke PDF**: Mengubah file DOCX menjadi dokumen PDF
- **Generate Barcode**: Membuat gambar barcode dari data yang diberikan
- **API Key Authentication**: Keamanan endpoint dengan API Key
- **Rate Limiting**: Pembatasan jumlah request per waktu tertentu

## 🛠️ Teknologi

- [FastAPI](https://fastapi.tiangolo.com/) - Framework API modern dengan performa tinggi
- [PyMuPDF](https://pymupdf.readthedocs.io/) - Library untuk manipulasi file PDF
- [PIL/Pillow](https://pillow.readthedocs.io/) - Library untuk pemrosesan gambar
- [SlowAPI](https://github.com/laurentS/slowapi) - Rate limiting middleware untuk FastAPI
- [Python-dotenv](https://github.com/theskumar/python-dotenv) - Manajemen konfigurasi environment
- [python-barcode](https://python-barcode.readthedocs.io/en/stable/) - Library untuk pembuatan barcode

## 📋 Prasyarat

- Python 3.8 atau lebih baru
- pip (Python package manager)
- Dependensi sistem untuk PyMuPDF (fitz)
- LibreOffice (for cross-platform DOCX to PDF conversion)

## 🔧 Instalasi

1. Clone repository ini:

```bash
git clone https://github.com/syaokifaradisa9/utility-api-service.git
cd utility-api-service
```

2. Buat dan aktifkan virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Untuk Linux/Mac
# atau
.venv\Scripts\activate     # Untuk Windows
```

3. Install dependensi:

```bash
pip install -r requirements.txt
```

4. Salin file .env.example menjadi .env dan sesuaikan konfigurasi:

```bash
cp .env.example .env
```

5. Edit file .env dan atur API_KEY dengan nilai yang aman

## 🚀 Menjalankan Aplikasi

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Aplikasi akan berjalan di http://localhost:8000, silahkan ganti port 8000 dengan port yang diinginkan.

## 📚 Penggunaan API

### Endpoint

#### Info & Health

- `GET /v1/about` - Informasi umum tentang layanan
- `GET /v1/health` - Health check untuk memastikan layanan berjalan

#### Konversi PDF

- `POST /v1/pdf/convert-to-image` - Konversi PDF ke gambar tunggal (memerlukan API key)
- `POST /v1/pdf/convert-to-text` - Ekstraksi teks dari PDF (memerlukan API key)

#### Manipulasi PDF

- `POST /v1/pdf/sign` - Tandatangan dokumen PDF dengan menyisipkan gambar pada template ${sign} (memerlukan API key)
- `POST /v1/pdf/remove-empty-pages` - Menghapus halaman kosong dari PDF (memerlukan API key)

#### Split/Pemisahan PDF

- `POST /v1/pdf/split-by-range` - Memisahkan PDF berdasarkan rentang halaman tertentu (memerlukan API key)

#### Konversi DOCX

- `POST /v1/docx/convert-to-pdf` - Konversi DOCX ke PDF (memerlukan API key)

#### Barcode

- `POST /v1/barcode/generate-barcode` - Membuat gambar barcode dari data yang diberikan, dengan opsi menyertakan logo di tengah (memerlukan API key)

## ⚙️ Konfigurasi

Konfigurasi dilakukan melalui file .env:

| Variabel   | Deskripsi                   | Default    |
| ---------- | --------------------------- | ---------- |
| API_KEY    | Kunci API untuk autentikasi | (required) |
| ENV_PATH   | Path ke file .env           | .env       |
| RATE_LIMIT | Batasan rate request        | 20/minute  |

## 🛡️ Keamanan

Semua endpoint API (kecuali `/v1/about`) dilindungi dengan API key authentication. Pastikan untuk menyimpan API key Anda dengan aman dan tidak membagikannya kepada pihak yang tidak berwenang.

API key harus disertakan pada setiap request dalam header `X-API-Key`.

## 📝 Kontribusi

Kontribusi dan saran selalu diterima. Silakan buat issue atau pull request untuk meningkatkan layanan ini.

## 🛎️ Support

Jika Anda menemukan masalah atau memiliki pertanyaan, silakan buat issue baru di GitHub repository ini.

## 📄 Lisensi

Hak Cipta © 2025

Dikembangkan oleh Muhammad Syaoki Faradisa (syaokifaradisa09)

Semua hak dilindungi. Kode ini dilindungi hak cipta dan tidak boleh digunakan, didistribusikan, atau direproduksi tanpa izin dari pemilik.

## 🔍 Catatan Teknis

- Layanan ini menggunakan PyMuPDF (fitz) untuk ekstraksi dan manipulasi PDF
- Untuk PDF yang tidak memiliki teks yang dapat dicari, layanan ini dapat mendeteksi hal tersebut dan memberikan pesan error yang sesuai
- Rate limiting diimplementasikan dengan SlowAPI dan menggunakan alamat IP klien sebagai kunci untuk pembatasan
- Konversi PDF ke teks dan fitur tandatangan PDF hanya bisa digunakan apabila PDF tersebut bukan dari hasil scanner
- Fitur split PDF mendukung metode pemisahan dengan rentang halaman tertentu
- Konversi DOCX ke PDF akan menggunakan Microsoft Word jika tersedia di Windows untuk kualitas terbaik, jika tidak, akan menggunakan LibreOffice.

## ⚠️ Catatan Penting

Mohon tidak menjual atau mencari keuntungan secara pribadi dengan repository ini. Jika anda melanggar silahkan tanggungjawab sendiri di akhirat kelak. Terimakasih
