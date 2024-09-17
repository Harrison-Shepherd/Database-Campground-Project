import unittest
import os
from Utils.pdf_generator import PDFGenerator  # Import the PDFGenerator class correctly
from Models.booking import Booking

class TestPDFGeneration(unittest.TestCase):
    """
    Test class for testing the PDF generation functionality of the PDFGenerator class.

    This class tests the generation of booking confirmation PDFs to ensure that the PDFs are created
    correctly in the specified output directory.
    """

    def setUp(self):
        """
        Set up the test environment before each test.

        Creates a mock booking object and initializes the PDFGenerator. It also sets up
        the output directory where the generated PDFs will be saved.
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

    def test_generate_confirmation_pdf(self):
        """
        Test the generation of a booking confirmation PDF.

        Verifies that the PDF file is generated in the specified output directory with the correct filename.
        """
        # Define the expected filename for the generated PDF
        filename = os.path.join(self.output_dir, f"confirmation_{self.booking.booking_id}.pdf")
        # Generate the confirmation PDF using the PDFGenerator
        self.pdf_generator.generate_confirmation(self.booking)
        # Assert that the PDF file was created successfully
        self.assertTrue(os.path.exists(filename), "Confirmation PDF should be created.")

    def tearDown(self):
        """
        Clean up after each test.

        Removes any PDF files created during testing to ensure a clean environment for subsequent tests.
        """
        # Define the expected filename for cleanup
        filename = os.path.join(self.output_dir, f"confirmation_{self.booking.booking_id}.pdf")
        # Remove the generated PDF if it exists
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    unittest.main()
