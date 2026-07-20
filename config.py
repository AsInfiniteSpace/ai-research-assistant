from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    TAVILY_API_KEY: str

    MODEL_NAME: str
    EMBEDDING_MODEL: str
    

    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    HOST: str = "0.0.0.0"

    PORT: int = 8000

    DEBUG: bool = False

    ENVIRONMENT: str = "production"


settings = Settings()