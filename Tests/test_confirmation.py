# Tests/test_confirmation.py
import unittest
import os
from Utils.confirmation import generate_confirmation
from Models.booking import Booking

class TestConfirmation(unittest.TestCase):
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

    def test_generate_confirmation(self):
        generate_confirmation(self.booking)
        filename = f"confirmation_pdfs/confirmation_{self.booking.booking_id}.pdf"
        self.assertTrue(os.path.exists(filename))

if __name__ == "__main__":
    unittest.main()
