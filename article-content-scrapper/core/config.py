import os.path

from pydantic_settings import BaseSettings
from pydantic import Extra
from typing import Optional


class Settings(BaseSettings):
    # APP Properties
    PROJECT_NAME: str = "Article Extractor"
    VERSION: str = "1.0.0"
    STAGE: str = 'DEV'
    SPOKESPERSON_ROOT_DIRECTORY: str
    SPOKESPERSON_FAILED_ARTICLE_DIRECTORY: str = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                              'failed_articles')
    SELENIUM_FRAMEWORK: str = 'selenium'
    SUPPORTED_FRAMEWORKS: str

    # DB Properties
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # Rabbit Properties
    MQ_HOST: str
    MQ_PORT: int
    MQ_USER: str
    MQ_PASSWORD: str
    DELIVERY_MODE: int
    RETRY_DELAY: int
    MQ_CONNECTION_ATTEMPT: int
    MQ_VIRTUAL_HOST: str
    SPOKESPERSON_ARTICLE_METADATA_QUEUE: str
    SPOKESPERSON_ARTICLE_METADATA_ROUTING_KEY: str
    SPOKESPERSON_ARTICLE_EXCHANGE: str
    SPOKESPERSON_ARTICLE_CONTENT_QUEUE: str
    SPOKESPERSON_ARTICLE_CONTENT_ROUTING_KEY: str
    SPOKESPERSON_ARTICLE_FAIL_EXCHANGE: str
    SPOKESPERSON_ARTICLE_METADATA_FAIL_ROUTING_KEY: str

    # SMTP Properties
    SMTP_HOST: str
    SMTP_PORT: int
    SENDER_EMAIL: str
    DEV_RECIPIENT_EMAILS: str
    UPDATE_RECIPIENT_EMAILS: str
    EMAIL_ALERT_LEVEL: str

    # Automation Tool Properties
    HEADLESS: bool
    PROXY: bool
    USER_AGENT: str
    BROWSER: str
    BROWSER_VERSION: str
    WINDOW_SIZE: str
    PAGE_LOAD_TIMEOUT: int
    SCRIPT_TIMEOUT: int
    IMPLICIT_WAIT: int
    EXPLICIT_WAIT: int
    # Optionally enable or disable screenshots on failure.
    TAKE_SCREENSHOTS: bool
    FAILED_CRAWL_SOURCE_DIR: str
    PROXIES: str
    PROXY_ENABLED: bool

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
data_source: Settings = create_instance()
