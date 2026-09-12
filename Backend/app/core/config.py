from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ORCHESTRATOR_URL: str = "http://127.0.0.1:8000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
