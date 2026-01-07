from typing import List

from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str

    class Config:
        json_schema_extra = {
            "example": {
                "question": "I just encountered error 404, what should I do?",
            }
        }


class CategoryMeta(BaseModel):
    category: str

    class Config:
        json_schema_extra = {
            "example": {
                "category": "tech_support",
            }
        }


class ChunkMetadata(BaseModel):
    text: str
    source: str
    category: str
    entities: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Explanation of 404 error",
                "source": "tech_support.csv",
                "category": "tech",
                "entities": ["404 error", "URL"],
            }
        }


class QueryResponse(BaseModel):
    answer: str
    chunks: List[ChunkMetadata]

    class Config:
        json_schema_extra = {
            "example": {
                "answer": "A 404 error means the page could not be found...",
                "chunks": [
                    {
                        "text": "Explanation of 404 error",
                        "source": "tech_support.csv",
                        "category": "tech",
                        "entities": ["404 error", "URL"],
                    }
                ],
            }
        }
