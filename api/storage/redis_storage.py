import redis
from models.progress import Progress
from config.config import settings


def get_redis_connection():
    r = redis.Redis(host="ydlaas.redis.cache.windows.net", port=6380, db=0,
                    password=settings.redis_key, ssl=True)
    return r


def get_status(identifier):
    con = get_redis_connection()
    status = Progress(uuid=identifier, status="Unknown")
    status = Progress.parse_raw(con.get("status:" + str(identifier)))
    return status


def set_status(progress: Progress):
    con = get_redis_connection()
    json_str = progress.json()
    con.set("status:" + str(progress.uuid), json_str, ex=36000)
