from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from storage3.exceptions import StorageApiError

from src.storage import get_preview_url, list_all_files, unified_upload

storage = APIRouter(prefix="/storage", tags=["storage"])


@storage.post("/upload")
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

        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "preview_url": result["preview_url"],
            "category": category,
        }

    except StorageApiError as e:
        raise HTTPException(status_code=403, detail=f"Upload failed: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@storage.get("/files")
async def files():
    try:
        result = list_all_files()
        return {
            "files": [
                {"filename": obj["name"], "preview_url": get_preview_url(obj["name"])}
                for obj in result
                if obj["name"] != ".emptyFolderPlaceholder"
            ]
        }
    except StorageApiError as e:
        raise HTTPException(status_code=403, detail=f"Listing failed: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
