from pydantic import BaseSettings

class Settings(BaseSettings):
    redis_key: str = ""
    ai_instrumentation_key: str = ""
    blob_conn_string: str = ""
    blob_container_name: str = ""
    blob_public_url: str = ""


settings = Settings()
