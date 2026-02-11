from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    url_database_user: str 
    url_database_products: str 

    model_config = SettingsConfigDict(
        env_file=".env"
    )

database_settings = DatabaseSettings()