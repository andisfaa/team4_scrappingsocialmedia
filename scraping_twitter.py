import os
import glob
import subprocess
import pandas as pd

# Konfigurasi Parameter Utama
DEFAULT_KEYWORD = "(sampah OR organik OR anorganik) lang:id"
DEFAULT_LIMIT = 2000
RAW_FILENAME = "data_twitter_raw.csv"
FINAL_FILENAME = "data_twitter.csv"
OUTPUT_DIR = "tweets-data"

# Kata kunci yang tidak relevan dengan topik sampah organik & anorganik
IRRELEVANT_KEYWORDS = [
    "dibunuh", "mayat", "jasad", "pembunuhan", "dibuang ke", "bayi"
]

def run_scraper(keyword, limit, auth_token):
    print("\n[INFO 1/3] Menjalankan proses crawling dengan Tweet-Harvest...")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    cmd = f'npx tweet-harvest@latest -s "{keyword}" -l {limit} -o "{RAW_FILENAME}" -t "{auth_token}"'
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        print("[SUKSES] Proses crawling selesai!\n")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Terjadi kesalahan saat proses scraping: {e}")

def process_and_cleanup():
    print("[INFO 2/3] Memproses, merapikan, dan memfilter data...")
    
    # Kumpulkan semua file CSV mentah yang dihasilkan
    search_path = os.path.join(OUTPUT_DIR, "*.csv")
    all_files = glob.glob(search_path)
    
    if os.path.exists(RAW_FILENAME):
        all_files.append(RAW_FILENAME)
    
    old_raw = "data_twitter_raw.old.csv"
    if os.path.exists(old_raw):
        all_files.append(old_raw)

    if not all_files:
        print("[ERROR] Tidak ada file CSV mentah yang ditemukan untuk diproses.")
        return

    df_list = []
    for file in all_files:
        try:
            temp_df = pd.read_csv(file)
            df_list.append(temp_df)
        except Exception as e:
            print(f"[WARNING] Gagal membaca {file}: {e}")

    if not df_list:
        print("[ERROR] Data mentah kosong.")
        return

    # Gabungkan data
    df = pd.concat(df_list, ignore_index=True)
    
    # 1. Hapus duplikasi berdasarkan ID unik tweet
    df = df.drop_duplicates(subset=["id_str"])
    
    # 2. Hapus baris kosong pada teks
    df = df.dropna(subset=["full_text"])

    # 3. Rapikan teks (ubah enter/newline '\n' menjadi spasi biasa agar rapat)
    df['full_text'] = df['full_text'].astype(str).str.replace(r'\r\n|\r|\n', ' ', regex=True)

    # 4. Filter topik tidak relevan
    df['text_lower'] = df['full_text'].str.lower()
    pattern = '|'.join(IRRELEVANT_KEYWORDS)
    df_filtered = df[~df['text_lower'].str.contains(pattern, na=False)].copy()
    df_filtered = df_filtered.drop(columns=['text_lower'])

    final_count = len(df_filtered)
    print(f"-> Total data bersih akhir: {final_count} baris")

    if final_count < 1000:
        print("⚠️ [PERINGATAN] Data di bawah 1.000 baris. Silakan jalankan ulang jika ingin menambah data.")
    else:
        print("✅ [VALIDASI] Target >= 1.000 baris data bersih berhasil dipenuhi!")

    # Simpan langsung ke SATU file utama
    df_filtered.to_csv(FINAL_FILENAME, index=False, encoding="utf-8-sig")
    print(f"-> Berhasil memperbarui file: {FINAL_FILENAME}\n")

    # --- PENGHAPUSAN OTOMATIS FILE MENTAH SEMENTARA ---
    print("[INFO 3/3] Membersihkan file CSV mentah sisa secara otomatis...")
    
    # Hapus file mentah yang ditemukan
    for file_path in set(all_files):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"-> Menghapus file sementara: {file_path}")
        except Exception as e:
            print(f"[WARNING] Gagal menghapus {file_path}: {e}")
            
    # Hapus folder tweets-data jika sudah kosong
    try:
        if os.path.exists(OUTPUT_DIR) and not os.listdir(OUTPUT_DIR):
            os.rmdir(OUTPUT_DIR)
            print(f"-> Menghapus folder kosong: {OUTPUT_DIR}")
    except Exception:
        pass

    print("\n[SELESAI] Folder Anda kini bersih dan HANYA menyisakan file 'data_twitter.csv'!")

if __name__ == "__main__":
    print("==================================================")
    print("      AUTOMASI SCRAPING & CLEANING TWITTER        ")
    print("==================================================")
    
    keyword_input = input(f"Masukkan Keyword [{DEFAULT_KEYWORD}]: ").strip()
    keyword = keyword_input if keyword_input else DEFAULT_KEYWORD
    
    limit_input = input(f"Masukkan Target Limit [{DEFAULT_LIMIT}]: ").strip()
    limit = int(limit_input) if limit_input else DEFAULT_LIMIT
    
    auth_token = input("Tempelkan (Paste) Twitter auth_token Anda di sini: ").strip()
    
    if auth_token:
        run_scraper(keyword, limit, auth_token)
        process_and_cleanup()
    else:
        print("[ERROR] auth_token wajib diisi untuk menjalankan program!")