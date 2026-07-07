"""
Model Pemeriksaan — Operasi CRUD untuk tabel 'pemeriksaan' di Supabase.
"""

from config.database import supabase


class PemeriksaanModel:
    TABLE = "pemeriksaan"

    @staticmethod
    def get_all():
        """Mengambil semua data pemeriksaan beserta data balita terkait."""
        response = (
            supabase.table(PemeriksaanModel.TABLE)
            .select("*, balita(id, nama, jenis_kelamin, tanggal_lahir)")
            .order("created_at", desc=True)
            .execute()
        )
        return response.data

    @staticmethod
    def get_by_id(pemeriksaan_id):
        """Mengambil data pemeriksaan berdasarkan ID."""
        response = (
            supabase.table(PemeriksaanModel.TABLE)
            .select("*, balita(id, nama, jenis_kelamin, tanggal_lahir)")
            .eq("id", pemeriksaan_id)
            .single()
            .execute()
        )
        return response.data

    @staticmethod
    def get_by_balita_id(balita_id):
        """Mengambil semua pemeriksaan untuk balita tertentu."""
        response = (
            supabase.table(PemeriksaanModel.TABLE)
            .select("*")
            .eq("balita_id", balita_id)
            .order("tanggal_pemeriksaan", desc=True)
            .execute()
        )
        return response.data

    @staticmethod
    def create(data):
        """
        Membuat data pemeriksaan baru.
        data: dict berisi balita_id, umur_bulan, berat_badan, tinggi_badan,
              tanggal_pemeriksaan, zscore_bb_u, zscore_tb_u, zscore_bb_tb,
              status_gizi, status_bb_u, status_tb_u, status_bb_tb,
              ringkasan_analisis, rekomendasi_nutrisi
        """
        response = (
            supabase.table(PemeriksaanModel.TABLE)
            .insert(data)
            .execute()
        )
        return response.data[0] if response.data else None

    @staticmethod
    def update(pemeriksaan_id, data):
        """Mengupdate data pemeriksaan berdasarkan ID."""
        response = (
            supabase.table(PemeriksaanModel.TABLE)
            .update(data)
            .eq("id", pemeriksaan_id)
            .execute()
        )
        return response.data[0] if response.data else None

    @staticmethod
    def delete(pemeriksaan_id):
        """Menghapus data pemeriksaan secara permanen."""
        response = (
            supabase.table(PemeriksaanModel.TABLE)
            .delete()
            .eq("id", pemeriksaan_id)
            .execute()
        )
        return response.data

    @staticmethod
    def get_latest_by_balita(balita_id):
        """Mengambil pemeriksaan terakhir dari balita tertentu."""
        response = (
            supabase.table(PemeriksaanModel.TABLE)
            .select("*")
            .eq("balita_id", balita_id)
            .order("tanggal_pemeriksaan", desc=True)
            .limit(1)
            .execute()
        )
        return response.data[0] if response.data else None
