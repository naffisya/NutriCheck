-- ============================================================
-- NUTRICHECK DATABASE SCHEMA
-- PostgreSQL / Supabase
-- ============================================================

-- ============================================================
-- ENUM JENIS KELAMIN
-- ============================================================

CREATE TYPE jenis_kelamin_enum AS ENUM (
    'Laki-laki',
    'Perempuan'
);

-- ============================================================
-- TABEL BALITA
-- ============================================================

CREATE TABLE balita (
    id BIGSERIAL PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    jenis_kelamin jenis_kelamin_enum NOT NULL,
    tanggal_lahir DATE,
    nama_orang_tua VARCHAR(100),
    alamat TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- TABEL PEMERIKSAAN
-- ============================================================

CREATE TABLE pemeriksaan (
    id BIGSERIAL PRIMARY KEY,

    balita_id BIGINT NOT NULL,

    umur_bulan INTEGER NOT NULL,

    berat_badan NUMERIC(5,2) NOT NULL,

    tinggi_badan NUMERIC(5,2) NOT NULL,

    tanggal_pemeriksaan DATE DEFAULT CURRENT_DATE,

    -- Hasil Perhitungan Z-Score
    zscore_bb_u NUMERIC(4,2),
    zscore_tb_u NUMERIC(4,2),
    zscore_bb_tb NUMERIC(4,2),

    -- Status Gizi
    status_gizi VARCHAR(50),
    status_bb_u VARCHAR(50),
    status_tb_u VARCHAR(50),
    status_bb_tb VARCHAR(50),

    -- Ringkasan Analisis
    ringkasan_analisis TEXT,

    -- Disimpan dalam format JSON
    rekomendasi_nutrisi JSONB,

    created_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT fk_balita
    FOREIGN KEY (balita_id)
    REFERENCES balita(id)
    ON DELETE CASCADE
);

-- ============================================================
-- TABEL TIPS NUTRISI
-- ============================================================

CREATE TABLE tips_nutrisi (
    id BIGSERIAL PRIMARY KEY,

    judul VARCHAR(100) NOT NULL,

    deskripsi TEXT NOT NULL,

    kategori VARCHAR(50) DEFAULT 'Umum',

    ikon VARCHAR(20),

    is_active BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- TABEL LAPORAN PDF
-- ============================================================

CREATE TABLE laporan (
    id BIGSERIAL PRIMARY KEY,

    pemeriksaan_id BIGINT NOT NULL,

    nama_file VARCHAR(255) NOT NULL,

    file_url TEXT NOT NULL,

    ukuran_file BIGINT,

    created_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT fk_pemeriksaan
    FOREIGN KEY (pemeriksaan_id)
    REFERENCES pemeriksaan(id)
    ON DELETE CASCADE
);

-- ============================================================
-- INDEX
-- ============================================================

CREATE INDEX idx_balita_nama
ON balita(nama);

CREATE INDEX idx_pemeriksaan_balita
ON pemeriksaan(balita_id);

CREATE INDEX idx_laporan_pemeriksaan
ON laporan(pemeriksaan_id);

-- ============================================================
-- TRIGGER UPDATE updated_at
-- ============================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS
$$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_balita
BEFORE UPDATE ON balita
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- ============================================================
-- DATA AWAL TIPS NUTRISI
-- ============================================================

INSERT INTO tips_nutrisi
(judul, deskripsi, kategori, ikon)
VALUES

(
'Vitamin A',
'Penting untuk menjaga kesehatan mata dan meningkatkan daya tahan tubuh balita.',
'Vitamin',
'🥕'
),

(
'Protein',
'Membantu pertumbuhan otot dan perkembangan jaringan tubuh.',
'Makronutrien',
'🥚'
),

(
'Zat Besi',
'Mencegah anemia dan mendukung perkembangan otak.',
'Mineral',
'🥩'
),

(
'Kalsium',
'Membantu pertumbuhan tulang dan gigi yang kuat.',
'Mineral',
'🥛'
),

(
'Vitamin C',
'Meningkatkan daya tahan tubuh dan membantu penyerapan zat besi.',
'Vitamin',
'🍊'
),

(
'Omega 3',
'Mendukung perkembangan otak dan kesehatan mata.',
'Lemak',
'🐟'
),

(
'Serat',
'Membantu menjaga kesehatan sistem pencernaan.',
'Makronutrien',
'🥦'
),

(
'Zinc',
'Membantu pertumbuhan sel dan meningkatkan sistem imun.',
'Mineral',
'🌰'
);