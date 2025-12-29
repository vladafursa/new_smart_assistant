import logging

from storage3.exceptions import StorageApiError
from supabase import create_client

from src.config import settings

logger = logging.getLogger(__name__)

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


# file upload into supabase storage and its metadata into table
def upload_file(filename: str, content: bytes, category: str):
    try:
        response = supabase.storage.from_(settings.BUCKET_NAME).upload(
            filename, content
        )
        supabase.table(settings.SUPABASE_TABLE).insert(
            {"filename": filename, "category": category}
        ).execute()
        return response
    except StorageApiError as e:
        logger.error("Upload failed: %s", e)
        raise


def get_preview_url(filename: str) -> str:
    return supabase.storage.from_(settings.BUCKET_NAME).get_public_url(filename)


def list_all_files() -> list:
    return supabase.storage.from_(settings.BUCKET_NAME).list()
