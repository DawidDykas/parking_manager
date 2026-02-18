from pydantic_settings import BaseSettings, SettingsConfigDict
import os 


class DatabaseSettings(BaseSettings):
    url_database_user: str 
    url_database_products: str 

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.getcwd(),"config/.env"),
        case_sensitive=False,
        extra="ignore" 
    )

class SecuritySettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_DAYS: int

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.getcwd(),"config/.env"),
        case_sensitive=False,
        extra="ignore" 
    )



database_settings = DatabaseSettings()
security_settings = SecuritySettings()