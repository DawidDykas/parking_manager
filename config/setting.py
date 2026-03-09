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



class FastAPISettings(BaseSettings):
    PORT : int = 8000
    HOST : str = "127.0.0.1"

    model_config = SettingsConfigDict(
        env_file = Path(__file__).resolve().parent / ".env",
        case_sensitive=False,
        extra="ignore" 
    )


database_settings = DatabaseSettings()
fastapi_settings = FastAPISettings()
security_settings = SecuritySettings()
celery_settings = CelerySetting() 
