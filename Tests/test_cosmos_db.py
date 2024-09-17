# Tests/test_cosmos_db.py

import unittest
from unittest.mock import MagicMock
from Database.cosmos_db import connect_to_cosmos, insert_booking_to_cosmos

class TestCosmosDB(unittest.TestCase):
    """
    Test class for testing Cosmos DB interactions.

    This class tests the functionality of inserting bookings into the Cosmos DB container
    by mocking the container and checking the behavior of the insert function.
    """

    def setUp(self):
        """
        Set up the test environment before each test.

        Initializes a mock Cosmos DB container to simulate the database interactions.
        """
        # Create a mock container to simulate Cosmos DB operations
        self.container = MagicMock()

    def test_insert_booking_to_cosmos(self):
        """
        Test the insertion of booking data into the Cosmos DB container.

        This test checks that the `insert_booking_to_cosmos` function correctly inserts booking data
        into the Cosmos DB container when the booking does not already exist.
        """
        booking_data = {'booking_id': 1}  # Sample booking data to insert
        # Mock the return value of the query_items method to simulate an empty result (booking does not exist)
        self.container.query_items.return_value = []

        # Call the insert function with the mock container and booking data
        insert_booking_to_cosmos(self.container, booking_data)

        # Assert that the create_item method was called with the correct booking data
        self.container.create_item.assert_called_with(booking_data)

if __name__ == "__main__":
    unittest.main()
