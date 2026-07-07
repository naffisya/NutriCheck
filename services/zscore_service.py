"""
Service Z-Score — Perhitungan Z-Score untuk status gizi balita.

Menggunakan standar WHO untuk menghitung:
- BB/U  (Berat Badan menurut Umur)
- TB/U  (Tinggi Badan menurut Umur)
- BB/TB (Berat Badan menurut Tinggi Badan)

Referensi: WHO Child Growth Standards (2006)
"""


# ============================================================
# DATA REFERENSI MEDIAN & SD (WHO SIMPLIFIED)
# Format: umur_bulan -> (median, sd)
# ============================================================

# Berat Badan menurut Umur (BB/U) — Laki-laki
BB_U_LAKI = {
    0: (3.3, 0.5), 1: (4.5, 0.6), 2: (5.6, 0.7), 3: (6.4, 0.8),
    4: (7.0, 0.8), 5: (7.5, 0.9), 6: (7.9, 0.9), 7: (8.3, 0.9),
    8: (8.6, 1.0), 9: (8.9, 1.0), 10: (9.2, 1.0), 11: (9.4, 1.0),
    12: (9.6, 1.1), 13: (9.9, 1.1), 14: (10.1, 1.1), 15: (10.3, 1.1),
    16: (10.5, 1.2), 17: (10.7, 1.2), 18: (10.9, 1.2), 19: (11.1, 1.2),
    20: (11.3, 1.3), 21: (11.5, 1.3), 22: (11.8, 1.3), 23: (12.0, 1.3),
    24: (12.2, 1.4), 30: (13.3, 1.5), 36: (14.3, 1.6), 42: (15.3, 1.7),
    48: (16.3, 1.8), 54: (17.3, 2.0), 60: (18.3, 2.1),
}

# Berat Badan menurut Umur (BB/U) — Perempuan
BB_U_PEREMPUAN = {
    0: (3.2, 0.4), 1: (4.2, 0.5), 2: (5.1, 0.6), 3: (5.8, 0.7),
    4: (6.4, 0.7), 5: (6.9, 0.8), 6: (7.3, 0.8), 7: (7.6, 0.8),
    8: (7.9, 0.9), 9: (8.2, 0.9), 10: (8.5, 0.9), 11: (8.7, 1.0),
    12: (8.9, 1.0), 13: (9.2, 1.0), 14: (9.4, 1.0), 15: (9.6, 1.1),
    16: (9.8, 1.1), 17: (10.0, 1.1), 18: (10.2, 1.1), 19: (10.4, 1.2),
    20: (10.6, 1.2), 21: (10.9, 1.2), 22: (11.1, 1.2), 23: (11.3, 1.3),
    24: (11.5, 1.3), 30: (12.7, 1.5), 36: (13.9, 1.6), 42: (15.0, 1.7),
    48: (16.1, 1.8), 54: (17.2, 2.0), 60: (18.2, 2.1),
}

# Tinggi Badan menurut Umur (TB/U) — Laki-laki (cm)
TB_U_LAKI = {
    0: (49.9, 1.9), 1: (54.7, 2.0), 2: (58.4, 2.1), 3: (61.4, 2.1),
    4: (63.9, 2.2), 5: (65.9, 2.2), 6: (67.6, 2.3), 7: (69.2, 2.3),
    8: (70.6, 2.3), 9: (72.0, 2.4), 10: (73.3, 2.4), 11: (74.5, 2.4),
    12: (75.7, 2.5), 13: (76.9, 2.5), 14: (78.0, 2.5), 15: (79.1, 2.6),
    16: (80.2, 2.6), 17: (81.2, 2.6), 18: (82.3, 2.7), 19: (83.2, 2.7),
    20: (84.2, 2.7), 21: (85.1, 2.8), 22: (86.0, 2.8), 23: (86.9, 2.8),
    24: (87.8, 2.9), 30: (91.9, 3.1), 36: (95.7, 3.3), 42: (99.1, 3.5),
    48: (102.4, 3.7), 54: (105.6, 3.9), 60: (108.6, 4.1),
}

# Tinggi Badan menurut Umur (TB/U) — Perempuan (cm)
TB_U_PEREMPUAN = {
    0: (49.1, 1.9), 1: (53.7, 1.9), 2: (57.1, 2.0), 3: (59.8, 2.1),
    4: (62.1, 2.1), 5: (64.0, 2.2), 6: (65.7, 2.2), 7: (67.3, 2.3),
    8: (68.7, 2.3), 9: (70.1, 2.3), 10: (71.5, 2.4), 11: (72.8, 2.4),
    12: (74.0, 2.5), 13: (75.2, 2.5), 14: (76.4, 2.5), 15: (77.5, 2.6),
    16: (78.6, 2.6), 17: (79.7, 2.6), 18: (80.7, 2.7), 19: (81.7, 2.7),
    20: (82.7, 2.7), 21: (83.7, 2.8), 22: (84.6, 2.8), 23: (85.5, 2.8),
    24: (86.4, 2.9), 30: (90.7, 3.1), 36: (94.6, 3.3), 42: (98.1, 3.5),
    48: (101.5, 3.7), 54: (104.8, 3.9), 60: (107.9, 4.1),
}

# Berat Badan menurut Tinggi Badan (BB/TB) — Laki-laki
# Format: tinggi_badan_cm -> (median_bb, sd)
BB_TB_LAKI = {
    45: (2.4, 0.3), 50: (3.2, 0.4), 55: (4.5, 0.5), 60: (5.9, 0.6),
    65: (7.1, 0.7), 70: (8.4, 0.8), 75: (9.5, 0.9), 80: (10.4, 1.0),
    85: (11.4, 1.1), 90: (12.5, 1.2), 95: (13.7, 1.3), 100: (15.1, 1.4),
    105: (16.6, 1.6), 110: (18.2, 1.8), 115: (20.0, 2.0), 120: (22.0, 2.2),
}

# Berat Badan menurut Tinggi Badan (BB/TB) — Perempuan
BB_TB_PEREMPUAN = {
    45: (2.3, 0.3), 50: (3.1, 0.4), 55: (4.3, 0.5), 60: (5.7, 0.6),
    65: (6.9, 0.7), 70: (8.1, 0.8), 75: (9.2, 0.9), 80: (10.2, 1.0),
    85: (11.2, 1.1), 90: (12.3, 1.2), 95: (13.5, 1.3), 100: (14.9, 1.4),
    105: (16.4, 1.6), 110: (18.0, 1.8), 115: (19.8, 2.0), 120: (21.8, 2.2),
}


def _interpolate(table, value):
    """
    Interpolasi linear untuk mendapatkan median dan SD
    dari tabel referensi jika nilai tidak ada persis di tabel.
    """
    keys = sorted(table.keys())

    # Jika nilai persis ada di tabel
    if value in table:
        return table[value]

    # Jika di bawah range minimum
    if value <= keys[0]:
        return table[keys[0]]

    # Jika di atas range maksimum
    if value >= keys[-1]:
        return table[keys[-1]]

    # Cari dua titik terdekat untuk interpolasi
    for i in range(len(keys) - 1):
        if keys[i] <= value <= keys[i + 1]:
            k1, k2 = keys[i], keys[i + 1]
            m1, s1 = table[k1]
            m2, s2 = table[k2]

            # Interpolasi linear
            ratio = (value - k1) / (k2 - k1)
            median = m1 + ratio * (m2 - m1)
            sd = s1 + ratio * (s2 - s1)
            return (round(median, 2), round(sd, 2))

    return table[keys[-1]]


def hitung_zscore(jenis_kelamin, umur_bulan, berat_badan, tinggi_badan):
    """
    Menghitung Z-Score berdasarkan data balita.

    Parameters:
        jenis_kelamin (str): 'Laki-laki' atau 'Perempuan'
        umur_bulan (int): Umur dalam bulan (0-60)
        berat_badan (float): Berat badan dalam kg
        tinggi_badan (float): Tinggi badan dalam cm

    Returns:
        dict: {
            'zscore_bb_u': float,
            'zscore_tb_u': float,
            'zscore_bb_tb': float,
            'status_bb_u': str,
            'status_tb_u': str,
            'status_bb_tb': str,
            'status_gizi': str,
            'ringkasan_analisis': str,
            'rekomendasi_nutrisi': list[dict]
        }
    """
    is_laki = jenis_kelamin == "Laki-laki"

    # ---- Pilih tabel referensi ----
    tabel_bb_u = BB_U_LAKI if is_laki else BB_U_PEREMPUAN
    tabel_tb_u = TB_U_LAKI if is_laki else TB_U_PEREMPUAN
    tabel_bb_tb = BB_TB_LAKI if is_laki else BB_TB_PEREMPUAN

    # ---- Hitung Z-Score BB/U ----
    median_bb_u, sd_bb_u = _interpolate(tabel_bb_u, umur_bulan)
    zscore_bb_u = round((berat_badan - median_bb_u) / sd_bb_u, 2) if sd_bb_u else 0

    # ---- Hitung Z-Score TB/U ----
    median_tb_u, sd_tb_u = _interpolate(tabel_tb_u, umur_bulan)
    zscore_tb_u = round((tinggi_badan - median_tb_u) / sd_tb_u, 2) if sd_tb_u else 0

    # ---- Hitung Z-Score BB/TB ----
    median_bb_tb, sd_bb_tb = _interpolate(tabel_bb_tb, tinggi_badan)
    zscore_bb_tb = round((berat_badan - median_bb_tb) / sd_bb_tb, 2) if sd_bb_tb else 0

    # ---- Tentukan Status ----
    status_bb_u = _klasifikasi_bb_u(zscore_bb_u)
    status_tb_u = _klasifikasi_tb_u(zscore_tb_u)
    status_bb_tb = _klasifikasi_bb_tb(zscore_bb_tb)
    status_gizi = _tentukan_status_gizi(zscore_bb_u, zscore_tb_u, zscore_bb_tb)

    # ---- Buat Ringkasan Analisis ----
    ringkasan = _buat_ringkasan(
        status_bb_u, status_tb_u, status_bb_tb, status_gizi,
        zscore_bb_u, zscore_tb_u, zscore_bb_tb
    )

    # ---- Buat Rekomendasi Nutrisi ----
    rekomendasi = _buat_rekomendasi(status_gizi, status_bb_u, status_tb_u, status_bb_tb)

    return {
        "zscore_bb_u": zscore_bb_u,
        "zscore_tb_u": zscore_tb_u,
        "zscore_bb_tb": zscore_bb_tb,
        "status_bb_u": status_bb_u,
        "status_tb_u": status_tb_u,
        "status_bb_tb": status_bb_tb,
        "status_gizi": status_gizi,
        "ringkasan_analisis": ringkasan,
        "rekomendasi_nutrisi": rekomendasi,
    }


def _klasifikasi_bb_u(zscore):
    """Klasifikasi BB/U berdasarkan Z-Score."""
    if zscore < -3:
        return "Berat Badan Sangat Kurang"
    elif zscore < -2:
        return "Berat Badan Kurang"
    elif zscore <= 1:
        return "Berat Badan Normal"
    else:
        return "Risiko Berat Badan Lebih"


def _klasifikasi_tb_u(zscore):
    """Klasifikasi TB/U berdasarkan Z-Score."""
    if zscore < -3:
        return "Sangat Pendek (Severely Stunted)"
    elif zscore < -2:
        return "Pendek (Stunted)"
    elif zscore <= 3:
        return "Normal"
    else:
        return "Tinggi"


def _klasifikasi_bb_tb(zscore):
    """Klasifikasi BB/TB berdasarkan Z-Score."""
    if zscore < -3:
        return "Gizi Buruk (Severely Wasted)"
    elif zscore < -2:
        return "Gizi Kurang (Wasted)"
    elif zscore <= 1:
        return "Gizi Baik (Normal)"
    elif zscore <= 2:
        return "Berisiko Gizi Lebih"
    elif zscore <= 3:
        return "Gizi Lebih (Overweight)"
    else:
        return "Obesitas"


def _tentukan_status_gizi(zscore_bb_u, zscore_tb_u, zscore_bb_tb):
    """Menentukan status gizi keseluruhan."""
    if zscore_bb_tb < -3 or zscore_bb_u < -3:
        return "Gizi Buruk"
    elif zscore_bb_tb < -2 or zscore_bb_u < -2:
        return "Gizi Kurang"
    elif zscore_bb_tb > 2:
        return "Gizi Lebih"
    elif zscore_bb_tb > 3:
        return "Obesitas"
    else:
        return "Gizi Baik"


def _buat_ringkasan(status_bb_u, status_tb_u, status_bb_tb, status_gizi,
                     zscore_bb_u, zscore_tb_u, zscore_bb_tb):
    """Membuat ringkasan analisis dalam bentuk teks."""
    ringkasan = (
        f"Hasil analisis status gizi menunjukkan status keseluruhan: {status_gizi}.\n\n"
        f"📊 Detail Indikator:\n"
        f"• BB/U (Z-Score: {zscore_bb_u}): {status_bb_u}\n"
        f"• TB/U (Z-Score: {zscore_tb_u}): {status_tb_u}\n"
        f"• BB/TB (Z-Score: {zscore_bb_tb}): {status_bb_tb}\n\n"
    )

    if status_gizi == "Gizi Buruk":
        ringkasan += (
            "⚠️ PERHATIAN: Balita mengalami gizi buruk. "
            "Segera konsultasikan ke dokter atau tenaga kesehatan terdekat "
            "untuk penanganan lebih lanjut."
        )
    elif status_gizi == "Gizi Kurang":
        ringkasan += (
            "⚠️ Balita mengalami gizi kurang. "
            "Perlu peningkatan asupan nutrisi dan pemantauan rutin."
        )
    elif status_gizi == "Gizi Lebih" or status_gizi == "Obesitas":
        ringkasan += (
            "⚠️ Balita mengalami kelebihan gizi. "
            "Perlu pengaturan pola makan dan peningkatan aktivitas fisik."
        )
    else:
        ringkasan += (
            "✅ Status gizi balita baik. "
            "Pertahankan pola makan bergizi seimbang dan lakukan pemeriksaan rutin."
        )

    return ringkasan


def _buat_rekomendasi(status_gizi, status_bb_u, status_tb_u, status_bb_tb):
    """Membuat daftar rekomendasi nutrisi berdasarkan status gizi."""
    rekomendasi = []

    if status_gizi in ("Gizi Buruk", "Gizi Kurang"):
        rekomendasi.extend([
            {
                "judul": "Tingkatkan Asupan Kalori",
                "deskripsi": "Berikan makanan padat energi seperti bubur dengan tambahan minyak, santan, atau mentega.",
                "prioritas": "tinggi"
            },
            {
                "judul": "Tambah Protein Hewani",
                "deskripsi": "Berikan telur, ikan, ayam, atau daging secara rutin untuk mendukung pertumbuhan.",
                "prioritas": "tinggi"
            },
            {
                "judul": "Pemberian Makan Lebih Sering",
                "deskripsi": "Berikan makan 5-6 kali sehari (3 makan utama + 2-3 snack bergizi).",
                "prioritas": "tinggi"
            },
            {
                "judul": "Suplementasi Vitamin A",
                "deskripsi": "Pastikan balita mendapat suplementasi vitamin A sesuai jadwal Posyandu.",
                "prioritas": "sedang"
            },
        ])

    if "Pendek" in status_tb_u or "Stunted" in status_tb_u:
        rekomendasi.extend([
            {
                "judul": "Asupan Kalsium & Vitamin D",
                "deskripsi": "Berikan susu, keju, yogurt, dan paparan sinar matahari pagi untuk pertumbuhan tulang.",
                "prioritas": "tinggi"
            },
            {
                "judul": "Zinc & Zat Besi",
                "deskripsi": "Berikan makanan kaya zinc (daging merah, kacang-kacangan) dan zat besi untuk mendukung pertumbuhan linear.",
                "prioritas": "tinggi"
            },
        ])

    if status_gizi in ("Gizi Lebih", "Obesitas"):
        rekomendasi.extend([
            {
                "judul": "Kurangi Makanan Tinggi Gula",
                "deskripsi": "Batasi pemberian makanan dan minuman manis, ganti dengan buah segar.",
                "prioritas": "tinggi"
            },
            {
                "judul": "Perbanyak Sayur & Buah",
                "deskripsi": "Tingkatkan konsumsi sayur dan buah sebagai sumber serat dan vitamin.",
                "prioritas": "tinggi"
            },
            {
                "judul": "Aktivitas Fisik",
                "deskripsi": "Ajak balita bermain aktif minimal 60 menit sehari.",
                "prioritas": "sedang"
            },
        ])

    if status_gizi == "Gizi Baik":
        rekomendasi.extend([
            {
                "judul": "Pertahankan Pola Makan Seimbang",
                "deskripsi": "Lanjutkan pemberian makanan bergizi seimbang dengan variasi menu.",
                "prioritas": "sedang"
            },
            {
                "judul": "Pemeriksaan Rutin",
                "deskripsi": "Lakukan pemeriksaan pertumbuhan rutin setiap bulan di Posyandu.",
                "prioritas": "sedang"
            },
            {
                "judul": "ASI & Makanan Pendamping",
                "deskripsi": "Untuk balita di bawah 2 tahun, lanjutkan ASI disertai MPASI yang bergizi.",
                "prioritas": "sedang"
            },
        ])

    return rekomendasi
