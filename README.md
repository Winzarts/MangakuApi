# Mangaku API (Komiku Scraper)

API mangaku adalah sebuah REST API sederhana yang dibuat menggunakan Flask untuk melakukan scraping data komik dari situs Komiku. API ini memungkinkan Anda untuk mendapatkan daftar genre, komik terbaru, komik populer, pencarian komik, serta detail komik beserta gambarnya.

## ✨ Fitur

- 📂 **Daftar Genre**: Mendapatkan semua kategori genre yang tersedia.
- 🕒 **Update Terbaru**: Mendapatkan daftar komik yang baru saja diperbarui (Manga, Manhwa, Manhua).
- 🏆 **Populer**: Melihat daftar komik yang sedang tren atau populer.
- 🔍 **Pencarian**: Mencari komik berdasarkan judul.
- 📖 **Detail Komik**: Informasi lengkap mengenai komik beserta daftar chapternya.
- 🖼️ **Baca Komik**: Mengambil gambar-gambar per halaman dari sebuah chapter.
- 📃 **Daftar Semua Komik**: Dilengkapi dengan sistem paginasi.

## 🚀 Teknologi yang Digunakan

- **Python 3.x**
- **Flask**: Web Framework.
- **BeautifulSoup4**: HTML Parsing/Scraping.
- **Requests**: HTTP Library.
- **Selenium (Dynamic Scrapper)**: Untuk menangani konten yang dirender via JavaScript.

## 🛠️ Instalasi

1. **Clone repository ini:**

   ```bash
   git clone https://github.com/winzarts/MangakuApi.git
   cd MangakuApi
   ```

2. **Buat Virtual Environment (Opsional tapi disarankan):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Untuk Windows: venv\Scripts\activate
   ```

3. **Install dependensi:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Konfigurasi Environment:**
   Buat file `.env` di direktori akar dan tambahkan variabel berikut:

   ```env
   BASE_URL=https://komiku.id
   API_BASE=http://localhost:3080
   TIMEOUT=10
   ```

5. **Jalankan API:**
   ```bash
   python app.py
   ```
   API akan berjalan di `http://localhost:3080`.

## 📌 Dokumentasi API

### 1. Status API

`GET /`

- Cek apakah API berjalan dengan normal.

### 2. Genre

`GET /genre/`

- Menampilkan semua daftar genre yang tersedia.

`GET /genre/<slug>/`

- Menampilkan daftar komik berdasarkan genre tertentu.
- **Query Params**: `orderby` (default: update), `limit` (default: 30).

### 3. Update Terbaru

`GET /latest`

- Menampilkan semua update komik terbaru.

`GET /latest-manga` / `/latest-manhwa` / `/latest-manhua`

- Menampilkan update terbaru spesifik berdasarkan tipe.

### 4. Populer

`GET /popular`

- Menampilkan komik yang paling populer saat ini.

### 5. Pencarian

`GET /search?q=<judul>`

- Mencari komik berdasarkan judul. Contoh: `/search?q=one+piece`.

### 6. Detail Komik

`GET /manga/<slug>/`

- Menampilkan informasi detail komik, sinopsis, dan daftar chapter.

### 7. Baca Chapter

`GET /manga/<slug>/<chapter_slug>/`

- Menampilkan daftar URL gambar dari chapter yang dipilih.

### 8. Daftar Semua Komik

`GET /list-semua-komik?page=1`

- Menampilkan list komik secara keseluruhan dengan paginasi.

## 🤝 Kontribusi

Kontribusi selalu terbuka! Silakan lakukan fork repository ini dan buat pull request jika ingin menambahkan fitur atau memperbaiki bug.

## 📄 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).
