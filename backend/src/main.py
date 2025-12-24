from fastapi import FastAPI, UploadFile, File, HTTPException
from src.storage import upload_file
from storage3.exceptions import StorageApiError

api = FastAPI()


@api.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@api.post("/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    try:
        result = upload_file(file.filename, content)
        return {"message": "File uploaded successfully", "result": str(result)}
    except StorageApiError as e:
        raise HTTPException(status_code=403, detail=f"Upload failed: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
