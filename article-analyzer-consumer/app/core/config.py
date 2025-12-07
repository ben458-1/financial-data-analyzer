from pydantic_settings import BaseSettings
from pydantic import Extra, Field
from typing import Optional
from typing import List


# APP CONFIG
class AppSettings(BaseSettings):
    PROJECT_NAME: str = "Article Analyzer"
    VERSION: str = "1.0.0"
    STAGE: str = "DEV"
    # IMPORTANT: Add your personal Google Gemini API key(s) in the .env file before running
    # Set API_KEYS as a comma-separated list for multiple keys (for quota management)
    # Example: API_KEYS=["key1", "key2", "key3"]
    API_KEYS: List[str]
    # Set API_KEY as the primary key to use
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


# PARSING MODEL CONFIG
class ParsingModelConfig(BaseSettings):
    MODEL_NAME: str
    MAX_OUTPUT_TOKENS: int
    TEMPERATURE: float
    TOP_P: float
    TOP_K: int
    CANDIDATE_COUNT: int

    class Config:
        env_file = ".env"
        env_prefix = 'PARSING_'
        extra = Extra.allow 

# VALIDATION MODEL CONFIG
class ValidationModelConfig(BaseSettings):
    MODEL_NAME: str
    TEMPERATURE: float
    TOP_P: float
    TOP_K: int
    # CANDIDATE_COUNT: int

    class Config:
        env_file = ".env"
        env_prefix = 'VALIDATION_'
        extra = Extra.allow



# RABBITMQ CONFIG
class RABBITMQSettings(BaseSettings):
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    SPOKESPERSON_ARTICLE_ANALYZER_QUEUE: str
    # DELIVERY_MODE: int
    # RETRY_DELAY: int
    # MQ_CONNECTION_ATTEMPT: int
    # MQ_VIRTUAL_HOST: str
    # SPOKESPERSON_ARTICLE_METADATA_QUEUE: str
    # SPOKESPERSON_ARTICLE_METADATA_ROUTING_KEY: str
    # SPOKESPERSON_ARTICLE_EXCHANGE: str
    # SPOKESPERSON_ARTICLE_CONTENT_QUEUE: str
    # SPOKESPERSON_ARTICLE_CONTENT_ROUTING_KEY: str
    # SPOKESPERSON_ARTICLE_FAIL_EXCHANGE: str
    # SPOKESPERSON_ARTICLE_METADATA_FAIL_ROUTING_KEY: str

    class Config:
        env_file = ".env"
        env_prefix = 'RABBITMQ_'
        extra = Extra.allow


# COMBINED CONFIG
class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    db: DBSettings = DBSettings()
    parsing: ParsingModelConfig = ParsingModelConfig()
    validation: ValidationModelConfig = ValidationModelConfig()
    rabbitmq: RABBITMQSettings = RABBITMQSettings()

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
