from fastapi import FastAPI, UploadFile, File, HTTPException
from src.storage import upload_file, get_preview_url
from storage3.exceptions import StorageApiError


api = FastAPI()


@api.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@api.post("/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    try:
        upload_file(file.filename, content)
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
