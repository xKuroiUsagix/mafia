from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ACCES_TOKEN_EXPIRES_MINUTES: int
    ALGORITHM: str

settings = Settings()
