import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from Models.booking import Booking
from Models.campsite import Campsite
from Utils.booking_processor import process_bookings

# Define a test class for the BookingProcessor
class TestBookingProcessor(unittest.TestCase):
    """
    Test class for testing the booking processing functionality.

    This class verifies that bookings are processed correctly, including campsite allocation
    and interaction with database connections.
    """
    # Set up the test environment before each test
    def setUp(self):
        """
        Set up the test environment before each test.

        Initializes mock Booking and Campsite objects and sets up mocked database connections.
        """
        # Create a mock Booking object
        self.bookings = [Booking(
            booking_id=1,
            customer_id=101,
            booking_date="2024-09-01",
            arrival_date="2024-09-07",
            campsite_size='Medium',
            num_campsites=1
        )]
        # Create a mock Campsite object
        self.campsites = [Campsite(
            site_number=1,
            size='Medium',
            rate_per_night=60
        )]
        # Mock the book_campsite method of Campsite to simulate successful allocation
        self.campsites[0].book_campsite = MagicMock(return_value=True)
        # Initialize mock database connections
        self.head_office_conn = MagicMock()
        self.cosmos_conn = MagicMock()


    # Test the successful processing of bookings
    @patch('Utils.booking_processor.insert_booking_to_cosmos_db')
    def test_process_bookings_success(self, mock_insert_booking_to_cosmos_db):
        """
        Test successful processing of bookings.

        Verifies that a booking is processed correctly and a suitable campsite is allocated.
        Also checks that the Cosmos DB insertion happens.
        """
        # Process the bookings with the initialized campsite
        process_bookings(self.bookings, self.campsites, self.head_office_conn, self.cosmos_conn, campground_id=1121132)
        # Assert that the booking's campsite ID is set to 1, indicating successful allocation
        self.assertEqual(self.bookings[0].campsite_id, 1, "Campsite should be allocated.")
        # Ensure that the Cosmos DB insert function was called
        mock_insert_booking_to_cosmos_db.assert_called()

    def test_process_bookings_no_campsites(self):
        """
        Test processing of bookings when no campsites are available.

        Verifies that when all campsites are booked, the booking is not allocated to any campsite.
        """
        # Use datetime objects for start and end dates
        start_date = datetime(2024, 9, 7)
        end_date = start_date + timedelta(days=7)
        # Pre-book the campsite to make it unavailable for new bookings
        self.campsites[0].book_campsite = MagicMock(return_value=False)
        # Process the bookings with no available campsites
        process_bookings(self.bookings, self.campsites, self.head_office_conn, self.cosmos_conn, campground_id=1121132)
        # Assert that the booking's campsite ID remains None, indicating no allocation
        self.assertIsNone(self.bookings[0].campsite_id, "Campsite should not be allocated if unavailable.")
        # Ensure that the SQL update was never called since no campsite was allocated
        self.head_office_conn.cursor().execute.assert_not_called()

if __name__ == "__main__":
    unittest.main()
