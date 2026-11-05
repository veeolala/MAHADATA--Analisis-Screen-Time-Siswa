
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# =====================================================
# KONEKSI DATABASE
# =====================================================

db_file = "screen_time_siswa.db"
conn = sqlite3.connect(db_file)

print("=" * 50)
print("       ANALISIS SCREEN TIME SISWA")
print("=" * 50)


# =====================================================
# PEMERIKSAAN DATA
# =====================================================

query = """
SELECT *
FROM screen_time_siswa
"""

df = pd.read_sql(query, conn)

print("\nPEMERIKSAAN DATA")
print("-" * 50)

print("Jumlah data:", len(df))
print("Jumlah siswa:", df["student_id"].nunique())
print("Data kosong:", df.isnull().sum().sum())

if len(df) < 1000:
    conn.close()
    raise SystemExit("Data kurang dari 1.000 baris!")


# =====================================================
# RINGKASAN DATA
# =====================================================

print("\nRINGKASAN DATA")
print("-" * 50)

print("Rata-rata Screen Time:",
      round(df["total_screen_time_hours"].mean(), 2),
      "jam/hari")

print("Screen Time Terendah:",
      df["total_screen_time_hours"].min(), "jam")

print("Screen Time Tertinggi:",
      df["total_screen_time_hours"].max(), "jam")


# =====================================================
# 1. TOP 10 SISWA SCREEN TIME TERTINGGI
# =====================================================

top10 = df.groupby("student_id").agg({
    "total_screen_time_hours": "mean"
})

top10 = top10.sort_values(
    by="total_screen_time_hours",
    ascending=False
).head(10).reset_index()

print("\nTOP 10 SISWA SCREEN TIME TERTINGGI")
print("-" * 50)
print(top10.round(2))


# =====================================================
# VISUALISASI 1: TOP 10 SISWA
# =====================================================

plt.figure(figsize=(12, 6))

plt.bar(
    top10["student_id"].astype(str),
    top10["total_screen_time_hours"],
    color="skyblue"
)

plt.title(
    "Top 10 Siswa dengan Screen Time Tertinggi",
    fontsize=14
)

plt.xlabel("ID Siswa")
plt.ylabel("Rata-rata Screen Time (jam/hari)")

plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)

for i, nilai in enumerate(top10["total_screen_time_hours"]):
    plt.text(
        i,
        nilai,
        f"{nilai:.2f}",
        ha="center",
        va="bottom",
        fontsize=8
    )

plt.tight_layout()
plt.show()


# =====================================================
# 2. KORELASI SCREEN TIME DENGAN DAMPAK
# =====================================================

kolom_dampak = [
    "gpa_academic_score",
    "assignment_completion_rate",
    "sleep_duration_hours",
    "sleep_quality_score",
    "eye_fatigue_level"
]

korelasi = df[kolom_dampak].corrwith(
    df["total_screen_time_hours"]
).reset_index()

korelasi.columns = [
    "Variabel",
    "Nilai Korelasi"
]

print("\nKORELASI SCREEN TIME DENGAN DAMPAK")
print("-" * 50)
print(korelasi.round(2))


# =====================================================
# VISUALISASI 2: KORELASI
# =====================================================

plt.figure(figsize=(10, 6))

plt.barh(
    korelasi["Variabel"],
    korelasi["Nilai Korelasi"],
    color="cornflowerblue"
)

plt.title(
    "Korelasi Screen Time dengan Dampak Akademik dan Kesehatan",
    fontsize=13
)

plt.xlabel("Nilai Korelasi")
plt.ylabel("Variabel")

plt.axvline(
    x=0,
    color="black",
    linewidth=0.8
)

plt.grid(axis="x", linestyle="--", alpha=0.7)

plt.tight_layout()
plt.show()


# =====================================================
# 3. DAMPAK BERDASARKAN KATEGORI SCREEN TIME
# =====================================================

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

print("\nDAMPAK BERDASARKAN KATEGORI SCREEN TIME")
print("-" * 50)
print(kategori)


# =====================================================
# VISUALISASI 3: KATEGORI SCREEN TIME
# =====================================================

plt.figure(figsize=(10, 6))

plt.bar(
    kategori.index.astype(str),
    kategori["gpa_academic_score"],
    color="lightgreen"
)

plt.title(
    "Rata-rata Nilai Akademik Berdasarkan Kategori Screen Time",
    fontsize=13
)

plt.xlabel("Kategori Screen Time")
plt.ylabel("Rata-rata GPA")

plt.grid(axis="y", linestyle="--", alpha=0.7)

plt.tight_layout()
plt.show()


# =====================================================
# 4. PERBANDINGAN WEEKDAY DAN WEEKEND
# =====================================================

hari = df.groupby("day_type").agg({
    "total_screen_time_hours": "mean",
    "screen_time_social_media_hours": "mean",
    "screen_time_gaming_hours": "mean",
    "sleep_duration_hours": "mean"
})

hari = hari.reindex(["Weekday", "Weekend"]).round(2)

print("\nPERBANDINGAN WEEKDAY DAN WEEKEND")
print("-" * 50)
print(hari)


# =====================================================
# VISUALISASI 4: WEEKDAY VS WEEKEND
# =====================================================

plt.figure(figsize=(10, 6))

plt.bar(
    ["Weekday", "Weekend"],
    hari["total_screen_time_hours"],
    color=["skyblue", "orange"]
)

plt.title(
    "Perbandingan Screen Time Weekday dan Weekend",
    fontsize=14
)

plt.xlabel("Jenis Hari")
plt.ylabel("Rata-rata Screen Time (jam)")

plt.grid(axis="y", linestyle="--", alpha=0.7)

for i, nilai in enumerate(hari["total_screen_time_hours"]):
    plt.text(
        i,
        nilai,
        f"{nilai:.2f}",
        ha="center",
        va="bottom"
    )

plt.tight_layout()
plt.show()


# =====================================================
# 5. HUBUNGAN SCREEN TIME DENGAN DURASI TIDUR
# =====================================================

print("\nHUBUNGAN SCREEN TIME DENGAN DURASI TIDUR")
print("-" * 50)

print(
    "Korelasi:",
    round(
        df["total_screen_time_hours"].corr(
            df["sleep_duration_hours"]
        ),
        2
    )
)


# =====================================================
# VISUALISASI 5: SCATTER PLOT
# =====================================================

plt.figure(figsize=(10, 6))

plt.scatter(
    df["total_screen_time_hours"],
    df["sleep_duration_hours"],
    alpha=0.5,
    color="mediumpurple"
)

plt.title(
    "Hubungan Screen Time dengan Durasi Tidur",
    fontsize=14
)

plt.xlabel("Total Screen Time (jam)")
plt.ylabel("Durasi Tidur (jam)")

plt.grid(True, linestyle="--", alpha=0.7)

plt.tight_layout()
plt.show()


# =====================================================
# INTERPRETASI HASIL
# =====================================================

print("\nINTERPRETASI HASIL")
print("-" * 50)

rata_screen_time = df["total_screen_time_hours"].mean()

print(
    "Rata-rata Screen Time:",
    round(rata_screen_time, 2),
    "jam/hari"
)

korelasi_terkuat = korelasi.loc[
    korelasi["Nilai Korelasi"].abs().idxmax()
]

print(
    "Variabel dengan hubungan terkuat:",
    korelasi_terkuat["Variabel"]
)

selisih_hari = (
    hari.loc["Weekend", "total_screen_time_hours"]
    - hari.loc["Weekday", "total_screen_time_hours"]
)

print(
    "Selisih Screen Time Weekend dan Weekday:",
    round(selisih_hari, 2),
    "jam"
)

print(
    "Catatan: Korelasi tidak membuktikan hubungan sebab-akibat."
)


# =====================================================
# SELESAI
# =====================================================

print("\n" + "=" * 50)
print("ANALISIS SCREEN TIME SISWA SELESAI!")
print("=" * 50)

conn.close()
