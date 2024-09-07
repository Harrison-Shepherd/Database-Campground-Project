# Tests/test_database_operations.py

import unittest
from Database.sql_db import connect_to_sql, insert_summary
from Database.head_office_db import connect_to_head_office, fetch_bookings, update_booking_campground
from Database.cosmos_db import connect_to_cosmos, insert_booking_to_cosmos  # Correct the import name
from datetime import datetime

class TestDatabaseOperations(unittest.TestCase):

    def test_sql_connection(self):
        """Test SQL database connection."""
        conn = connect_to_sql()
        self.assertIsNotNone(conn, "Failed to connect to SQL database.")
        if conn:
            conn.close()

    def test_insert_summary(self):
        """Test inserting a summary record into the SQL database."""
        conn = connect_to_sql()
        summary_data = {
            "campground_id": 1121132,
            "summary_date": datetime.now().strftime("%Y-%m-%d"),
            "total_sales": 1500.50,
            "total_bookings": 12
        }
        try:
            insert_summary(conn, summary_data)
            self.assertTrue(True, "Summary inserted successfully.")
        except Exception as e:
            self.fail(f"Failed to insert summary: {e}")
        finally:
            conn.close()

    def test_head_office_connection(self):
        """Test connection to Head Office database."""
        conn = connect_to_head_office()
        self.assertIsNotNone(conn, "Failed to connect to Head Office database.")
        if conn:
            conn.close()

    def test_fetch_bookings(self):
        """Test fetching bookings from Head Office."""
        conn = connect_to_head_office()
        if conn:
            bookings = fetch_bookings(conn)
            self.assertIsInstance(bookings, list, "Bookings should be a list.")
            conn.close()

    def test_update_booking_campground(self):
        """Test updating a booking's campground ID in Head Office database."""
        conn = connect_to_head_office()
        if conn:
            bookings = fetch_bookings(conn)
            if bookings:
                booking_id = bookings[0][0]  # Assuming booking ID is the first field
                try:
                    update_booking_campground(conn, booking_id, 1121132)
                    self.assertTrue(True, "Booking updated successfully.")
                except Exception as e:
                    self.fail(f"Failed to update booking: {e}")
            conn.close()

    def test_cosmos_connection(self):
        """Test connection to Cosmos DB."""
        container = connect_to_cosmos()
        self.assertIsNotNone(container, "Failed to connect to Cosmos DB.")

    def test_insert_cosmos_booking(self):
        """Test inserting a booking into Cosmos DB."""
        container = connect_to_cosmos()
        booking = {
            "booking_id": 1,
            "customer_id": 101,
            "booking_date": "2024-09-07",
            "arrival_date": "2024-09-07",
            "campground_id": 1121132,
            "campsite_size": "Large",
            "num_campsites": 1
        }
        try:
            insert_booking_to_cosmos(container, booking)
            self.assertTrue(True, "Booking inserted into Cosmos DB successfully.")
        except Exception as e:
            self.fail(f"Failed to insert booking into Cosmos DB: {e}")

if __name__ == '__main__':
    unittest.main()
