from pydantic import BaseModel, HttpUrl

class Video(BaseModel):
    """Post input for root call"""
    url: HttpUrl
    optimize: bool = True
    start_seconds: int = None
    stop_seconds: int = None
