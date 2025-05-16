from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ACCES_TOKEN_EXPIRES_MINUTES: int
    REFRESH_TOKEN_EXPIRES_HOURS: int
    ALGORITHM: str
    DEBUG: int = 1

class ProductionSettings(Settings):
    pass

class DevSettings(Settings):
    pass


base_settings = Settings()
settings = DevSettings() if base_settings.DEBUG else ProductionSettings()
