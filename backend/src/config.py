from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True
    SECRET_KEY: str
    ACCES_TOKEN_EXPIRES_MINUTES: int
    REFRESH_TOKEN_EXPIRES_HOURS: int
    ALGORITHM: str

    USE_DB: bool = False
    DB_USER: str = None
    DB_PASSWORD: str = None
    DB_NAME: str = None

class ProductionSettings(Settings):
    pass

class DevSettings(Settings):
    pass


base_settings = Settings()
settings = DevSettings() if base_settings.DEBUG else ProductionSettings()
