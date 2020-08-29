import logging
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from opencensus.ext.azure.log_exporter import AzureLogHandler
from config.config import settings

logger = logging.getLogger(__name__)
print("Logging to ai: " + settings.ai_instrumentation_key)
logger.addHandler(AzureLogHandler(connection_string='InstrumentationKey='+settings.ai_instrumentation_key))
logger.setLevel(logging.INFO)


def store_delete_file(filepath, blob_name):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(settings.blob_conn_string)
        blob_client = blob_service_client.get_blob_client(container=settings.blob_container_name, blob=blob_name)
        with open(filepath, "rb") as data:
            blob_client.upload_blob(data)
        return settings.blob_public_url + blob_name
    except Exception as ex:
        logger.exception(ex)
        return
