import os

from dotenv import load_dotenv
load_dotenv()

REDIS_KEY = os.getenv("REDIS_KEY", "")
AI_INSTRUMENTATION_KEY = os.getenv("AI_INSTRUMENTATION_KEY", "")
BLOB_CONN_STRING = os.getenv("BLOB_CONN_STRING", "")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME", "")
BLOB_PUBLIC_URL = os.getenv("BLOB_PUBLIC_URL", "")
