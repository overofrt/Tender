import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str = "9054990690:AAFBF-X2vSb6gceA-u4rjLLELec4Mumioc8"
    DATABASE_URL: str = "sqlite+aiosqlite:///tenders.db"
    OPENAI_API_KEY: str = "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"
    ADMIN_CHAT_ID: int = 8703643195
    TIMEZONE: str = "Asia/Tbilisi"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
