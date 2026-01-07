from typing import List

from pydantic import BaseModel


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
