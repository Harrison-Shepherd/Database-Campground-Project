# Tests/test_sql_db.py
import unittest
from Database.sql_db import connect_to_sql

class TestSQLDatabase(unittest.TestCase):
    def test_connect_to_sql(self):
        conn = connect_to_sql()
        self.assertIsNotNone(conn)
        conn.close()

if __name__ == "__main__":
    unittest.main()
