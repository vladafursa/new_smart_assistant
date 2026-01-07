from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from storage3.exceptions import StorageApiError

from src.apis.storage_models import FileInfo, FileListResponse, UploadResponse
from src.storage import get_preview_url, list_all_files, unified_upload

storage = APIRouter(prefix="/storage", tags=["storage"])


@storage.post("/upload", response_model=UploadResponse)
async def upload(
    request: Request, category: str = Form(...), file: UploadFile = File(...)
):
    index = request.app.state.index
    content = await file.read()
    try:
        result = unified_upload(
            filename=file.filename,
            content=content,
            category=category,
            index=index,
        )

        return UploadResponse(
            message="File uploaded successfully",
            filename=file.filename,
            preview_url=result.preview_url,
            category=category,
        )

    except StorageApiError as e:
        raise HTTPException(status_code=403, detail=f"Upload failed: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@storage.get("/files", response_model=FileListResponse)
async def files():
    try:
        result = list_all_files()

        retrieved_files = [
            FileInfo(filename=obj["name"], preview_url=get_preview_url(obj["name"]))
            for obj in result
            if obj["name"] != ".emptyFolderPlaceholder"
        ]

        return FileListResponse(files=retrieved_files)
    except StorageApiError as e:
        raise HTTPException(status_code=403, detail=f"Listing failed: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
