import unittest
from datetime import datetime, timedelta
from Models.booking import Booking
from Models.campsite import Campsite, allocate_campsite


# Define a test class for the Booking model
class TestBooking(unittest.TestCase):
    """
    Unit test class for the Booking model and campsite allocation logic.

    This class tests the functionality of the Booking class, including the creation of Booking objects,
    the validation of booking dates, and the allocation of campsites based on booking requirements.
    """
    # Set up the test environment before each test
    def setUp(self):
        """
        Set up the test environment before each test.

        This method initializes a mock Booking object and a list of available Campsite objects to be
        used for campsite allocation during the test cases.
        """
        # Initialize a mock Booking object with predefined attributes
        self.booking = Booking(
            booking_id=1,
            customer_id=101,
            booking_date="2024-09-01",
            arrival_date="2024-09-07",
            campground_id=1121132,
            campsite_size='Medium',
            num_campsites=1
        )
        
        # Define a list of available Campsite objects with varying sizes and rates
        self.campsites = [
            Campsite(site_number=1, size='Medium', rate_per_night=60),
            Campsite(site_number=2, size='Large', rate_per_night=70)
        ]

    # Test the creation of a Booking object
    def test_booking_creation(self):
        """
        Test the creation of a Booking object.

        Verifies that the attributes of the Booking object (e.g., booking ID, customer ID, campsite size,
        and number of campsites) are correctly initialized and match the expected values.
        """
        # Check that the booking attributes are correctly set upon initialization
        self.assertEqual(self.booking.booking_id, 1, "Booking ID should be 1.")
        self.assertEqual(self.booking.customer_id, 101, "Customer ID should be 101.")
        self.assertEqual(self.booking.campsite_size, 'Medium', "Campsite size should be 'Medium'.")
        self.assertEqual(self.booking.num_campsites, 1, "Number of campsites should be 1.")

    # Test the validation and conversion of date inputs
    def test_validate_date(self):
        """
        Test the validation and conversion of date inputs.

        Verifies that the booking's arrival date is correctly validated and converted into a datetime object.
        This ensures that any string or other supported input type is properly parsed.
        """
        # Verify that the arrival date was properly validated and converted into a datetime object
        self.assertEqual(self.booking.arrival_date, datetime(2024, 9, 7), "Arrival date should be September 7, 2024.")

    # Test the allocation of a campsite based on booking requirements
    def test_allocate_campsite(self):
        """
        Test the allocation of a campsite based on the booking requirements.

        Verifies that the allocate_campsite function allocates an appropriate campsite based on the
        booking's campsite size and the campsite's availability for the specified booking period.
        """
        # Define the booking period with start and end dates
        start_date = datetime(2024, 9, 7)
        end_date = start_date + timedelta(days=7)

        # Call the allocate_campsite function to allocate a campsite that matches the booking requirements
        allocated_campsite = allocate_campsite(self.campsites, start_date, end_date, self.booking)
        
        # Assert that a campsite was successfully allocated
        self.assertIsNotNone(allocated_campsite, "Campsite allocation should succeed.")

        # Verify that the allocated campsite is the expected one (site number 1)
        self.assertEqual(allocated_campsite.site_number, 1, "The allocated campsite should be site number 1.")

if __name__ == "__main__":
    unittest.main()
