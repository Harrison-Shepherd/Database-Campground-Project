import unittest
from Database.sql_db import connect_to_sql

class TestSQLDatabase(unittest.TestCase):
    """
    Test class for testing the SQL database connection.

    This class ensures that the connection to the SQL database is established successfully
    and that the connection object returned is not None.
    """


    def test_connect_to_sql(self):
        """
        Test the connection to the SQL database.

        This test checks that the `connect_to_sql` function successfully connects to the SQL database
        and returns a valid connection object. It also ensures the connection is closed after testing.
        """
        # Attempt to connect to the SQL database
        conn = connect_to_sql()
        # Assert that the connection object is not None, indicating a successful connection
        self.assertIsNotNone(conn, "Failed to connect to the SQL database.")
        # Close the connection to clean up after the test
        conn.close()

if __name__ == "__main__":
    unittest.main()
