import logging
from typing import List

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from storage3.exceptions import StorageApiError

from src.ml import generate_answer, query_index
from src.ml.classification import classify
from src.storage import get_preview_url, init_index, list_all_files, unified_upload

index = init_index()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
    ],
)

NOISY_LIBS = [
    "httpx",
    "httpcore",
    "hpack",
    "urllib3",
    "asyncio",
    "uvicorn.error",
    "uvicorn.access",
]

for lib in NOISY_LIBS:
    logging.getLogger(lib).setLevel(logging.WARNING)


api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CategoryMeta(BaseModel):
    category: str


class ChunkMetadata(BaseModel):
    text: str
    source: str
    category: str
    entities: List[str]


class QueryResponse(BaseModel):
    answer: str
    chunks: List[ChunkMetadata]


class QueryRequest(BaseModel):
    question: str


@api.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@api.post("/upload")
async def upload(category: str = Form(...), file: UploadFile = File(...)):
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


@api.post("/rag", response_model=QueryResponse)
def rag_endpoint(request: QueryRequest):
    category = classify(request.question)
    context_chunks = query_index(index, request.question, category)
    context_text = "\n\n".join([chunk["text"] for chunk in context_chunks])
    answer = generate_answer(context_text, request.question)
    return QueryResponse(answer=answer, chunks=context_chunks)
