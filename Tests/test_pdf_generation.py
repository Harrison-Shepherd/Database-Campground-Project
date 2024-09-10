# Tests/test_pdf_generation.py
import unittest
import os
from Utils.confirmation import generate_confirmation
from Models.booking import Booking

class TestPDFGeneration(unittest.TestCase):
    def setUp(self):
        self.booking = Booking(
            booking_id=1, customer_id=101, booking_date="2024-09-01", 
            arrival_date="2024-09-07", campsite_size='Medium', num_campsites=1
        )
        self.confirmation_path = f"confirmation_pdfs/confirmation_{self.booking.booking_id}.pdf"

    def test_generate_confirmation_pdf(self):
        generate_confirmation(self.booking)
        self.assertTrue(os.path.exists(self.confirmation_path), "Confirmation PDF should be created.")

    def tearDown(self):
        # Cleanup generated PDFs after the test
        if os.path.exists(self.confirmation_path):
            os.remove(self.confirmation_path)

if __name__ == "__main__":
    unittest.main()
