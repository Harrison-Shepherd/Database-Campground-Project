# Tests/test_main.py
import unittest
from unittest.mock import patch, MagicMock
import main  # Replace with your actual main module name if different

class TestMainFlow(unittest.TestCase):
    @patch('main.connect_to_sql')
    @patch('main.connect_to_head_office')
    @patch('main.connect_to_cosmos')
    @patch('main.fetch_bookings')
    def test_main_flow(self, mock_fetch_bookings, mock_connect_to_cosmos, mock_connect_to_head_office, mock_connect_to_sql):
        mock_connect_to_sql.return_value = MagicMock()
        mock_connect_to_head_office.return_value = MagicMock()
        mock_connect_to_cosmos.return_value = MagicMock()
        mock_fetch_bookings.return_value = []

        main.main()  # Call the main function

        # Ensure connections and fetch methods are called
        mock_connect_to_sql.assert_called_once()
        mock_connect_to_head_office.assert_called_once()
        mock_connect_to_cosmos.assert_called_once()
        mock_fetch_bookings.assert_called_once()

if __name__ == "__main__":
    unittest.main()
