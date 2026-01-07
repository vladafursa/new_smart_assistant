from typing import List

from pydantic import BaseModel


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


class UploadResponse(BaseModel):
    message: str
    filename: str
    preview_url: str
    category: str


class FileInfo(BaseModel):
    filename: str
    preview_url: str


class FileListResponse(BaseModel):
    files: list[FileInfo]
