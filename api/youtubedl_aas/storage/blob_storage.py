import logging
from azure.storage.blob import BlobServiceClient
from opencensus.ext.azure.log_exporter import AzureLogHandler
from youtubedl_aas.config import AI_INSTRUMENTATION_KEY, BLOB_CONN_STRING, BLOB_CONTAINER_NAME, BLOB_PUBLIC_URL

logger = logging.getLogger(__name__)
print("Logging to ai: " + AI_INSTRUMENTATION_KEY)
logger.addHandler(
    AzureLogHandler(
        connection_string="InstrumentationKey=" + AI_INSTRUMENTATION_KEY
    )
)
logger.setLevel(logging.INFO)


def store_delete_file(filepath, blob_name):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(
            BLOB_CONN_STRING
        )
        blob_client = blob_service_client.get_blob_client(
            container=BLOB_CONTAINER_NAME, blob=blob_name
        )
        with open(filepath, "rb") as data:
            blob_client.upload_blob(data)
        return BLOB_PUBLIC_URL + blob_name
    except Exception as ex:
        logger.exception(ex)
        return
