# Tests/test_flask_app.py

import unittest
from flask import Flask
from Front_End.app import app

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        """Set up test client for Flask app."""
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        """Test the index route."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bookings Overview', response.data)

    def test_booking_details_route(self):
        """Test the booking details route."""
        response = self.app.get('/booking/1')
        self.assertEqual(response.status_code, 200)

    def test_summary_route(self):
        """Test the summary route."""
        response = self.app.get('/summary')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Daily Summary', response.data)

if __name__ == '__main__':
    unittest.main()
