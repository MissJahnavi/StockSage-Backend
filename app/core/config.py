import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GOOGLE_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash-preview-04-17"
    NEWSAPI_KEY: str = ""
    SERPAPI_KEY: str = ""
    POLYGON_API_KEY: str = ""          # Massive.com / Polygon.io API key
    FAISS_INDEX_PATH: str = "./data/faiss_index"
    MAX_AGENT_ITERATIONS: int = 8
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    class Config:
        env_file = ".env"
        extra = "ignore"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]


settings = Settings()
