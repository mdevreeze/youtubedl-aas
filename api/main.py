import uvicorn
import sys
from opencensus.ext.azure.log_exporter import AzureLogHandler
from youtubedl_aas.app import app, logger
from youtubedl_aas.config import settings

print(sys.path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
else:
    logger.addHandler(
        AzureLogHandler(
            connection_string="InstrumentationKey=" + settings.ai_instrumentation_key
        )
    )
    print("Logging to ai: " + settings.ai_instrumentation_key)
