import os.path

from pydantic_settings import BaseSettings
from pydantic import Extra
from typing import Optional


class Settings(BaseSettings):
    # APP Properties
    PROJECT_NAME: str = "SPOKE API"
    VERSION: str = "1.0.0"

    # DB Properties
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_MIN_CONNECTION: int
    DB_MAX_CONNECTION: int

    # SMTP Properties
    SMTP_HOST: str
    SMTP_PORT: int
    SENDER_EMAIL: str
    RECIPIENT_EMAILS: str
    EMAIL_ALERT_LEVEL: str

    # Azure AD Properties
    AZURE_CLIENT_ID: str
    AZURE_CLIENT_SECRET: str
    AZURE_TENANT_ID: str
    REDIRECT_URI: str
    FRONTEND_URL: str

    class Config:
        env_file = ".env"
        extra = Extra.allow  # Allow extra fields


# Create a global setting instance
setting: Optional[Settings] = None


def create_instance() -> Settings:
    global setting
    if setting is None:
        setting = Settings()
    return setting


def reset_settings() -> None:
    global data_source
    data_source = Settings()  # Reinitialize to load new values from .env


# Initialize the setting
data_source = create_instance()
