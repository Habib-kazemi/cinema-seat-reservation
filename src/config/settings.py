from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ENVIRONMENT: str = "development"

    web_concurrency: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "forbid"


settings = Settings()
