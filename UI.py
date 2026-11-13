import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# =====================================================
# KONEKSI DATABASE
# =====================================================

db_file = "screen_time_siswa.db"
conn = sqlite3.connect(db_file)

print("=" * 50)
print("VISUALISASI DATABASE SCREEN TIME SISWA")
print("=" * 50)

# =====================================================
# GRAFIK 1: TOP 10 SISWA (BAR CHART)
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

plt.figure(figsize=(10, 5))
plt.bar(top_siswa["student_id"], top_siswa["rata_screen_time"], color="skyblue")
plt.title("Top 10 Siswa Screen Time Tertinggi")
plt.xlabel("Student ID")
plt.ylabel("Rata-rata Screen Time (Jam/Hari)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# =====================================================
# GRAFIK 2: KELELAHAN MATA (PIE CHART)
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

plt.figure(figsize=(8, 5))
plt.pie(kelelahan_df["jumlah"],
        labels=kelelahan_df["tingkat_kelelahan"],
        autopct="%1.1f%%")
plt.title("Distribusi Tingkat Kelelahan Mata (1-5)")
plt.show()

# =====================================================
# GRAFIK 3: TREN MINGGUAN (LINE CHART)
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
# GRAFIK 4: WEEKDAY VS WEEKEND (GROUPED BAR CHART)
# =====================================================

query = """
SELECT day_type,
       ROUND(AVG(screen_time_social_media_hours), 2) AS media_sosial,
       ROUND(AVG(screen_time_gaming_hours), 2) AS gaming
FROM screen_time_siswa
GROUP BY day_type
ORDER BY day_type
"""
weekday_weekend = pd.read_sql(query, conn)
print("\nWEEKDAY VS WEEKEND")
print(weekday_weekend)

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
# GRAFIK 5: SCREEN TIME VS KELELAHAN MATA (SCATTER)
# =====================================================

query = """
SELECT total_screen_time_hours, eye_fatigue_level
FROM screen_time_siswa
WHERE total_screen_time_hours IS NOT NULL
  AND eye_fatigue_level IS NOT NULL
"""
scatter_df = pd.read_sql(query, conn)
print("\nJUMLAH DATA SCATTER:", len(scatter_df))

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

conn.close()
