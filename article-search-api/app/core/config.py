from pydantic_settings import BaseSettings
from pydantic import Extra, Field
from typing import Optional
from typing import List


# APP CONFIG
class AppSettings(BaseSettings):
    PROJECT_NAME: str = "Fetching Module"
    VERSION: str = "1.0.0"
    STAGE: str = "DEV"
    # IMPORTANT: Add your personal Google Gemini API key in the .env file before running this code
    # Example: API_KEY=your_gemini_api_key_here
    API_KEY: str
    
    class Config:
        env_file = ".env"
        extra = Extra.allow


# DATABASE CONFIG
class DBSettings(BaseSettings):
    HOST: str
    NAME: str
    USER: str
    PASSWORD: str
    PORT: int

    class Config:
        env_file = ".env"
        env_prefix = 'DB_'
        extra = Extra.allow


# COMBINED CONFIG
class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    db: DBSettings = DBSettings()

    class Config:
        extra = Extra.allow


settings: Optional[Settings] = None


def create_instance() -> Settings:
    global settings
    if settings is None:
        settings = Settings()
    return settings


def reset_settings() -> None:
    global settings
    settings = Settings()  

settings: Settings = create_instance()
