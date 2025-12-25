from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from storage3.exceptions import StorageApiError

from src.storage import get_preview_url, list_all_files, upload_file

api = FastAPI()


class CategoryMeta(BaseModel):
    category: str


@api.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@api.post("/upload")
async def upload(category: str = Form(...), file: UploadFile = File(...)):
    content = await file.read()
    try:
        upload_file(file.filename, content, category)
        preview_url = get_preview_url(file.filename)
        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "preview_url": preview_url,
        }
    except StorageApiError as e:
        raise HTTPException(status_code=403, detail=f"Upload failed: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@api.get("/files")
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
