# Database/sql_db.py
import pyodbc

def connect_to_sql():
    """
    Connects to the local SQL database and returns the connection object.
    """
    connection_string = (
        "Driver={ODBC Driver 18 for SQL Server};"
        "Server=campground-server.database.windows.net;"  # Server address for local SQL
        "Database=CampgroundBookingsDB;"                  # Database name
        "Uid=CampgroundAdmin;"                            # Username
        "Pwd=CampgroundDatabasePassword!1;"               # Password
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    conn = pyodbc.connect(connection_string)
    return conn
