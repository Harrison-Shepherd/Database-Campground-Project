# Tests/test_campsite.py
import unittest
from datetime import datetime, timedelta
from Models.campsite import Campsite

class TestCampsite(unittest.TestCase):
    def setUp(self):
        self.campsite = Campsite(site_number=1, size='Medium', rate_per_night=60)

    def test_is_available(self):
        start_date = datetime(2024, 9, 7)
        end_date = start_date + timedelta(days=7)
        self.assertTrue(self.campsite.is_available(start_date, end_date), "Campsite should be available initially.")

    def test_book_campsite(self):
        start_date = datetime(2024, 9, 7)
        end_date = start_date + timedelta(days=7)
        self.assertTrue(self.campsite.book_campsite(start_date, end_date), "Campsite booking should succeed.")
        self.assertFalse(self.campsite.is_available(start_date, end_date), "Campsite should not be available after booking.")

if __name__ == "__main__":
    unittest.main()
