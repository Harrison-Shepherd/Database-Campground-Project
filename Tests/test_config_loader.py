# Tests/test_config_loader.py
import unittest
from Utils.config_loader import load_config, get_connection_string

class TestConfigLoader(unittest.TestCase):
    def test_load_valid_config(self):
        config = load_config('connection_strings.json')
        self.assertIn('sql_server', config, "Config should load SQL server settings.")

    def test_missing_config_file(self):
        with self.assertRaises(FileNotFoundError):
            load_config('non_existent_config.json')

    def test_get_connection_string(self):
        conn_str = get_connection_string('sql_server')
        # Normalize keys to lowercase to ensure case-insensitivity in the test
        self.assertIn('server=', conn_str.lower(), "Connection string should include server details.")

if __name__ == "__main__":
    unittest.main()
