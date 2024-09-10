# Tests/test_campsite_manager.py
import unittest
from Utils.campsite_manager import initialize_campsites

class TestCampsiteManager(unittest.TestCase):
    def test_initialize_campsites(self):
        campsites = initialize_campsites()
        self.assertEqual(len(campsites), 30)
        self.assertEqual(campsites[0].size, 'Small')
        self.assertEqual(campsites[10].size, 'Medium')
        self.assertEqual(campsites[20].size, 'Large')

if __name__ == "__main__":
    unittest.main()
