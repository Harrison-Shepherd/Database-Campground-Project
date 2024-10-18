import logging
import os

# Ensure the Logs directory exists
log_dir = os.path.join(os.path.dirname(__file__), '..', 'Logs')
os.makedirs(log_dir, exist_ok=True)

# Define the log file path in the Logs directory
log_file_path = os.path.join(log_dir, 'Campground.log')

# Create a file handler that logs INFO level and above
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)  # Logs messages at INFO level and above to the file
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  # Define log message format
file_handler.setFormatter(file_formatter)  # Set the format for the file handler

# Create a stream handler that logs WARNING level and above
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)  # Logs WARNING and above to the console
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  # Define format for console output
console_handler.setFormatter(console_formatter)  # Set the format for the console handler

# Configure the logging system with basic settings
logging.basicConfig(
    level=logging.INFO,  # Overall logging level, capturing INFO and above unless overridden by handlers
    handlers=[file_handler, console_handler]  # Attach the file and console handlers to the logging system
)

# Create a logger instance for use throughout the application
logger = logging.getLogger(__name__)

# Suppress detailed logs from specific libraries, especially HTTP logs from Azure SDK
# These settings reduce log verbosity from external libraries
logging.getLogger('azure.core.pipeline.policies.http_logging_policy').setLevel(logging.WARNING)
logging.getLogger('azure.cosmos').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)
