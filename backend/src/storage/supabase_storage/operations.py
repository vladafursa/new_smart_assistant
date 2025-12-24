from src.config import SUPABASE_KEY, SUPABASE_URL, BUCKET_NAME, SUPABASE_TABLE
from supabase import create_client
from storage3.exceptions import StorageApiError


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def upload_file(filename: str, content: bytes, category: str):
    try:
        response = supabase.storage.from_(BUCKET_NAME).upload(filename, content)
        supabase.table(SUPABASE_TABLE).insert(
            {"filename": filename, "category": category}
        ).execute()
        return response
    except StorageApiError as e:
        print(f"Upload failed: {e}")
        raise


def get_preview_url(filename: str) -> str:
    return supabase.storage.from_(BUCKET_NAME).get_public_url(filename)


def list_all_files() -> list:
    return supabase.storage.from_(BUCKET_NAME).list()
