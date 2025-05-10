from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PERMIT_API_KEY: str
    PERMIT_PROJECT_ID: str
    MONGO_URI: str
    MONGO_DB_NAME: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()
