from .pinecone_storage import init_index, process_file
from .supabase_storage import get_preview_url, upload_file


def unified_upload(filename: str, content: bytes, category: str, index):
    upload_file(filename, content, category)
    preview_url = get_preview_url(filename)
    process_file(filename, content, index, category)
    return {"preview_url": preview_url}
