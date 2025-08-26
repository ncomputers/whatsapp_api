from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    bind: str = "0.0.0.0"
    port: int = 8000
    basic_user: str = "admin"
    basic_pass: str = "admin"
    user_data_dir: str = "./.mw_profile"
    headless: bool = False
    webhook_url: str | None = None
    rate_limit: str = "30/minute"

    model_config = SettingsConfigDict(env_prefix="MW_", case_sensitive=False)


settings = Settings()
