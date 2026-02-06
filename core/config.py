from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / '.env'),
        env_file_encoding='utf-8',
        extra='ignore'
    )

    DATABASE_URL: str

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    REFRESH_TOKEN_EXPIRE_DAYS: int = 1

    CORS_ORIGINS: str = "*"

    def cors_list(self) -> list[str]:
        v = (self.CORS_ORIGINS or "*").strip()
        if v == "*":
            return ["*"]
        return [x.strip() for x in v.split(",") if x.strip()]


settings = Settings()
