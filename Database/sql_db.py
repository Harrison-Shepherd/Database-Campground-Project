import pyodbc
from Utils.logging_config import logger

def connect_to_sql():
    """
    Connects to the local SQL database (camping).
    
    :return: Connection object to the SQL database.
    :raises: Exception if the connection fails.
    """
    connection_string = (
        "Driver={ODBC Driver 18 for SQL Server};"
        "Server=campground-server.database.windows.net;"  # Server address
        "Database=CampgroundBookingsDB;"                  # Database name
        "Uid=CampgroundAdmin;"                            # Username
        "Pwd=CampgroundDatabasePassword!1;"               # Password
        "Encrypt=yes;"                                    # Encrypt connection
        "TrustServerCertificate=no;"                      # Do not trust the server certificate
        "Connection Timeout=30;"                          # Connection timeout in seconds
    )
    try:
        conn = pyodbc.connect(connection_string)
        logger.info("Connected to SQL database successfully.")
        print("Connected to SQL database successfully.")

        return conn
    except pyodbc.Error as e:
        logger.error(f"Error connecting to SQL database: {e}")
        raise
