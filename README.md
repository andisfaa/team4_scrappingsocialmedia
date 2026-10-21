# ♻️ Automated Twitter (X) Data Scraping & Preprocessing: Public Discussion on Organic & Inorganic Waste Management

**Mata Kuliah:** Analisis Media Sosial (*Social Media Analysis*)
**Dosen Pengampu:** Andi Hermanto, S.E., M.Si
**Capaian Tugas:** Pengumpulan & Pembersihan Dataset Media Sosial Min. 1.000 Baris Data Unik

---

## 📄 Ringkasan Eksekutif & Identitas Tim
### Kelompok 4 — Bisnis Digital
* **A. Sifa Ramadani**
* **Nahdatunnisa Alfitrah**
* **Nur Ulfiah Triputri Iskandar**
* **Siti Nurfadillah Rahmah Tasdir**
---

## 🌿 Latar Belakang & Fokus Penelitian

Pengelolaan sampah lingkungan, khususnya pemilahan antara **sampah organik dan anorganik**, merupakan isu krusial yang membutuhkan perhatian luas. Di platform X (Twitter), percakapan seputar krisis sampah sering bercampur dengan berbagai topik lain.

Proyek ini bertujuan untuk mengumpulkan dan memproses dataset perbincangan publik berbahasa Indonesia mengenai sampah secara otomatis, sekaligus menerapkan penyaringan ketat (*data filtering*) untuk menyeleksi konten yang relevan demi kebutuhan analisis sentimen dan edukasi lingkungan.

---

## 📊 Evaluasi Capaian & Kriteria Penugasan

| Parameter Tugas | Target Minimal | Hasil Capaian Kelompok 4 | Status Verifikasi |
| --- | --- | --- | --- |
| **Volume Data Unik** | $\ge 1.000$ Baris | $\ge 1.000$ Baris Valid & Unik | **LULUS** |
| **Automasi Skrip** | Skrip Scraping & Cleaning | `scraping_twitter.py` (All-in-One Pipeline) | **LULUS** |
| **Kelengkapan Berkas** | Dataset & Dokumentasi | `data_twitter.csv` & `README.md` | **LULUS** |

---

## 🛠️ Justifikasi Pemilihan Metodologi Crawling

Dalam mengumpulkan data percakapan publik, kami memanfaatkan kombinasi **`tweet-harvest`** (Node.js & Playwright) dan **Python Pandas**:

```
+-------------------------------------------------------------------------------+
|  Metode: Tweet-Harvest                    |  Metode Alternative: Twitter API v2 |
+-------------------------------------------+-----------------------------------+
| • Bebas biaya untuk riset & akademis      | • Akses search terbatas di tier   |
| • Fleksibel untuk query kata kunci        |   Gratis / Membutuhkan $100+/bulan |
| • Tanpa prosedur verifikasi dev account   | • Verifikasi akun developer rumit |
| • Pengambilan data stabil via Session Token| • Limitasi query pencarian ketat  |
+-------------------------------------------------------------------------------+

```

---

## 📁 Tata Kelola Berkas (Repository Architecture)

Struktur direktori dibuat ringkas dan tersistematis agar mudah dijalankan ulang:

```text
Social Media_Scrapping Klp 4/
├── data_twitter.csv          # File dataset akhir yang telah dibersihkan & disaring
├── scraping_twitter.py       # Skrip otomatisasi utama (crawling, cleaning, & auto-remove raw)
├── requirements.txt          # Library pendukung (pandas)
├── .gitignore                # Pengecualian berkas sistem dan virtual environment (.venv)
└── README.md                 # Dokumentasi teknis proyek

```

---

## 📋 Struktur Kolom Dataset (`data_twitter.csv`)

| Atribut Data | Tipe Data | Deskripsi Lapangan |
| --- | --- | --- |
| `id_str` | String | Unique Identifier dari setiap postingan tweet |
| `created_at` | Datetime | Waktu pembuatan tweet (Format UTC) |
| `username` | String | Handle akun pembuat tweet (`@username`) |
| `full_text` | Text | Teks bersih tweet (newline `\n` dikonversi ke spasi) |
| `favorite_count` | Integer | Akumulasi jumlah apresiasi (Likes) |
| `retweet_count` | Integer | Akumulasi penyebaran ulang (Retweets) |
| `reply_count` | Integer | Jumlah interaksi balasan (Replies) |
| `quote_count` | Integer | Jumlah kutipan tweet (Quotes) |
| `lang` | String | Filter bahasa postingan (`in` = Bahasa Indonesia) |
| `tweet_url` | String | Tautan langsung menuju postingan di platform X |
| `conversation_id_str` | String | ID awal dari utas/percakapan |
| `user_id_str` | String | Unique ID internal akun pengguna |
| `in_reply_to_screen_name` | String | Username target balasan (jika ada) |
| `image_url` | String | Tautan media lampiran (jika ada) |
| `location` | String | Lokasi akun pengguna yang terdaftar |

---

## 🔄 Pipeline Pemrosesan & Pembersihan Data

Pipeline dalam `scraping_twitter.py` bekerja secara berurutan (*end-to-end*):

```text
[1. User Input (Auth Token)] ──► [2. Fetch Raw Data via Tweet-Harvest]
                                               │
                                               ▼
[5. Auto-Cleanup Temp Files]  ◄── [4. Filter Unrelated Topics & Format Text]
            │                                  ▲
            ▼                                  │
[6. Export Final File: data_twitter.csv] ──────┘

```

### Tahapan Pembersihan (*Data Cleaning*):

1. **Deduplikasi ID (`id_str`)**: Mencegah adanya tweet ganda akibat pengulangan pencarian.
2. **Perapian Tata Letak Teks**: Karakter *enter* (`\n`) dihapus dan diubah menjadi spasi tunggal agar tampilan tabel di Excel/CSV teratur rapat.
3. **Penyaringan Konteks Tidak Relevan**: Mengeliminasi tweet yang menggunakan kata "sampah" untuk konteks berita kejahatan/kekerasan di luar isu lingkungan.
4. **Optimalisasi Karakter Encoding**: Menggunakan format `utf-8-sig` agar teks dan emoji tampil utuh tanpa karakter rusak.
5. **Otomasi Pembersihan Berkas Mentah**: Menghapus folder `tweets-data` dan seluruh file `.csv` mentah secara otomatis setelah file utama `data_twitter.csv` terbentuk.



---

## 🚀 Panduan Pengoperasian Skrip

### 1. Persiapan Dependensi

Pastikan **Node.js** ($\ge v18$) dan **Python** ($\ge 3.8$) sudah terpasang. Instal *library* Python yang dibutuhkan:

```powershell
pip install -r requirements.txt

```

### 2. Pengambilan Session `auth_token`

1. Login ke [x.com](https://x.com) pada browser Chrome/Edge.
2. Tekan **F12** $\rightarrow$ Buka tab **Application**.
3. Pilih menu **Cookies** $\rightarrow$ `[https://x.com](https://x.com)`.
4. Salin kode string acak dari kolom Value pada kunci **`auth_token`**.

### 3. Eksekusi Program

Jalankan skrip utama di terminal VS Code:

```powershell
python scraping_twitter.py

```

* Tekan **Enter** untuk menggunakan kata kunci pencarian bawaan: `(sampah OR organik OR anorganik) lang:id`.
* Tekan **Enter** untuk menggunakan limit target bawaan (`2000`).
* Tempelkan (*paste*) nilai `auth_token` Anda saat diminta, lalu tekan **Enter**.

---

## 📈 Rencana Pengembangan Analisis Lanjutan

Dataset bersih yang terkumpul disiapkan untuk tiga tahapan analisis dalam mata kuliah *Social Media Analysis*:

1. **Analisis Sentimen Publik**: Mengkategorikan respons masyarakat terhadap pengolahan sampah organik/anorganik ke dalam kelas positif, netral, atau negatif.
2. **Pemodelan Topik (Topic Modeling)**: Mengelompokkan tren bahasan utama masyarakat (seperti daur ulang plastik, pembuatan pupuk kompos, bank sampah, dll.).
3. **Pola Interaksi Sosial**: Menganalisis tingkat partisipasi dan jangkauan edukasi publik berdasarkan statistik *likes*, *retweets*, dan *replies*.

---

## 🔒 Etika Penulisan & Batasan Penelitian

* Seluruh data yang dihimpun berasal dari domain publik dan ditujukan murni untuk pemenuhan tugas akademik mata kuliah Analisis Media Sosial.
* Tidak ada informasi pribadi yang bersifat rahasia (*Personally Identifiable Information*) yang disimpan atau dipublikasikan.
