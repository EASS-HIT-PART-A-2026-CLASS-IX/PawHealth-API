from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "PawHealth PRO"
    # Database & Redis (Session 10)
    database_url: str = "sqlite:///./data/pawhealth.db"
    redis_url: str = "redis://redis:6379/0"
    
    # Security (EX3 Baseline - Session 11)
    jwt_secret: str = "super-secret-key-change-in-prod"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # AI Sidecar (Session 08)
    ai_sidecar_url: str = "http://sidecar:8001"
    google_api_key: str = "your-google-api-key"

    model_config = SettingsConfigDict(env_prefix="PAW_", env_file=".env", extra="ignore")

settings = Settings()
