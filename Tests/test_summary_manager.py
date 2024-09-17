import unittest
from datetime import datetime
from Models.summary import Summary
from Utils.pdf_generator import PDFGenerator  # Import the PDFGenerator class correctly
import os

class TestSummaryManager(unittest.TestCase):
    """
    Test class for testing the functionality of the Summary and PDF generation process.

    This class tests the creation of summary data and the generation of summary PDFs to
    ensure that the summary information is correctly handled and the PDFs are generated as expected.
    """

    def setUp(self):
        """
        Set up test environment before each test.

        Creates a list of mock bookings and initializes the PDFGenerator. It also sets up
        the output directory where the generated PDFs will be saved.
        """
        # Create mock bookings with varying total costs and campsite IDs
        self.bookings = []
        for i in range(5):
            self.bookings.append(
                type('Booking', (object,), {
                    'booking_id': i + 1,
                    'total_cost': 100 + i * 50,
                    'campsite_id': i + 1
                })
            )
        # Initialize PDFGenerator with a report title
        self.pdf_generator = PDFGenerator("Daily Summary Report")
        self.output_dir = "pdfs"  # Directory to save generated PDFs
        # Create the output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def test_summary_creation(self):
        """
        Test the creation of a Summary object.

        Verifies that the Summary object is created with the correct campground ID, total sales, and total bookings.
        """
        summary = Summary(
            campground_id=1121132,
            summary_date=datetime.now().date(),
            total_sales=500,
            total_bookings=5
        )
        # Assert that the summary fields match the expected values
        self.assertEqual(summary.campground_id, 1121132)
        self.assertEqual(summary.total_sales, 500)
        self.assertEqual(summary.total_bookings, 5)

    def test_generate_summary_pdf(self):
        """
        Test the generation of a summary PDF.

        Verifies that the PDF file is generated in the specified output directory with the correct filename.
        """
        summary = Summary(
            campground_id=1121132,
            summary_date=datetime.now().date(),
            total_sales=500,
            total_bookings=5
        )
        # Generate the summary PDF
        filename = self.pdf_generator.generate_summary(summary)
        # Expected filename based on summary date
        expected_filename = os.path.join(self.output_dir, f"summary_{summary.summary_date}.pdf")
        # Assert that the PDF file was created successfully
        self.assertTrue(os.path.exists(expected_filename), "Summary PDF should be created.")

    def tearDown(self):
        """
        Clean up after each test.

        Removes any files created during testing to ensure a clean environment for subsequent tests.
        """
        # Determine the expected filename based on the current date
        summary_filename = os.path.join(self.output_dir, f"summary_{datetime.now().date()}.pdf")
        # Remove the summary PDF if it exists
        if os.path.exists(summary_filename):
            os.remove(summary_filename)

if __name__ == "__main__":
    unittest.main()
