import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GOOGLE_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"
    NEWSAPI_KEY: str = ""
    SERPAPI_KEY: str = ""
    POLYGON_API_KEY: str = ""          # Massive.com / Polygon.io API key
    FAISS_INDEX_PATH: str = "/tmp/faiss_index"
    MAX_AGENT_ITERATIONS: int = 8
    CORS_ORIGINS: str = "*"

    class Config:
        env_file = ".env"
        extra = "ignore"

    @property
    def cors_origins_list(self) -> list[str]:
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]


settings = Settings()
