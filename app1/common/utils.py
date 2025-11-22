import logfire
from pydantic import BaseModel
import config

logging_initialized=False

def _initialize_logging():
    global logging_initialized
    if config.GOOGLE_CLOUD_LOGGING_ENABLED:
        import google.cloud.logging
        client = google.cloud.logging.Client()
        client.setup_logging()
    else:
        logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging_initialized=True