import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = ""
    # get hash by running `openssl rand -hex 32`
    SECRET_KEY: str = "5f1bfbc76c92fe8e7d0e9d683e697149807a65732316b9719ecd4529a26fa318"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"


settings = Settings()