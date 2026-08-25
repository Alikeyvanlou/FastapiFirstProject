from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    database_name: str
    secret_key: str
    algorithm : str
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env"
    )

    @property
    def database_url(self) -> str:
        return f"sqlite:///{BASE_DIR /'database'/ self.database_name}"


settings = Settings()