from .redis_storage import get_redis_connection


def get_set_test():
    """set value in Redis and retrieve it"""
    con = get_redis_connection()
    con.set("ping", "pong")
    assert con.get("ping") == "pong"
