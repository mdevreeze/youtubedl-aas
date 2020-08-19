from pydantic import BaseSettings

class Settings(BaseSettings):
    redis_key: str = ""
    ai_instrumentation_key: str = ""


settings = Settings()
