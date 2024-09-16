import unittest
import os
from Utils.pdf_generator import PDFGenerator  # Import the PDFGenerator class correctly
from Models.booking import Booking

class TestPDFGeneration(unittest.TestCase):
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
        self.output_dir = "pdfs"  # Ensure this matches where PDFs are saved
        self.pdf_generator = PDFGenerator("Booking Confirmation")  # Initialize PDFGenerator with a title
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def test_generate_confirmation_pdf(self):
        filename = os.path.join(self.output_dir, f"confirmation_{self.booking.booking_id}.pdf")
        self.pdf_generator.generate_confirmation(self.booking)  # Use the correct method from PDFGenerator
        self.assertTrue(os.path.exists(filename), "Confirmation PDF should be created.")

    def tearDown(self):
        filename = os.path.join(self.output_dir, f"confirmation_{self.booking.booking_id}.pdf")
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    unittest.main()
