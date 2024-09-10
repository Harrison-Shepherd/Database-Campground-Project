# Tests/test_error_handling.py
import unittest
import os
import logging
import time
from Utils.error_handler import handle_error

class TestErrorHandler(unittest.TestCase):
    def setUp(self):
        # Path to the log file
        self.log_file = 'error.log'
        
        # Close and remove existing handlers to avoid file locking issues
        logging.shutdown()  # Ensure all logging is shut down completely
        for handler in logging.root.handlers[:]:
            handler.close()
            logging.root.removeHandler(handler)

        # Attempt to remove the log file safely
        if os.path.exists(self.log_file):
            try:
                os.remove(self.log_file)
            except PermissionError:
                # If the file is in use, wait briefly and retry
                time.sleep(0.1)  # Short delay
                os.remove(self.log_file)

        # Reconfigure the logger for this test specifically
        logging.basicConfig(
            level=logging.ERROR,
            filename=self.log_file,
            filemode='a',  # Use 'a' to append and ensure the file is created if it doesn't exist
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def test_handle_error(self):
        try:
            # Intentionally raise an error to test logging
            raise ValueError("Test Error")
        except Exception as e:
            # Use the error handler function to log the error
            handle_error(e)

            # Force shutdown logging to ensure logs are written and file locks are released
            logging.shutdown()

            # Verify that the log file exists
            self.assertTrue(os.path.exists(self.log_file), "Log file was not created.")

            # Read the log file to check if the error message is logged correctly
            with open(self.log_file, 'r') as file:
                logs = file.read()

            # Check if the expected error message is present in the logs
            self.assertIn("Test Error", logs)

    def tearDown(self):
        # Clean up and remove handlers after the test
        logging.shutdown()  # Shutdown logging to ensure all handlers are closed
        for handler in logging.root.handlers[:]:
            handler.close()
            logging.root.removeHandler(handler)

        # Optionally remove the log file if needed for cleanup
        if os.path.exists(self.log_file):
            try:
                os.remove(self.log_file)
            except PermissionError:
                time.sleep(0.1)  # Wait before retrying to delete the file
                os.remove(self.log_file)

if __name__ == "__main__":
    unittest.main()
