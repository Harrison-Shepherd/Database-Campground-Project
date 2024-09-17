# Tests/test_app.py
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Ensure the app's directory is added to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the Flask app from the correct file
from Front_End.app import app  # Adjust this path according to the location of your app.py file

class TestApp(unittest.TestCase):
    # Set up the Flask test client
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('Front_End.app.connect_to_cosmos')
    @patch('Front_End.app.fetch_cosmos_bookings')
    def test_index(self, mock_fetch_cosmos_bookings, mock_connect_to_cosmos):
        # Mock the Cosmos DB connection and fetching of bookings
        mock_connect_to_cosmos.return_value = MagicMock()
        mock_fetch_cosmos_bookings.return_value = []

        # Make a GET request to the index route
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No bookings available.', response.data)

    @patch('Front_End.app.connect_to_sql')
    @patch('Front_End.app.connect_to_head_office')
    @patch('Front_End.app.connect_to_cosmos')
    @patch('Front_End.app.fetch_bookings')
    @patch('Front_End.app.process_bookings')
    def test_process_bookings_route(self, mock_process_bookings, mock_fetch_bookings, 
                                    mock_connect_to_cosmos, mock_connect_to_head_office, 
                                    mock_connect_to_sql):
        # Mock database connections and data processing
        mock_connect_to_sql.return_value = MagicMock()
        mock_connect_to_head_office.return_value = MagicMock()
        mock_connect_to_cosmos.return_value = MagicMock()
        mock_fetch_bookings.return_value = []

        # Make a POST request to the process_bookings route
        response = self.app.post('/process_bookings', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Summary generated and stored successfully!', response.data)

    @patch('Front_End.app.connect_to_cosmos')
    @patch('Front_End.app.fetch_cosmos_bookings')
    def test_view_bookings(self, mock_fetch_cosmos_bookings, mock_connect_to_cosmos):
        # Mock the fetching of bookings from Cosmos DB
        mock_connect_to_cosmos.return_value = MagicMock()
        mock_fetch_cosmos_bookings.return_value = [{'booking_id': 1, 'customer_name': 'John Doe'}]

        # Make a GET request to the bookings route
        response = self.app.get('/bookings', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Doe', response.data)

    @patch('Front_End.app.connect_to_cosmos')
    @patch('Front_End.app.create_and_insert_summary')
    @patch('Front_End.app.generate_summary')
    @patch('Front_End.app.display_summary')
    def test_summary(self, mock_display_summary, mock_generate_summary, 
                     mock_create_and_insert_summary, mock_connect_to_cosmos):
        # Mock the summary generation and insertion
        mock_connect_to_cosmos.return_value = MagicMock()
        mock_generate_summary.return_value = {'total_sales': 100, 'total_bookings': 1}
        mock_display_summary.return_value = None
        mock_create_and_insert_summary.return_value = None

        # Make a GET request to the summary route
        response = self.app.get('/summary', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Summary generated and stored successfully!', response.data)

    @patch('Front_End.app.connect_to_cosmos')
    @patch('Front_End.app.fetch_pdf_from_cosmos')
    def test_show_pdf(self, mock_fetch_pdf_from_cosmos, mock_connect_to_cosmos):
        # Mock fetching PDF data from Cosmos DB
        mock_connect_to_cosmos.return_value = MagicMock()
        mock_fetch_pdf_from_cosmos.return_value = b'%PDF-1.4...'

        # Make a GET request to the PDF route
        response = self.app.get('/pdf/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/pdf')

if __name__ == "__main__":
    unittest.main()
