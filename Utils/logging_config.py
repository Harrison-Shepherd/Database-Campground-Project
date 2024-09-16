# Utils/logging_config.py
import logging
import os

# Define the log file path
log_file_path = os.path.join(os.path.dirname(__file__), '..', 'app.log')

# Configure the logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),  # Log to file
        logging.StreamHandler()  # Optional: keep this line if you also want logs to appear in the console
    ]
)

# Example logger usage
logger = logging.getLogger(__name__)
