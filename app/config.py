from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "PawHealth API"
    db_mode: str = "sqlite"
    database_url: str = "sqlite:///./paw_health.db"
    jwt_secret: str = "pawhealth-super-secret-key-change-in-production-32b"

    class Config:
        env_file = ".env"

settings = Settings()
