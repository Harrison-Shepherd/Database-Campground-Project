# Tests/test_query_processor.py
import unittest
from unittest.mock import MagicMock
from Utils.query_processor import execute_query

class TestQueryProcessor(unittest.TestCase):
    def test_execute_query(self):
        conn = MagicMock()
        cursor = conn.cursor.return_value
        execute_query(conn, "SELECT * FROM camping.booking")
        cursor.execute.assert_called_once()

if __name__ == "__main__":
    unittest.main()
