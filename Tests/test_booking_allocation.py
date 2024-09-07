# Tests/test_booking_allocation.py

import unittest
from datetime import datetime, timedelta
from Models.campsite import Campsite

class TestCampsite(unittest.TestCase):
    def setUp(self):
        self.campsite = Campsite(1, "Large", 70)

    def test_campsite_availability(self):
        start_date = datetime(2024, 9, 7)
        end_date = datetime(2024, 9, 14)
        self.assertTrue(self.campsite.is_available(start_date, end_date))
        self.campsite.book(start_date, end_date)
        self.assertFalse(self.campsite.is_available(start_date, end_date))

if __name__ == "__main__":
    unittest.main()
