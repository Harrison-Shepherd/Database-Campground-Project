# Database/sql_db.py

import pyodbc
from Utils.logging_config import logger


def connect_to_sql():
    """
    Connects to the local SQL database (camping).
    :return: Connection object to the SQL database.
    """
    connection_string = (
        "Driver={ODBC Driver 18 for SQL Server};"
        "Server=campground-server.database.windows.net;"
        "Database=CampgroundBookingsDB;"
        "Uid=CampgroundAdmin;"
        "Pwd=CampgroundDatabasePassword!1;"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    conn = pyodbc.connect(connection_string)
    return conn
