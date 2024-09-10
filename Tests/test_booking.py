# Tests/test_booking.py
import unittest
from datetime import datetime, timedelta
from Models.booking import Booking
from Models.campsite import Campsite, allocate_campsite

class TestBooking(unittest.TestCase):
    def setUp(self):
        self.booking = Booking(
            booking_id=1,
            customer_id=101,
            booking_date="2024-09-01",
            arrival_date="2024-09-07",
            campground_id=1121132,
            campsite_size='Medium',
            num_campsites=1
        )
        self.campsites = [
            Campsite(site_number=1, size='Medium', rate_per_night=60),
            Campsite(site_number=2, size='Large', rate_per_night=70)
        ]

    def test_booking_creation(self):
        self.assertEqual(self.booking.booking_id, 1)
        self.assertEqual(self.booking.customer_id, 101)
        self.assertEqual(self.booking.campsite_size, 'Medium')
        self.assertEqual(self.booking.num_campsites, 1)

    def test_validate_date(self):
        self.assertEqual(self.booking.arrival_date, datetime(2024, 9, 7))

    def test_allocate_campsite(self):
        start_date = datetime(2024, 9, 7)
        end_date = start_date + timedelta(days=7)
        allocated_campsite = allocate_campsite(self.campsites, start_date, end_date, self.booking)
        self.assertIsNotNone(allocated_campsite)
        self.assertEqual(allocated_campsite.site_number, 1)

if __name__ == "__main__":
    unittest.main()
