import pyodbc
from Utils.logging_config import logger

# Function to connect to the local SQL database
def connect_to_sql():
    """
    Connects to the local SQL database (camping).

    :return: Connection object to the SQL database.
    :raises Exception: If the connection fails.
    """
    # Define the connection string with necessary parameters
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
    try:
        # Attempt to connect to the SQL database using the connection string
        conn = pyodbc.connect(connection_string)
        logger.info("Connected to SQL database successfully.")  # Log successful connection
        print("Connected to SQL database successfully.")        # Print success message for user feedback

        return conn  # Return the active database connection object

    except pyodbc.Error as e:
        # Log the error if connection fails and raise the exception for further handling
        logger.error(f"Error connecting to SQL database: {e}")
        raise
