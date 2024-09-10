# Tests/test_cosmos_db.py
import unittest
from unittest.mock import MagicMock
from Database.cosmos_db import connect_to_cosmos, insert_booking_to_cosmos

class TestCosmosDB(unittest.TestCase):
    def setUp(self):
        self.container = MagicMock()

    def test_insert_booking_to_cosmos(self):
        booking_data = {'booking_id': 1}
        self.container.query_items.return_value = []
        insert_booking_to_cosmos(self.container, booking_data)
        self.container.create_item.assert_called_with(booking_data)

if __name__ == "__main__":
    unittest.main()
