from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # constants
    BUCKET_NAME: str = "files"
    INDEX_NAME: str = "smart-support"
    SUPABASE_TABLE: str = "documents"

    # int
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 100
    DIMENSION: int = 1024
    TIMEOUT: int = 30

    # keys (required, no defaults)
    HUGGINGFACE_KEY: str
    LLM_KEY: str
    PINECONE_KEY: str
    SUPABASE_KEY: str

    # URLs
    CHAT_COMPLETIONS_URL: str
    MULTILINGUAL_E5_EMBEDDER_URL: str
    MULTILINGUAL_MINILM_L12_CLASSIFICATION_URL: str
    SUPABASE_URL: str

    class Config:
        env_file = ".env"  # automatically loads from .env
        env_file_encoding = "utf-8"


settings = Settings()
HEADERS = {"Authorization": f"Bearer {settings.HUGGINGFACE_KEY}"}
