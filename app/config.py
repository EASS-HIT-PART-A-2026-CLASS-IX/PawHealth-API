from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "PawHealth API"
    db_mode: str = "sqlite" # options: memory | sqlite | postgres
    database_url_sqlite: str = "sqlite:///./data/pawhealth.db"
    database_url_postgres: str = "postgresql+psycopg://postgres:postgres@localhost:5432/pawhealth"
    database_echo: bool = False

    @property
    def database_url(self) -> str:
        if self.db_mode == "postgres":
            return self.database_url_postgres
        return self.database_url_sqlite

    model_config = SettingsConfigDict(env_prefix="PAW_", env_file=".env", extra="ignore")

settings = Settings()
