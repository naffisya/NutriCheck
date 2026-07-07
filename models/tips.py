"""
Model Tips Nutrisi — Operasi CRUD untuk tabel 'tips_nutrisi' di Supabase.
"""

from config.database import supabase


class TipsModel:
    TABLE = "tips_nutrisi"

    @staticmethod
    def get_all():
        """Mengambil semua tips nutrisi yang aktif."""
        response = (
            supabase.table(TipsModel.TABLE)
            .select("*")
            .eq("is_active", True)
            .order("created_at", desc=True)
            .execute()
        )
        return response.data

    @staticmethod
    def get_by_id(tips_id):
        """Mengambil tips nutrisi berdasarkan ID."""
        response = (
            supabase.table(TipsModel.TABLE)
            .select("*")
            .eq("id", tips_id)
            .eq("is_active", True)
            .single()
            .execute()
        )
        return response.data

    @staticmethod
    def get_by_kategori(kategori):
        """Mengambil tips nutrisi berdasarkan kategori."""
        response = (
            supabase.table(TipsModel.TABLE)
            .select("*")
            .eq("kategori", kategori)
            .eq("is_active", True)
            .order("judul")
            .execute()
        )
        return response.data

    @staticmethod
    def create(data):
        """
        Membuat tips nutrisi baru.
        data: dict berisi judul, deskripsi, kategori, ikon
        """
        response = (
            supabase.table(TipsModel.TABLE)
            .insert(data)
            .execute()
        )
        return response.data[0] if response.data else None

    @staticmethod
    def update(tips_id, data):
        """Mengupdate tips nutrisi berdasarkan ID."""
        response = (
            supabase.table(TipsModel.TABLE)
            .update(data)
            .eq("id", tips_id)
            .execute()
        )
        return response.data[0] if response.data else None

    @staticmethod
    def delete(tips_id):
        """Soft delete — set is_active = False."""
        response = (
            supabase.table(TipsModel.TABLE)
            .update({"is_active": False})
            .eq("id", tips_id)
            .execute()
        )
        return response.data[0] if response.data else None
    @staticmethod
    def get_by_status(status):
        """ 
        Mengambil rekomendasi sesuai status gizi.
        """

        response = (
            supabase.table(TipsModel.TABLE)
            .select("*")
            .eq("target_status", status)
            .eq("is_active", True)
            .execute()
        )

        return response.data
    @staticmethod
    def get_by_target(target):
        response = (
            supabase.table(TipsModel.TABLE)
            .select("*")
            .eq("target", target)
            .eq("is_active", True)
            .execute()
        )
        return response.data
    
    @staticmethod
    def get_rekomendasi(status_gizi):
        """
        Mengambil rekomendasi berdasarkan status gizi.
        """

        response = (
            supabase.table(TipsModel.TABLE)
            .select("*")
            .eq("kategori", status_gizi)
            .eq("is_active", True)
            .execute()
        )

        return response.data