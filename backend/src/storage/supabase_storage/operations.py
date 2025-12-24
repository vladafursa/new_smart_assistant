from src.config import SUPABASE_KEY, SUPABASE_URL
from supabase import create_client


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

BUCKET_NAME = "files"


def upload_file(filename: str, content: bytes):
    return supabase.storage.from_(BUCKET_NAME).upload(filename, content)
