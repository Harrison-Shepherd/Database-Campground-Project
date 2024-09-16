import logging
import os

# Define the log file path
log_file_path = os.path.join(os.path.dirname(__file__), '..', 'app.log')

# Configure the logging
logging.basicConfig(
    level=logging.INFO,  # Set to INFO for routine events, use DEBUG sparingly
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)

# Create a logger instance
logger = logging.getLogger(__name__)

# Suppress detailed logs from specific libraries, especially HTTP logs from Azure SDK
logging.getLogger('azure.core.pipeline.policies.http_logging_policy').setLevel(logging.WARNING)
logging.getLogger('azure.cosmos').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)
