"""
FASE 2: Template gambar untuk Tipe A
----------------------------------------
Tujuan:
- Membuat 1 fungsi gambar yang bisa dipakai untuk SEMUA kode Tipe A
- Mengisi fungsi itu dengan angka hasil decode (radius/chamfer/snip)
- Menguji ke kode-kode asli dari data E51

Cara pakai:
1. pip install matplotlib --break-system-packages
2. python fase2_gambar_tipe_a.py
3. Hasilnya: contoh_gambar_tipe_a.png
"""

import re
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Ukuran dasar bar (skema, bukan ukuran asli material)
PANJANG = 300
TINGGI = 100

POLA_TIPE_A = re.compile(
    r'^A(?P<sisi1>[ab])(?:(?P<jenis1>[CR])(?P<nilai1>\d+))?'
    r'(?:(?P<sisi2>[ab])(?P<jenis2>[CR])(?P<nilai2>\d+))?'
    r'(?:S(?P<snip>\d+))?$'
)


def decode_tipe_a(kode):
    """Ubah kode Tipe A (contoh: AaR50S30) jadi dictionary parameter angka."""
    m = POLA_TIPE_A.match(kode)
    if not m:
        raise ValueError(f"Kode '{kode}' tidak sesuai pola Tipe A")
    g = m.groupdict()
    return {
        "kode_asli": kode,
        "jenis1": g["jenis1"],   # 'C' atau 'R' untuk sisi utama (a)
        "nilai1": int(g["nilai1"]) if g["nilai1"] else 0,
        "jenis2": g["jenis2"],   # 'C' atau 'R' untuk sisi kedua (b), kalau ada
        "nilai2": int(g["nilai2"]) if g["nilai2"] else 0,
        "snip": int(g["snip"]) if g["snip"] else 0,
    }


def gambar_tipe_a(ax, params):
    """Gambar 1 komponen Tipe A ke dalam 'ax' (area gambar matplotlib)."""
    # 1. Gambar badan bar (persegi panjang dasar)
    ax.plot([0, PANJANG, PANJANG, 0, 0], [0, 0, TINGGI, TINGGI, 0], "k-", linewidth=1.5)

    ujung_atas = (PANJANG, TINGGI)   # sudut sisi 'a' (atas)
    ujung_bawah = (PANJANG, 0)       # sudut sisi 'b' (bawah)

    # 2. Terapkan perlakuan di sisi 'a' (atas)
    if params["jenis1"] == "R":
        r = params["nilai1"]
        arc = patches.Arc((PANJANG - r, TINGGI - r), r * 2, r * 2,
                           angle=0, theta1=0, theta2=90, color="red", linewidth=2)
        ax.add_patch(arc)
        ax.plot([PANJANG, PANJANG], [TINGGI - r, TINGGI], "r-", linewidth=0)  # placeholder
        ax.text(PANJANG - r * 0.6, TINGGI - r * 0.6, f"R{r}", color="red", fontsize=9)
    elif params["jenis1"] == "C":
        c = params["nilai1"]
        ax.plot([PANJANG - c, PANJANG], [TINGGI, TINGGI - c], "r-", linewidth=2)
        ax.text(PANJANG - c, TINGGI - c * 0.5, f"C{c}", color="red", fontsize=9)

    # 3. Terapkan perlakuan di sisi 'b' (bawah), kalau ada
    if params["jenis2"] == "R":
        r = params["nilai2"]
        arc = patches.Arc((PANJANG - r, r), r * 2, r * 2,
                           angle=0, theta1=270, theta2=360, color="blue", linewidth=2)
        ax.add_patch(arc)
        ax.text(PANJANG - r * 0.6, r * 0.6, f"R{r}", color="blue", fontsize=9)
    elif params["jenis2"] == "C":
        c = params["nilai2"]
        ax.plot([PANJANG - c, PANJANG], [0, c], "b-", linewidth=2)
        ax.text(PANJANG - c, c * 0.5, f"C{c}", color="blue", fontsize=9)

    # 4. Tambahkan tanda snip (sudut potong tambahan) di ujung kanan tengah
    if params["snip"]:
        s = params["snip"]
        ax.plot([PANJANG - 15, PANJANG], [TINGGI / 2 + 12, TINGGI / 2 - 12],
                "g-", linewidth=2)
        ax.text(PANJANG - 45, TINGGI / 2 + 15, f"S{s}\u00b0", color="green", fontsize=9)

    ax.set_xlim(-20, PANJANG + 40)
    ax.set_ylim(-20, TINGGI + 20)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(params["kode_asli"], fontsize=10)


# ---- Uji coba ke 5 kode asli dari data E51 ----
kode_asli_e51 = ["AaC10S30", "AaC10bC10S30", "AaR50S30", "AaR75S30", "AaS30"]

fig, axes = plt.subplots(1, len(kode_asli_e51), figsize=(18, 4))
for ax, kode in zip(axes, kode_asli_e51):
    params = decode_tipe_a(kode)
    gambar_tipe_a(ax, params)

plt.tight_layout()
plt.savefig("contoh_gambar_tipe_a.png", dpi=150, bbox_inches="tight")
print("Selesai! Cek contoh_gambar_tipe_a.png")
