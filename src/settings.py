from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    MODEL: str = "llama3.1:8b"
    GALILEO_PROJECT: str = "onboarding"
    GALILEO_LOG_STREAM: str = "default"
    GALILEO_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = AppSettings()
