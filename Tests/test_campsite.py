import unittest
from Models.campsite import Campsite

class TestCampsite(unittest.TestCase):

    def setUp(self):
        """Set up a campsite with available dates."""
        self.campsite = Campsite(site_number=1, size="Large", rate=60, available_dates=["2024-09-07", "2024-09-08"])

    def test_campsite_availability(self):
        """Test checking availability within a date range."""
        self.assertTrue(self.campsite.is_available("2024-09-07", "2024-09-08"))  # Should be available
        self.assertFalse(self.campsite.is_available("2024-09-07", "2024-09-09"))  # Should not be available

if __name__ == '__main__':
    unittest.main()
