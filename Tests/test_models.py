# Tests/test_models.py

import unittest
from Models.booking import Booking
from Models.campsite import Campsite

class TestBooking(unittest.TestCase):
    def test_booking_creation(self):
        booking = Booking(booking_id=1, customer_name="John Doe", campsite_size="Large")
        self.assertEqual(booking.customer_name, "John Doe")

    def test_campsite_availability(self):
        campsite = Campsite(site_number=1, size="Medium", rate=60)
        self.assertTrue(campsite.is_available("2024-09-07", "2024-09-14"))

if __name__ == "__main__":
    unittest.main()
