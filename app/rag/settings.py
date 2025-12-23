from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: str | None = None
    openai_model: str = "gpt-5"
    openai_embedding_model: str = "text-embedding-3-small"

    chunk_size: int = 800
    chunk_overlap: int = 120

    pinecone_api_key: str | None = None
    pinecone_index: str = "rag-demo"
    pinecone_namespace: str = "default"
    pinecone_cloud: str = "aws"
    pinecone_region: str = "us-east-1"

    # derived
    @property
    def mode(self) -> str:
        return "openai" if self.openai_api_key else "mock"

settings = Settings()  # singleton
