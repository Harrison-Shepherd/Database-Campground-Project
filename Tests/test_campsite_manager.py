import unittest
from Utils.campsite_manager import initialize_campsites

class TestCampsiteManager(unittest.TestCase):
    """
    Test class for testing the initialization of campsites.

    This class tests the `initialize_campsites` function to ensure that it correctly
    initializes campsites with the expected sizes and quantities.
    """

    def test_initialize_campsites(self):
        """
        Test the initialization of campsites.

        Verifies that the `initialize_campsites` function initializes the correct number of campsites
        and that the campsites are categorized correctly by size (Small, Medium, Large).
        """
        # Call the function to initialize campsites
        campsites = initialize_campsites()
        
        # Assert that the total number of campsites is 30
        self.assertEqual(len(campsites), 30, "The total number of campsites should be 30.")
        
        # Assert that the first 10 campsites are of size 'Small'
        self.assertEqual(campsites[0].size, 'Small', "The first campsite should be of size 'Small'.")
        
        # Assert that the next 10 campsites (starting from index 10) are of size 'Medium'
        self.assertEqual(campsites[10].size, 'Medium', "The 11th campsite should be of size 'Medium'.")
        
        # Assert that the last 10 campsites (starting from index 20) are of size 'Large'
        self.assertEqual(campsites[20].size, 'Large', "The 21st campsite should be of size 'Large'.")

if __name__ == "__main__":
    unittest.main()
