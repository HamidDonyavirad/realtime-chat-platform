from pydantic_settings import SettingsConfigDict,BaseSettings


class Settings(BaseSettings):
    database_url: str
    database_test_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"

    rabbitmq_url: str  = "amqp://guest:guest@localhost:5672/"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding = "utf-8",
        extra = "ignore",
    )


settings = Settings()