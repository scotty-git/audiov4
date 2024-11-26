from pydantic import PostgresDsn, SecretStr, AnyUrl, computed_field, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional, Literal

class Settings(BaseSettings):
    # Project Settings
    PROJECT_NAME: str = Field(..., env="PROJECT_NAME")  # Add PROJECT_NAME to the settings configuration
    ENVIRONMENT: Literal["development", "production", "testing"] = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"

    # Supabase Configuration
    SUPABASE_URL: AnyUrl
    SUPABASE_SERVICE_ROLE_KEY: SecretStr
    SUPABASE_ANON_KEY: SecretStr

    # OpenAI Configuration
    OPENAI_API_KEY: SecretStr

    # Database Configuration
    DATABASE_URL: PostgresDsn

    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Security Settings
    SECRET_KEY: SecretStr
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Computed Fields
    @computed_field
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    # Configuration for environment variable loading
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignore extra environment variables
        case_sensitive=False  # Allow case-insensitive env var names
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Additional validation or setup can be done here
        if self.DEBUG and self.is_production:
            raise ValueError("Debug mode should not be enabled in production!")

# Create a singleton settings instance
settings = Settings()
