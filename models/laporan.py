"""
Model Laporan — Operasi CRUD untuk tabel 'laporan' di Supabase.
"""

from config.database import supabase


class LaporanModel:
    TABLE = "laporan"

    @staticmethod
    def get_all():
        """Mengambil semua data laporan beserta pemeriksaan terkait."""
        response = (
            supabase.table(LaporanModel.TABLE)
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )
        return response.data

    @staticmethod
    def get_by_id(laporan_id):
        """Mengambil data laporan berdasarkan ID."""
        response = (
            supabase.table(LaporanModel.TABLE)
            .select("*")
            .eq("id", laporan_id)
            .single()
            .execute()
        )
        return response.data

    @staticmethod
    def get_by_pemeriksaan_id(pemeriksaan_id):
        """Mengambil laporan berdasarkan ID pemeriksaan."""
        response = (
            supabase.table(LaporanModel.TABLE)
            .select("*")
            .eq("pemeriksaan_id", pemeriksaan_id)
            .order("created_at", desc=True)
            .execute()
        )
        return response.data

    @staticmethod
    def create(data):
        """
        Membuat record laporan baru.
        data: dict berisi pemeriksaan_id, nama_file, file_url, ukuran_file
        """
        response = (
            supabase.table(LaporanModel.TABLE)
            .insert(data)
            .execute()
        )
        return response.data[0] if response.data else None

    @staticmethod
    def delete(laporan_id):
        """Menghapus data laporan secara permanen."""
        response = (
            supabase.table(LaporanModel.TABLE)
            .delete()
            .eq("id", laporan_id)
            .execute()
        )
        return response.data

    from config.database import supabase
