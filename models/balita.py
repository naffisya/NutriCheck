"""
Model Balita — Operasi CRUD untuk tabel 'balita' di Supabase.
"""

from config.database import supabase


class BalitaModel:
    TABLE = "balita"

    @staticmethod
    def get_all():
        """Mengambil semua data balita yang aktif."""
        response = (
            supabase.table(BalitaModel.TABLE)
            .select("*")
            .eq("is_active", True)
            .order("created_at", desc=True)
            .execute()
        )
        return response.data

    @staticmethod
    def get_by_id(balita_id):
        """Mengambil data balita berdasarkan ID."""
        response = (
            supabase.table(BalitaModel.TABLE)
            .select("*")
            .eq("id", balita_id)
            .eq("is_active", True)
            .single()
            .execute()
        )
        return response.data

    @staticmethod
    def create(data):
        """
        Membuat data balita baru.
        data: dict dengan keys: nama, jenis_kelamin, tanggal_lahir,
              nama_orang_tua, alamat
        """
        response = (
            supabase.table(BalitaModel.TABLE)
            .insert(data)
            .execute()
        )
        return response.data[0] if response.data else None

    @staticmethod
    def update(balita_id, data):
        """Mengupdate data balita berdasarkan ID."""
        response = (
            supabase.table(BalitaModel.TABLE)
            .update(data)
            .eq("id", balita_id)
            .execute()
        )
        return response.data[0] if response.data else None

    @staticmethod
    def delete(balita_id):
        """Soft delete — set is_active = False."""
        response = (
            supabase.table(BalitaModel.TABLE)
            .update({"is_active": False})
            .eq("id", balita_id)
            .execute()
        )
        return response.data[0] if response.data else None

    @staticmethod
    def search(keyword):
        """Mencari balita berdasarkan nama (case-insensitive)."""
        response = (
            supabase.table(BalitaModel.TABLE)
            .select("*")
            .ilike("nama", f"%{keyword}%")
            .eq("is_active", True)
            .order("nama")
            .execute()
        )
        return response.data
