import unittest
from datetime import datetime, timedelta
from Models.campsite import Campsite


# Define a test class for the Campsite model
class TestCampsite(unittest.TestCase):
    """
    Test class for testing the functionality of the Campsite class.

    This class tests the campsite availability and booking methods to ensure that
    campsite reservations are handled correctly.
    """

    # Set up the test environment before each test
    def setUp(self):
        """
        Set up the test environment before each test.

        Initializes a Campsite object with specific attributes to test booking and availability.
        """
        # Initialize a Campsite object with specified attributes
        self.campsite = Campsite(site_number=1, size='Medium', rate_per_night=60)

    # Test the availability of the campsite
    def test_is_available(self):
        """
        Test the availability of the campsite.

        Verifies that the campsite is initially available for a specified date range.
        """
        # Define the start and end dates for availability check
        start_date = datetime(2024, 9, 7)
        end_date = start_date + timedelta(days=7)
        # Assert that the campsite is available initially
        self.assertTrue(self.campsite.is_available(start_date, end_date), "Campsite should be available initially.")

    # Test booking the campsite
    def test_book_campsite(self):
        """
        Test booking the campsite.

        Verifies that the campsite can be booked for a specified date range and that it is
        no longer available for the same period after booking.
        """
        # Define the start and end dates for the booking
        start_date = datetime(2024, 9, 7)
        end_date = start_date + timedelta(days=7)
        # Assert that booking the campsite succeeds
        self.assertTrue(self.campsite.book_campsite(start_date, end_date), "Campsite booking should succeed.")
        # Assert that the campsite is no longer available after booking
        self.assertFalse(self.campsite.is_available(start_date, end_date), "Campsite should not be available after booking.")

    # Test the rate calculation for the campsite
if __name__ == "__main__":
    unittest.main()
