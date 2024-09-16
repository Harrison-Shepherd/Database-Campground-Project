import unittest
from datetime import datetime
from Models.summary import Summary
from Utils.pdf_generator import PDFGenerator  # Import the PDFGenerator class correctly
import os

class TestSummaryManager(unittest.TestCase):
    def setUp(self):
        self.bookings = []
        for i in range(5):
            self.bookings.append(
                type('Booking', (object,), {
                    'booking_id': i + 1,
                    'total_cost': 100 + i * 50,
                    'campsite_id': i + 1
                })
            )
        self.pdf_generator = PDFGenerator("Daily Summary Report")  # Initialize PDFGenerator with a title
        self.output_dir = "pdfs"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def test_summary_creation(self):
        summary = Summary(
            campground_id=1121132,
            summary_date=datetime.now().date(),
            total_sales=500,
            total_bookings=5
        )
        self.assertEqual(summary.campground_id, 1121132)
        self.assertEqual(summary.total_sales, 500)
        self.assertEqual(summary.total_bookings, 5)

    def test_generate_summary_pdf(self):
        summary = Summary(
            campground_id=1121132,
            summary_date=datetime.now().date(),
            total_sales=500,
            total_bookings=5
        )
        filename = self.pdf_generator.generate_summary(summary)  # Use the generate_summary method
        expected_filename = os.path.join(self.output_dir, f"summary_{summary.summary_date}.pdf")
        self.assertTrue(os.path.exists(expected_filename), "Summary PDF should be created.")

    def tearDown(self):
        # Clean up any files created during testing
        summary_filename = os.path.join(self.output_dir, f"summary_{datetime.now().date()}.pdf")
        if os.path.exists(summary_filename):
            os.remove(summary_filename)

if __name__ == "__main__":
    unittest.main()
