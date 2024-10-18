import unittest
from unittest.mock import patch, MagicMock
import main  

class TestMainFlow(unittest.TestCase):
    """
    Test class for testing the main flow of the application.

    This class mocks the key components of the main application, including database connections
    and data fetching methods, to ensure the main flow runs without actual dependencies.
    """

    @patch('main.connect_to_sql')
    @patch('main.connect_to_head_office')
    @patch('main.connect_to_cosmos')
    @patch('main.fetch_bookings')
    def test_main_flow(self, mock_fetch_bookings, mock_connect_to_cosmos, mock_connect_to_head_office, mock_connect_to_sql):
        """
        Test the main flow of the application by mocking database connections and fetching functions.

        This test ensures that the main function calls the expected methods and handles connections
        correctly without executing the actual logic inside these methods.
        """
        # Mock the return values of the connection and fetch functions
        mock_connect_to_sql.return_value = MagicMock()            # Mock SQL connection
        mock_connect_to_head_office.return_value = MagicMock()    # Mock Head Office connection
        mock_connect_to_cosmos.return_value = MagicMock()         # Mock Cosmos DB connection
        mock_fetch_bookings.return_value = []                     # Mock fetch_bookings to return an empty list

        # Call the main function to execute the flow with mocked components
        main.main()

        # Assert that the mocked functions were called exactly once during the main flow
        mock_connect_to_sql.assert_called_once()
        mock_connect_to_head_office.assert_called_once()
        mock_connect_to_cosmos.assert_called_once()
        mock_fetch_bookings.assert_called_once()

if __name__ == "__main__":
    unittest.main()
