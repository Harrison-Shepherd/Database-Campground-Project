import unittest
import os
from Utils.pdf_generator import PDFGenerator  
from Models.booking import Booking

# Define a test class for the PDF confirmation generation
class TestConfirmation(unittest.TestCase):
    """
    Test class for testing the PDF confirmation generation functionality.

    This class verifies that the PDF for a booking confirmation is generated correctly and that
    the returned file path matches the expected output.
    """

    # Set up the test environment before each test
    def setUp(self):
        """
        Set up the test environment before each test.

        Initializes a mock booking object and the PDFGenerator. It also prepares the output directory
        where the generated PDFs will be saved.
        """
        # Create a mock booking object with necessary attributes
        self.booking = Booking(
            booking_id=1,
            customer_id=101,
            booking_date="2024-09-01",
            arrival_date="2024-09-07",
            campground_id=1121132,
            campsite_size='Medium',
            num_campsites=1
        )
        # Define the output directory for PDFs
        self.output_dir = "pdfs"
        # Initialize the PDFGenerator with a report title
        self.pdf_generator = PDFGenerator("Booking Confirmation")
        # Create the output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    # Test the generation of a booking confirmation PDF
    def test_generate_confirmation(self):
        """
        Test the generation of a booking confirmation PDF.

        Verifies that the PDF file is generated in the specified output directory with the correct filename
        and that the function returns the correct file path.
        """
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

    # Clean up after each test
    def tearDown(self):
        """
        Clean up after each test.

        Removes any generated PDF files to ensure a clean environment for subsequent tests.
        """
        # Clean up by removing the generated file if it exists
        filename = os.path.join(self.output_dir, f"confirmation_{self.booking.booking_id}.pdf")
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    unittest.main()
