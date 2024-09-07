# Tests/test_campsite.py

import unittest
from datetime import datetime, timedelta
from Models.campsite import Campsite

class TestCampsite(unittest.TestCase):
    def setUp(self):
        # Set up a campsite for testing
        self.campsite = Campsite(1, "Large", 70)

    def test_campsite_availability(self):
        # Test if the campsite is available before booking
        start_date = datetime(2024, 9, 7)
        end_date = datetime(2024, 9, 14)
        self.assertTrue(self.campsite.is_available(start_date, end_date))
        
        # Book the campsite and check availability again
        self.campsite.book(start_date, end_date)
        self.assertFalse(self.campsite.is_available(start_date, end_date))

if __name__ == "__main__":
    unittest.main()
