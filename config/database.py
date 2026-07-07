"""
Konfigurasi koneksi database Supabase.
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def get_supabase_client() -> Client:
    """
    Membuat koneksi Supabase.
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError(
            "SUPABASE_URL dan SUPABASE_KEY harus diatur di file .env"
        )

    return create_client(SUPABASE_URL, SUPABASE_KEY)


# Client global
supabase = get_supabase_client()