# Tests/test_booking_processor.py
import unittest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from Models.booking import Booking
from Models.campsite import Campsite
from Utils.booking_processor import process_bookings

class TestBookingProcessor(unittest.TestCase):
    def setUp(self):
        self.bookings = [Booking(booking_id=1, customer_id=101, booking_date="2024-09-01", 
                                 arrival_date="2024-09-07", campsite_size='Medium', num_campsites=1)]
        self.campsites = [Campsite(site_number=1, size='Medium', rate_per_night=60)]
        self.head_office_conn = MagicMock()
        self.cosmos_conn = MagicMock()

    def test_process_bookings_success(self):
        process_bookings(self.bookings, self.campsites, self.head_office_conn, self.cosmos_conn, campground_id=1121132)
        self.assertEqual(self.bookings[0].campsite_id, 1, "Campsite should be allocated.")
        self.head_office_conn.cursor().execute.assert_called()  # Ensure SQL update was called

    def test_process_bookings_no_campsites(self):
        # Use datetime objects for start and end dates
        start_date = datetime(2024, 9, 7)
        end_date = start_date + timedelta(days=7)
        self.campsites[0].book_campsite(start_date, end_date)  # Pre-book campsite to make it unavailable
        process_bookings(self.bookings, self.campsites, self.head_office_conn, self.cosmos_conn, campground_id=1121132)
        self.assertIsNone(self.bookings[0].campsite_id, "Campsite should not be allocated if unavailable.")

if __name__ == "__main__":
    unittest.main()
