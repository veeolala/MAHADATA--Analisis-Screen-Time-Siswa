import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


# ==========================================
# 1. KONEKSI DATABASE
# ==========================================

conn = sqlite3.connect("screen_time_siswa.db")

df = pd.read_sql(
    "SELECT * FROM screen_time_siswa",
    conn
)

print("=" * 50)
print("         ANALISIS SCREEN TIME SISWA")
print("=" * 50)


# ==========================================
# 2. PEMERIKSAAN DATA
# ==========================================

print("\nPEMERIKSAAN DATA")
print("-" * 50)

print("Jumlah data:", len(df))
print("Jumlah siswa:", df["student_id"].nunique())
print("Data kosong:", df.isnull().sum().sum())

jumlah_duplikat = df.duplicated(
    subset=["student_id", "log_date"]
).sum()

print("Data duplikat:", jumlah_duplikat)

if len(df) < 1000:
    conn.close()
    raise SystemExit("Data kurang dari 1.000 baris!")


# ==========================================
# 3. RINGKASAN DATA
# ==========================================

print("\nRINGKASAN DATA")
print("-" * 50)

rata_screen_time = df["total_screen_time_hours"].mean()

print("Jumlah catatan:", len(df))

print("Rata-rata screen time:",
      round(rata_screen_time, 2), "jam/hari")

print("Screen time terendah:",
      df["total_screen_time_hours"].min())

print("Screen time tertinggi:",
      df["total_screen_time_hours"].max())


# ==========================================
# 4. KORELASI SCREEN TIME DENGAN DAMPAK
# ==========================================

print("\nKORELASI SCREEN TIME DENGAN DAMPAK")
print("-" * 50)

kolom_dampak = [
    "gpa_academic_score",
    "assignment_completion_rate",
    "sleep_duration_hours",
    "sleep_quality_score",
    "eye_fatigue_level"
]

korelasi = df[kolom_dampak].corrwith(
    df["total_screen_time_hours"]
)

print(korelasi.round(2))


# ==========================================
# 5. DAMPAK BERDASARKAN KATEGORI SCREEN TIME
# ==========================================

print("\nDAMPAK BERDASARKAN KATEGORI SCREEN TIME")
print("-" * 50)

df["kategori"] = pd.cut(
    df["total_screen_time_hours"],
    bins=[float("-inf"), 4, 6, 8, float("inf")],
    labels=["< 4 jam", "4 - <6 jam", "6 - <8 jam", ">= 8 jam"]
)

kategori = df.groupby("kategori", observed=False).agg({
    "student_id": "count",
    "gpa_academic_score": "mean",
    "sleep_duration_hours": "mean",
    "eye_fatigue_level": "mean"
}).round(2)

print(kategori)


# ==========================================
# 6. PERBANDINGAN WEEKDAY DAN WEEKEND
# ==========================================

print("\nPERBANDINGAN WEEKDAY DAN WEEKEND")
print("-" * 50)

hari = df.groupby("day_type").agg({
    "total_screen_time_hours": "mean",
    "screen_time_social_media_hours": "mean",
    "screen_time_gaming_hours": "mean",
    "sleep_duration_hours": "mean"
}).round(2)

hari = hari.reindex(["Weekday", "Weekend"])

print(hari)


# ==========================================
# 7. TOP 10 SISWA SCREEN TIME TERTINGGI
# ==========================================

print("\nTOP 10 SISWA SCREEN TIME TERTINGGI")
print("-" * 50)

top10 = df.groupby("student_id").agg({
    "total_screen_time_hours": "mean"
})

top10 = top10.sort_values(
    by="total_screen_time_hours",
    ascending=False
).head(10).round(2)

print(top10)


# ==========================================
# 8. INTERPRETASI HASIL
# ==========================================

print("\nINTERPRETASI HASIL")
print("-" * 50)

print("Rata-rata screen time siswa:",
      round(rata_screen_time, 2), "jam per hari.")

korelasi_terkuat = korelasi.abs().idxmax()

print("Variabel dengan hubungan paling kuat:",
      korelasi_terkuat)

ipk_rendah = kategori.loc["< 4 jam", "gpa_academic_score"]
ipk_tinggi = kategori.loc[">= 8 jam", "gpa_academic_score"]

if pd.notna(ipk_rendah) and pd.notna(ipk_tinggi):

    selisih_ipk = ipk_tinggi - ipk_rendah

    print("Perbedaan rata-rata IPK antara kategori < 4 jam",
          "dan >= 8 jam:", round(selisih_ipk, 2))

selisih_hari = (
    hari.loc["Weekend", "total_screen_time_hours"]
    - hari.loc["Weekday", "total_screen_time_hours"]
)

print("Perbedaan screen time Weekend dan Weekday:",
      round(selisih_hari, 2), "jam")

print("Catatan: Korelasi tidak membuktikan hubungan sebab-akibat.")


# ==========================================
# 9. GRAFIK 1: HORIZONTAL BAR CHART
# TOP 10 SISWA
# ==========================================

plt.figure(figsize=(9, 6))

top10["total_screen_time_hours"].sort_values().plot(
    kind="barh",
    color="skyblue"
)

plt.title("Top 10 Siswa dengan Screen Time Tertinggi")
plt.xlabel("Rata-rata Screen Time (jam/hari)")
plt.ylabel("ID Siswa")
plt.grid(axis="x")

plt.tight_layout()
plt.savefig("1_top10_siswa.png")
plt.show()


# ==========================================
# 10. GRAFIK 2: SCATTER PLOT
# SCREEN TIME VS DURASI TIDUR
# ==========================================

plt.figure(figsize=(8, 5))

plt.scatter(
    df["total_screen_time_hours"],
    df["sleep_duration_hours"],
    alpha=0.5
)

plt.title("Hubungan Screen Time dengan Durasi Tidur")
plt.xlabel("Total Screen Time (jam)")
plt.ylabel("Durasi Tidur (jam)")
plt.grid(True)

plt.tight_layout()
plt.savefig("2_screen_time_vs_tidur.png")
plt.show()


# ==========================================
# 11. GRAFIK 3: LINE CHART
# TREN SCREEN TIME HARIAN
# ==========================================

df["log_date"] = pd.to_datetime(df["log_date"])

tren_harian = df.groupby("log_date")[
    "total_screen_time_hours"
].mean()

plt.figure(figsize=(10, 5))

plt.plot(
    tren_harian.index,
    tren_harian.values,
    marker="o",
    color="green"
)

plt.title("Tren Rata-rata Screen Time Harian")
plt.xlabel("Tanggal")
plt.ylabel("Rata-rata Screen Time (jam)")
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.savefig("3_tren_screen_time.png")
plt.show()


# ==========================================
# 12. GRAFIK 4: BAR CHART
# WEEKDAY VS WEEKEND
# ==========================================

hari[[
    "total_screen_time_hours",
    "screen_time_social_media_hours",
    "screen_time_gaming_hours",
    "sleep_duration_hours"
]].plot(
    kind="bar",
    figsize=(9, 5)
)

plt.title("Perbandingan Weekday dan Weekend")
plt.xlabel("Jenis Hari")
plt.ylabel("Rata-rata Jam")

plt.legend([
    "Total Screen Time",
    "Media Sosial",
    "Gaming",
    "Tidur"
])

plt.xticks(rotation=0)
plt.grid(axis="y")

plt.tight_layout()
plt.savefig("4_weekday_weekend.png")
plt.show()


# ==========================================
# 13. EXPORT DATA KE EXCEL DAN CSV
# ==========================================

with pd.ExcelWriter("hasil_screen_time.xlsx") as writer:

    df.to_excel(
        writer,
        sheet_name="Data",
        index=False
    )

    korelasi.to_frame("Nilai Korelasi").to_excel(
        writer,
        sheet_name="Korelasi"
    )

    kategori.to_excel(
        writer,
        sheet_name="Kategori Screen Time"
    )

    hari.to_excel(
        writer,
        sheet_name="Weekday Weekend"
    )

    top10.to_excel(
        writer,
        sheet_name="Top 10 Siswa"
    )

df.to_csv("hasil_screen_time.csv", index=False)


# ==========================================
# 14. SELESAI
# ==========================================

print("\n" + "=" * 50)
print("ANALISIS SELESAI!")
print("File Excel dan CSV berhasil dibuat.")
print("Semua grafik berhasil disimpan.")
print("=" * 50)


# ==========================================
# 15. MENUTUP DATABASE
# ==========================================

conn.close()