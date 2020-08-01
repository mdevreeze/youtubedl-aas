import redis
from ..models.progress import Progress


def get_redis_connection():
    r = redis.Redis(host="ydlaas.redis.cache.windows.net", port=6380, db=0,
                    password="VpFXO0Jk599qhKM38goalkxmqV2BFwETUoZsKr23azk=", ssl=True)
    return r


def get_status(identifier):
    con = get_redis_connection()
    status = Progress(uuid=identifier, status="Unknown")
    status = Progress.parse_raw(con.get("status:" + str(identifier)))
    return status


def set_status(progress: Progress):
    con = get_redis_connection()
    json_str = progress.json()
    con.set("status:" + str(progress.uuid), json_str)
