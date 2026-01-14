from typing import List

from pydantic import BaseModel, HttpUrl


class UploadResponse(BaseModel):
    message: str
    filename: str
    preview_url: HttpUrl
    category: str

    class Config:
        json_schema_extra = {
            "example": {
                "message": "File uploaded successfully",
                "filename": "report.pdf",
                "preview_url": "https://cdn.example.com/previews/report.pdf",
                "category": "documents",
            }
        }


class FileInfo(BaseModel):
    filename: str
    preview_url: HttpUrl

    class Config:
        json_schema_extra = {
            "example": {
                "filename": "image.png",
                "preview_url": "https://cdn.example.com/previews/image.png",
            }
        }


class FileListResponse(BaseModel):
    files: list[FileInfo]

    class Config:
        json_schema_extra = {
            "example": {
                "files": [
                    {
                        "filename": "image.png",
                        "preview_url": "https://cdn.example.com/previews/image.png",
                    },
                    {
                        "filename": "report.pdf",
                        "preview_url": "https://cdn.example.com/previews/report.pdf",
                    },
                ]
            }
        }
