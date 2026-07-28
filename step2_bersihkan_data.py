"""
STEP 2: Bersihkan hasil ekstraksi PDF 1
------------------------------------------
Tujuan script ini:
- Membaca file hasil Step 1 (yang masih ada baris judul & sel kosong)
- Memperbaiki header yang salah
- Mengisi otomatis sel-sel kosong akibat merged cell (forward fill)
- Membuang baris-baris kosong (pemisah antar komponen)
- Menyimpan hasil bersih ke file baru

Cara pakai:
1. Pastikan file hasil Step 1 ada di folder yang sama
2. Ganti FILE_INPUT sesuai nama file kamu
3. Jalankan: python step2_bersihkan_data.py
4. Hasilnya ada di "data_bersih.csv"
"""

import pandas as pd

FILE_INPUT = "8242_A31_merge_00001_extract.xlsx"

# 1. Baca file, tapi kasih tahu pandas: header sebenarnya ada di baris ke-2
#    (header=1 artinya "lewati baris ke-1, pakai baris ke-2 sebagai nama kolom")
df = pd.read_excel(FILE_INPUT, header=1)

# 2. Buang baris yang SELURUH isinya kosong (baris pemisah antar komponen)
df = df.dropna(how="all")

# 3. Kolom-kolom ini isinya cuma ada di baris pertama tiap kelompok
#    (karena merged cell). Kita isi otomatis pakai nilai dari baris di atasnya.
kolom_perlu_diisi = ["Drawing No", "Material", "Qty", "Grade", "Size",
                     "Part Name", "Qty (Part)", "Scale", "Page"]

for kolom in kolom_perlu_diisi:
    if kolom in df.columns:
        df[kolom] = df[kolom].ffill()  # ffill = "forward fill", isi pakai nilai di atasnya

# 4. Simpan hasil yang sudah bersih
df.to_csv("data_bersih.csv", index=False, encoding="utf-8-sig")

print("Selesai! Cek file data_bersih.csv")
print(f"Total baris setelah dibersihkan: {len(df)}")
print(f"Jumlah kode 'Detail' (상세) unik: {df['Detail'].nunique()}")

# 5. Bonus: cek ulang apakah ada kode yang murni angka (buat mastiin asumsimu benar)
kode_angka = df[df["Detail"].astype(str).str.match(r"^\d+$", na=False)]
print(f"Jumlah baris dengan kode murni angka: {len(kode_angka)}")
