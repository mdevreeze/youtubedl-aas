from pydantic import BaseSettings

class Settings(BaseSettings):
    redis_key: str = "Nwec8ebiqoO1a5jAKyFtA56xr4h5RvPrGAtDiMc7jWU="
    ai_instrumentation_key: str = "dd79ec6c-5c40-4c9a-8131-dd1497db5c6d"
    blob_conn_string: str = "DefaultEndpointsProtocol=https;AccountName=youtubedlaasstorage;AccountKey=Gz4NzAnaQkV7k715F2wTjWzJ0nSsXZFSKNvipTMCCbE/qKKhqrEWvhp/LCb/no7A7BzY2SH/XRdBtwIC1wI+gA==;EndpointSuffix=core.windows.net"
    blob_container_name: str = "dl-media"
    blob_public_url: str = "https://youtubedlaasstorage.blob.core.windows.net/dl-media/"

settings = Settings()
