import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# =====================================================
# KONEKSI DATABASE
# =====================================================

db_file = "screen_time_siswa.db"
conn = sqlite3.connect(db_file)

print("=" * 50)
print("ANALISIS DATABASE SCREEN TIME SISWA")
print("=" * 50)

# =====================================================
# JUMLAH DATA
# =====================================================

query = """
SELECT COUNT(*) AS total_log,
       COUNT(DISTINCT student_id) AS total_siswa,
       COUNT(DISTINCT log_date) AS total_hari
FROM screen_time_siswa
"""
jumlah_data = pd.read_sql(query, conn)
print("\nJUMLAH DATA")
print(jumlah_data)

# =====================================================
# RINGKASAN SCREEN TIME
# =====================================================

query = """
SELECT ROUND(AVG(total_screen_time_hours), 2) AS rata_rata,
       MIN(total_screen_time_hours) AS terendah,
       MAX(total_screen_time_hours) AS tertinggi
FROM screen_time_siswa
"""
ringkasan = pd.read_sql(query, conn)
print("\nRINGKASAN SCREEN TIME")
print(ringkasan)

# =====================================================
# TOP 10 SISWA SCREEN TIME TERTINGGI
# =====================================================

query = """
SELECT student_id,
       ROUND(AVG(total_screen_time_hours), 2) AS rata_screen_time
FROM screen_time_siswa
GROUP BY student_id
ORDER BY rata_screen_time DESC, student_id
LIMIT 10
"""
top_siswa = pd.read_sql(query, conn)
print("\nTOP 10 SISWA")
print(top_siswa)

# =====================================================
# DISTRIBUSI KELELAHAN MATA
# =====================================================

query = """
SELECT eye_fatigue_level AS tingkat_kelelahan,
       COUNT(*) AS jumlah
FROM screen_time_siswa
GROUP BY eye_fatigue_level
ORDER BY eye_fatigue_level
"""
kelelahan_df = pd.read_sql(query, conn)
print("\nDISTRIBUSI KELELAHAN MATA")
print(kelelahan_df)

# =====================================================
# TREN SCREEN TIME MINGGUAN
# =====================================================

query = """
SELECT strftime('%Y-%W', log_date) AS minggu,
       ROUND(AVG(total_screen_time_hours), 2) AS rata_screen_time
FROM screen_time_siswa
GROUP BY minggu
ORDER BY minggu
"""
tren_mingguan = pd.read_sql(query, conn)
print("\nTREN MINGGUAN")
print(tren_mingguan)

# =====================================================
# WEEKDAY VS WEEKEND
# =====================================================

query = """
SELECT day_type,
       ROUND(AVG(total_screen_time_hours), 2) AS screen_time,
       ROUND(AVG(screen_time_social_media_hours), 2) AS media_sosial,
       ROUND(AVG(screen_time_gaming_hours), 2) AS gaming
FROM screen_time_siswa
GROUP BY day_type
ORDER BY day_type
"""
weekday_weekend = pd.read_sql(query, conn)
print("\nWEEKDAY VS WEEKEND")
print(weekday_weekend)

# =====================================================
# HUBUNGAN SCREEN TIME DAN KELELAHAN MATA
# =====================================================

query = """
SELECT total_screen_time_hours, eye_fatigue_level
FROM screen_time_siswa
WHERE total_screen_time_hours IS NOT NULL
  AND eye_fatigue_level IS NOT NULL
"""
scatter_df = pd.read_sql(query, conn)
print("\nDATA SCATTER PLOT")
print("Jumlah data:", len(scatter_df))

# =====================================================
# VISUALISASI 1: BAR CHART
# =====================================================

plt.figure(figsize=(10, 5))
plt.bar(top_siswa["student_id"], top_siswa["rata_screen_time"])
plt.title("Top 10 Siswa Screen Time Tertinggi")
plt.xlabel("Student ID")
plt.ylabel("Rata-rata Screen Time (Jam/Hari)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# =====================================================
# VISUALISASI 2: PIE CHART
# =====================================================

plt.figure(figsize=(8, 5))
plt.pie(kelelahan_df["jumlah"],
        labels=kelelahan_df["tingkat_kelelahan"],
        autopct="%1.1f%%")
plt.title("Distribusi Tingkat Kelelahan Mata (1-5)")
plt.show()

# =====================================================
# VISUALISASI 3: LINE CHART
# =====================================================

plt.figure(figsize=(10, 5))
plt.plot(tren_mingguan["minggu"], tren_mingguan["rata_screen_time"], marker="o")
plt.title("Tren Screen Time Mingguan")
plt.xlabel("Minggu")
plt.ylabel("Rata-rata Screen Time (Jam/Hari)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# =====================================================
# VISUALISASI 4: GROUPED BAR CHART
# =====================================================

x = range(len(weekday_weekend))
plt.figure(figsize=(8, 5))
plt.bar([i - 0.2 for i in x], weekday_weekend["media_sosial"],
        width=0.4, label="Media Sosial")
plt.bar([i + 0.2 for i in x], weekday_weekend["gaming"],
        width=0.4, label="Gaming")
plt.xticks(list(x), weekday_weekend["day_type"])
plt.title("Media Sosial dan Gaming: Weekday vs Weekend")
plt.xlabel("Jenis Hari")
plt.ylabel("Rata-rata Jam/Hari")
plt.legend()
plt.tight_layout()
plt.show()

# =====================================================
# VISUALISASI 5: SCATTER PLOT
# =====================================================

plt.figure(figsize=(10, 5))
plt.scatter(scatter_df["total_screen_time_hours"],
            scatter_df["eye_fatigue_level"], alpha=0.3)
plt.title("Hubungan Screen Time dengan Kelelahan Mata")
plt.xlabel("Screen Time (Jam/Hari)")
plt.ylabel("Tingkat Kelelahan Mata (1-5)")
plt.yticks([1, 2, 3, 4, 5])
plt.grid(True)
plt.tight_layout()
plt.show()

# =====================================================
# EXPORT KE EXCEL
# =====================================================

with pd.ExcelWriter("laporan_analisis_screen_time.xlsx") as writer:
    jumlah_data.to_excel(writer, sheet_name="Jumlah Data", index=False)
    ringkasan.to_excel(writer, sheet_name="Ringkasan", index=False)
    top_siswa.to_excel(writer, sheet_name="Top Siswa", index=False)
    kelelahan_df.to_excel(writer, sheet_name="Kelelahan Mata", index=False)
    tren_mingguan.to_excel(writer, sheet_name="Tren Mingguan", index=False)
    weekday_weekend.to_excel(writer, sheet_name="Weekday Weekend", index=False)
    scatter_df.to_excel(writer, sheet_name="Data Scatter", index=False)

print("\nFile laporan_analisis_screen_time.xlsx berhasil dibuat.")
# =====================================================
# EXPORT KE CSV
# =====================================================

top_siswa.to_csv("top_10_siswa.csv", index=False)
kelelahan_df.to_csv("distribusi_kelelahan_mata.csv", index=False)
tren_mingguan.to_csv("tren_screen_time_mingguan.csv", index=False)
weekday_weekend.to_csv("weekday_weekend.csv", index=False)
scatter_df.to_csv("hubungan_screen_time_kelelahan.csv", index=False)

print("File CSV berhasil dibuat.")

conn.close()
