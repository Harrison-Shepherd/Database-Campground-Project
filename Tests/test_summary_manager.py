# Tests/test_summary_manager.py
import unittest
from datetime import datetime
from Models.summary import Summary
from Utils.summary_manager import generate_summary_pdf, create_and_insert_summary
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
        generate_summary_pdf(summary)
        filename = f"confirmation_pdfs/summary_{summary.summary_date}.pdf"
        self.assertTrue(os.path.exists(filename))

if __name__ == "__main__":
    unittest.main()
