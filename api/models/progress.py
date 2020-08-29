from uuid import UUID
from datetime import datetime
import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Progress(BaseModel):
    """Keeps the progress information of a download/conversion"""
    uuid: UUID
    status: str
    filename: str = None
    stopdate: datetime = None
    gif_filename: str = None
    current: int = None
    total: int = None
    last_update: datetime = None
    mp4_url: str = None
    gif_url: str = None

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
