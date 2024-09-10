# Utils/error_handler.py
import logging
import os

# Configure logging to ensure the file is created correctly
log_file = 'error.log'
# Remove any previous handlers associated with the root logger
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Setup logging with explicit file mode and path
logging.basicConfig(
    level=logging.ERROR,
    filename=log_file,
    filemode='a',  # Append mode
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def handle_error(exception):
    """
    Handles exceptions by logging them.
    """
    # Explicitly check if logger is configured and log the error
    logging.error(f"An error occurred: {exception}")
    print(f"An error occurred: {exception}")
