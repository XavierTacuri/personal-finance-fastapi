from pydantic_settings import BaseSettings,SettingsConfigDict




class Settings(BaseSettings):

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file = ".env",
        extra = "ignore"
        )

    DATABASE_URL:  str


settings = Settings()