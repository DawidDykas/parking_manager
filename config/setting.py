from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class DatabaseSettings(BaseSettings):
    url_database: str 

    model_config = SettingsConfigDict(
        env_file = Path(__file__).resolve / "config" / ".env",
        case_sensitive=False,
        extra="ignore" 
    )

class SecuritySettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_DAYS: int

    model_config = SettingsConfigDict(
        env_file = Path(__file__).resolve / "config" / ".env",
        case_sensitive=False,
        extra="ignore" 
    )



database_settings = DatabaseSettings()
security_settings = SecuritySettings()