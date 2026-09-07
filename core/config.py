from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    REDIS_URL: str
    TESTING: bool = False


settings = Settings()
