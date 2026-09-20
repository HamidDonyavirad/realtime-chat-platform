from pydantic_settings import SettingsConfigDict,BaseSettings


class Settings(BaseSettings):
    database_url: str
    database_test_url: str

    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding = "utf-8",
        extra = "ignore",
    )
