import unittest
from Utils.config_loader import load_config, get_connection_string

class TestConfigLoader(unittest.TestCase):
    """
    Test class for testing the configuration loader functionality.

    This class verifies that configuration settings are correctly loaded from JSON files
    and that connection strings are correctly retrieved and formatted.
    """

    def test_load_valid_config(self):
        """
        Test loading a valid configuration file.

        Verifies that the configuration file 'connection_strings.json' is correctly loaded
        and contains the expected SQL server settings.
        """
        # Load configuration from a valid JSON file
        config = load_config('connection_strings.json')
        # Assert that the loaded configuration includes SQL server settings
        self.assertIn('sql_server', config, "Config should load SQL server settings.")

    def test_missing_config_file(self):
        """
        Test loading a missing configuration file.

        Verifies that attempting to load a non-existent configuration file raises a FileNotFoundError.
        """
        # Attempt to load a non-existent configuration file and expect a FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            load_config('non_existent_config.json')

    def test_get_connection_string(self):
        """
        Test retrieving a connection string from the configuration.

        Verifies that the connection string for the SQL server is correctly formatted and includes
        the necessary server details.
        """
        # Retrieve the connection string for the SQL server
        conn_str = get_connection_string('sql_server')
        # Normalize keys to lowercase to ensure case-insensitivity in the test
        self.assertIn('server=', conn_str.lower(), "Connection string should include server details.")

if __name__ == "__main__":
    unittest.main()
