# Utility REST API Service

![version](https://img.shields.io/badge/version-1.0.0-blue)

**Utility REST API Service** adalah aplikasi backend yang dibuat menggunakan bahasa pemrograman **Python** dengan framework **FastAPI**. Aplikasi ini dirancang untuk menyediakan berbagai utilitas dan tools melalui antarmuka REST API, termasuk fitur konversi file PDF ke gambar, autentikasi menggunakan API key, dan pembatasan request (rate limiting).

Aplikasi ini cocok digunakan sebagai layanan mandiri di VPS dan bisa diintegrasikan ke berbagai frontend atau sistem lainnya melalui endpoint HTTP.

## 🚀 Fitur

- **Konversi PDF ke Gambar**: Mengubah file PDF menjadi satu gambar PNG yang digabungkan secara vertikal
- **API Key Authentication**: Keamanan endpoint dengan API Key
- **Rate Limiting**: Pembatasan jumlah request per waktu tertentu

## 🛠️ Teknologi

- [FastAPI](https://fastapi.tiangolo.com/) - Framework API modern dengan performa tinggi
- [PyMuPDF](https://pymupdf.readthedocs.io/) - Library untuk manipulasi file PDF
- [PIL/Pillow](https://pillow.readthedocs.io/) - Library untuk pemrosesan gambar
- [SlowAPI](https://github.com/laurentS/slowapi) - Rate limiting middleware untuk FastAPI
- [Python-dotenv](https://github.com/theskumar/python-dotenv) - Manajemen konfigurasi environment

## 📋 Prasyarat

- Python 3.8 atau lebih baru
- pip (Python package manager)

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

Aplikasi akan berjalan di http://localhost:8000

## 📚 Penggunaan API

### Endpoint

- `GET /v1/about` - Informasi umum tentang layanan
- `GET /v1/health` - Health check untuk memastikan layanan berjalan
- `POST /v1/pdf/convert-to-image` - Konversi PDF ke gambar tunggal

## ⚙️ Konfigurasi

Konfigurasi dilakukan melalui file .env:

| Variabel   | Deskripsi                   | Default    |
| ---------- | --------------------------- | ---------- |
| API_KEY    | Kunci API untuk autentikasi | (required) |
| ENV_PATH   | Path ke file .env           | .env       |
| RATE_LIMIT | Batasan rate request        | 5/minute   |

## 🔒 Keamanan

Semua endpoint API (kecuali `/v1/about`) dilindungi dengan API key authentication. Pastikan untuk menyimpan API key Anda dengan aman dan tidak membagikannya kepada pihak yang tidak berwenang.

## 📝 Kontribusi

Kontribusi dan saran selalu diterima. Silakan buat issue atau pull request untuk meningkatkan layanan ini.

## 📄 Lisensi

Hak Cipta © 2025

Dikembangkan oleh Muhammad Syaoki Faradisa (syaokifaradisa09)

Semua hak dilindungi. Kode ini dilindungi hak cipta dan tidak boleh digunakan, didistribusikan, atau direproduksi tanpa izin tertulis dari pemilik.
