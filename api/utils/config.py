from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    MODELS_DIR: Path = Path("models")
    MODEL_NAME: str = "gemma-2-2b-it-Q4_K_M.gguf"
    MODEL_DOWNLOAD_URL: str = "https://huggingface.co/bartowski/gemma-2-2b-it-GGUF/resolve/main/gemma-2-2b-it-Q4_K_M.gguf"
    MODEL_N_CTX: int = 32768
    MODEL_N_THREADS: int = 8
    MODEL_MAXTOKEN: int = 2048
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int  = 6379




    @property
    def MODEL_PATH(self) -> Path:
        return self.MODELS_DIR / self.MODEL_NAME


@lru_cache()
def get_settings():
    settings = Settings()
    return settings