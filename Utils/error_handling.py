#Utils/error_handling.py
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, filename='error.log')

def handle_error(exception):
    """
    Handles exceptions by logging them.
    """
    logging.error(f"An error occurred: {exception}")
    print(f"An error occurred: {exception}")
