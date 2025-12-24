from src.config import SUPABASE_KEY, SUPABASE_URL
from supabase import create_client
from storage3.exceptions import StorageApiError


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

BUCKET_NAME = "files"


def upload_file(filename: str, content: bytes):
    try:
        return supabase.storage.from_(BUCKET_NAME).upload(filename, content)
    except StorageApiError as e:
        print(f"Upload failed: {e}")
        raise
