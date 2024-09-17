# Tests/test_booking.py

import unittest
from datetime import datetime, timedelta
from Models.booking import Booking
from Models.campsite import Campsite, allocate_campsite

class TestBooking(unittest.TestCase):
    """
    Test class for testing the functionality of the Booking class and campsite allocation.

    This class verifies the creation of Booking objects, date validation, and the allocation
    of campsites based on booking requirements.
    """

    def setUp(self):
        """
        Set up the test environment before each test.

        Initializes a Booking object and a list of Campsite objects to be used in the tests.
        """
        # Create a mock Booking object with necessary attributes
        self.booking = Booking(
            booking_id=1,
            customer_id=101,
            booking_date="2024-09-01",
            arrival_date="2024-09-07",
            campground_id=1121132,
            campsite_size='Medium',
            num_campsites=1
        )
        # Create a list of Campsite objects with varying sizes and rates
        self.campsites = [
            Campsite(site_number=1, size='Medium', rate_per_night=60),
            Campsite(site_number=2, size='Large', rate_per_night=70)
        ]

    def test_booking_creation(self):
        """
        Test the creation of a Booking object.

        Verifies that the booking attributes are correctly set during initialization.
        """
        # Assert that the booking attributes match the expected values
        self.assertEqual(self.booking.booking_id, 1, "Booking ID should be 1.")
        self.assertEqual(self.booking.customer_id, 101, "Customer ID should be 101.")
        self.assertEqual(self.booking.campsite_size, 'Medium', "Campsite size should be 'Medium'.")
        self.assertEqual(self.booking.num_campsites, 1, "Number of campsites should be 1.")

    def test_validate_date(self):
        """
        Test the date validation of the Booking object.

        Verifies that the arrival date is correctly validated and converted to a datetime object.
        """
        # Assert that the arrival date matches the expected datetime object
        self.assertEqual(self.booking.arrival_date, datetime(2024, 9, 7), "Arrival date should be September 7, 2024.")

    def test_allocate_campsite(self):
        """
        Test the allocation of a campsite based on the booking requirements.

        Verifies that the allocate_campsite function correctly allocates an available campsite
        that matches the booking size and availability.
        """
        # Define the start and end dates for the booking period
        start_date = datetime(2024, 9, 7)
        end_date = start_date + timedelta(days=7)
        # Call the allocate_campsite function to allocate a campsite based on the booking
        allocated_campsite = allocate_campsite(self.campsites, start_date, end_date, self.booking)
        # Assert that a campsite was allocated
        self.assertIsNotNone(allocated_campsite, "Campsite allocation should succeed.")
        # Assert that the allocated campsite matches the expected site number
        self.assertEqual(allocated_campsite.site_number, 1, "The allocated campsite should be site number 1.")

if __name__ == "__main__":
    unittest.main()
