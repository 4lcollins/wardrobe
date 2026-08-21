from src.settings import SETTINGS
from supabase import Client, create_client


def get_supabase() -> Client:
    if not SETTINGS.supabase_url or not SETTINGS.supabase_key:
        raise RuntimeError("Supabase is not configured. Set SUPABASE_URL and SUPABASE_KEY.")

    return create_client(SETTINGS.supabase_url, SETTINGS.supabase_key)
