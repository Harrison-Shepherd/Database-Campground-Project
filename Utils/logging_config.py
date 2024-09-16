import logging
import os

# Define the log file path
log_file_path = os.path.join(os.path.dirname(__file__), '..', 'app.log')

# Create a file handler that logs INFO level and above
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Create a stream handler that logs WARNING level and above
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)  # Only show WARNING and above in the console
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# Configure the logging
logging.basicConfig(
    level=logging.INFO,  # Set to INFO for routine events, but control handlers separately
    handlers=[file_handler, console_handler]
)

# Create a logger instance
logger = logging.getLogger(__name__)

# Suppress detailed logs from specific libraries, especially HTTP logs from Azure SDK
logging.getLogger('azure.core.pipeline.policies.http_logging_policy').setLevel(logging.WARNING)
logging.getLogger('azure.cosmos').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)
