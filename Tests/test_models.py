# Tests/test_models.py

import unittest
from Models.booking import Booking
from Models.campsite import Campsite
from Models.customer import Customer

class TestModels(unittest.TestCase):

    def test_booking_creation(self):
        """Test the creation of a Booking object."""
        booking = Booking(1, "John Doe", "2024-09-07", "Large", 1)
        self.assertEqual(booking.booking_id, 1)
        self.assertEqual(booking.customer_name, "John Doe")
        self.assertEqual(booking.arrival_date, "2024-09-07")
        self.assertEqual(booking.campsite_size, "Large")

    def test_campsite_availability(self):
            # Create a Campsite instance
            campsite = Campsite(site_number=1, size="Large", rate=60, available_dates=["2024-09-07", "2024-09-08"])

            # Test availability with both start and end dates
            self.assertTrue(campsite.is_available("2024-09-07", "2024-09-08"))  # Should be available
            self.assertFalse(campsite.is_available("2024-09-07", "2024-09-09"))  # Should not be available

    def test_customer_creation(self):
        """Test the creation of a Customer object."""
        customer = Customer(101, "Jane", "Smith", "0423 456 789", "456 Elm St", "4011")
        self.assertEqual(customer.first_name, "Jane")
        self.assertEqual(customer.last_name, "Smith")
        self.assertEqual(customer.phone, "0423 456 789")

if __name__ == '__main__':
    unittest.main()
