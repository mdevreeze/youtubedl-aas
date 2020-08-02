from pydantic import BaseSettings

class Settings(BaseSettings):
    redis_key: str = ""

settings = Settings()
