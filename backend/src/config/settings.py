from pydantic import AnyHttpUrl, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


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

    # keys
    HUGGINGFACE_KEY: SecretStr
    LLM_KEY: SecretStr
    PINECONE_KEY: SecretStr
    SUPABASE_KEY: SecretStr

    # URLs
    CHAT_COMPLETIONS_URL: AnyHttpUrl
    FRONTEND_URL: AnyHttpUrl
    MULTILINGUAL_E5_EMBEDDER_URL: AnyHttpUrl
    MULTILINGUAL_MINILM_L12_CLASSIFICATION_URL: AnyHttpUrl
    SUPABASE_URL: AnyHttpUrl

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @property
    def huggingface_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.HUGGINGFACE_KEY.get_secret_value()}"}


settings = Settings()
