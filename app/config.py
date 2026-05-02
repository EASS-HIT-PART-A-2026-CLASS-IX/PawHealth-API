from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "PawHealth API"
    db_mode: str = "sqlite"
    database_url: str = "sqlite:///./paw_health.db"
    jwt_secret: str = "supersecret"

    class Config:
        env_file = ".env"

settings = Settings()
