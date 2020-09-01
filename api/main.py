import uvicorn
from opencensus.ext.azure.log_exporter import AzureLogHandler
from youtubedl_aas.app import app, logger
from youtubedl_aas.config import AI_INSTRUMENTATION_KEY


print(AI_INSTRUMENTATION_KEY)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
else:
    logger.addHandler(
        AzureLogHandler(
            connection_string="InstrumentationKey=" + AI_INSTRUMENTATION_KEY
        )
    )
