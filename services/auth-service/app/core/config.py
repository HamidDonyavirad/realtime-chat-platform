from pydantic_settings import BaseSettings, settingsConfigDict

class Settings(BaseSettings):
    database_url: str

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"

    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    model_config = settingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra = "ignore",
    )

settings = Settings()