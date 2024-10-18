import unittest
from Database.head_office_db import connect_to_head_office

# Define a test class for the Head Office SQL database connection
class TestHeadOfficeDatabase(unittest.TestCase):
    """
    Test class for testing the Head Office SQL database connection.

    This class ensures that the connection to the Head Office SQL database is established successfully
    and that the connection object returned is not None.
    """

    # Test the connection to the Head Office SQL database
    def test_connect_to_head_office(self):
        """
        Test the connection to the Head Office SQL database.

        This test checks that the `connect_to_head_office` function successfully connects to the Head Office SQL database
        and returns a valid connection object. It also ensures the connection is closed after testing.
        """
        # Attempt to connect to the Head Office SQL database
        conn = connect_to_head_office()
        # Assert that the connection object is not None, indicating a successful connection
        self.assertIsNotNone(conn, "Failed to connect to the Head Office SQL database.")
        # Close the connection to clean up after the test
        if conn:
            conn.close()

if __name__ == "__main__":
    unittest.main()
