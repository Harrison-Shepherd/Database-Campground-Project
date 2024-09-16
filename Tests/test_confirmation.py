import unittest
import os
from Utils.pdf_generator import PDFGenerator  # Ensure this is the correct import
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
        self.output_dir = "pdfs"  # Ensure this matches the directory used in PDFGenerator
        self.pdf_generator = PDFGenerator("Booking Confirmation")  # Initialize PDFGenerator with a title
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def test_generate_confirmation(self):
        # Expected filename path
        filename = os.path.join(self.output_dir, f"confirmation_{self.booking.booking_id}.pdf")

        # Remove the file if it already exists to ensure a clean test
        if os.path.exists(filename):
            os.remove(filename)

        # Call the PDF generation function
        generated_file = self.pdf_generator.generate_confirmation(self.booking)

        # Debugging output
        print(f"Expected PDF path: {filename}")
        print(f"Generated PDF path: {generated_file}")

        # Check if the expected file was generated
        self.assertTrue(os.path.exists(filename), f"Expected PDF file was not created: {filename}")

        # Additional assertion to verify the function returned the correct path
        self.assertEqual(generated_file, filename, f"The returned path {generated_file} does not match the expected path {filename}.")

    def tearDown(self):
        # Clean up by removing the generated file if it exists
        filename = os.path.join(self.output_dir, f"confirmation_{self.booking.booking_id}.pdf")
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    unittest.main()
