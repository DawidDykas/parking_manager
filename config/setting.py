from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path



class DatabaseSettings(BaseSettings):
    url_database: str 

    model_config = SettingsConfigDict(
        env_file = Path(__file__).resolve().parent / ".env",
        case_sensitive=False,
        extra="ignore" 
    )

class SecuritySettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_DAYS: int

    model_config = SettingsConfigDict(
        env_file = Path(__file__).resolve().parent / ".env",
        case_sensitive=False,
        extra="ignore" 
    )

class CelerySetting(BaseSettings): 
    URL_BROKER: str

    # EMAIL_BACKEND: str
    # EMAIL_PORT: int
    # EMAIL_USE_TLS: bool
    # EMAIL_HOST_USER: str
    # EMAIL_HOST_PASSWORD: str


    model_config = SettingsConfigDict(
        env_file = Path(__file__).resolve().parent / ".env",
        case_sensitive=False,
        extra="ignore" 
    )



# print(Path(__file__).resolve().parent / ".env")


database_settings = DatabaseSettings()
security_settings = SecuritySettings()
celery_settings = CelerySetting() 
