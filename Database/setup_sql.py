import pyodbc
from Utils.logging_config import logger

def connect_to_sql():
    """
    Connects to the SQL Server database.

    :return: Connection object if successful, or None if connection fails.
    """
    # Define the connection string with required parameters for SQL Server
    connection_string = (
        "Driver={ODBC Driver 18 for SQL Server};"           # Specifies the ODBC driver for SQL Server
        "Server=campground-server.database.windows.net;"    # SQL Server address
        "Database=CampgroundBookingsDB;"                    # Name of the database to connect to
        "Uid=CampgroundAdmin;"                              # Database username
        "Pwd=CampgroundDatabasePassword!1;"                 # Database password
        "Encrypt=yes;"                                      # Encrypt the connection
        "TrustServerCertificate=no;"                        # Do not trust the server certificate
        "Connection Timeout=30;"                            # Timeout period for the connection attempt
    )
    try:
        # Attempt to connect to the SQL database
        conn = pyodbc.connect(connection_string)
        logger.info("Connected to SQL database successfully.")
        return conn  # Return the connection object

    except pyodbc.Error as e:
        # Log any errors encountered during the connection attempt
        logger.error(f"Error connecting to SQL database: {e}")
        return None  # Return None if the connection fails

def create_schema_if_not_exists(cursor):
    """
    Creates the schema 'camping' if it does not exist.

    :param cursor: Database cursor object.
    """
    try:
        # SQL command to check if the schema 'camping' exists and create it if it doesn't
        query = """
        IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'camping')
        BEGIN
            EXEC('CREATE SCHEMA camping');
        END
        """
        cursor.execute(query)  # Execute the query
        logger.info("Schema 'camping' checked/created successfully.")

    except pyodbc.Error as e:
        # Log any errors encountered during schema creation
        logger.error(f"Error creating schema: {e}")

def create_tables(cursor):
    """
    Creates the necessary tables in the SQL database if they do not exist.

    :param cursor: Database cursor object.
    """
    # SQL command to create the 'customers' table if it doesn't exist
    create_customers_table = """
    IF OBJECT_ID('camping.customers', 'U') IS NULL
    BEGIN
        CREATE TABLE camping.customers (
            customer_id INT IDENTITY(1,1) PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            phone VARCHAR(25) NULL,
            address VARCHAR(255) NULL,
            post_code VARCHAR(4) NULL
        );
    END
    """

    # SQL command to create the 'booking' table if it doesn't exist
    create_booking_table = """
    IF OBJECT_ID('camping.booking', 'U') IS NULL
    BEGIN
        CREATE TABLE camping.booking (
            booking_id INT IDENTITY(1,1) PRIMARY KEY,
            customer_id INT NULL FOREIGN KEY REFERENCES camping.customers(customer_id),
            booking_date DATE NOT NULL,
            arrival_date DATE NOT NULL,
            campground_id INT NOT NULL,
            campsite_size VARCHAR(10),
            num_campsites INT
        );
    END
    """

    # SQL command to create the 'summary' table if it doesn't exist
    create_summary_table = """
    IF OBJECT_ID('camping.summary', 'U') IS NULL
    BEGIN
        CREATE TABLE camping.summary (
            summary_id INT IDENTITY(1,1) PRIMARY KEY,
            campground_id INT NOT NULL,
            summary_date DATE NOT NULL,
            total_sales DECIMAL(10, 2) NOT NULL,
            total_bookings INT NOT NULL
        );
    END
    """

    try:
        # Execute the table creation commands
        cursor.execute(create_customers_table)
        cursor.execute(create_booking_table)
        cursor.execute(create_summary_table)
        logger.info("Tables created successfully.")

    except pyodbc.Error as e:
        # Log any errors encountered during table creation
        logger.error(f"Error creating tables: {e}")

def execute_sql_file(cursor, file_path):
    """
    Executes an SQL script from a file.

    :param cursor: Cursor object for the SQL connection.
    :param file_path: Path to the .sql file to be executed.
    """
    try:
        # Read and execute the SQL script from the specified file path
        with open(file_path, 'r') as file:
            sql_script = file.read()
        cursor.execute(sql_script)
        logger.info(f"SQL script {file_path} executed successfully.")

    except FileNotFoundError:
        # Log error if the specified file is not found
        logger.error(f"SQL file not found: {file_path}")
    except pyodbc.Error as e:
        # Log any errors encountered during script execution
        logger.error(f"Error executing SQL script: {e}")

def setup_database():
    """
    Main function to set up the SQL database: create schema, tables, and load initial data.
    """
    conn = connect_to_sql()  # Establish connection to the SQL database
    if conn:
        cursor = conn.cursor()
        try:
            # Step 1: Create schema if not exists
            create_schema_if_not_exists(cursor)

            # Step 2: Create required tables
            create_tables(cursor)
            conn.commit()  # Commit the changes to the database

            # Step 3: Execute initial setup SQL files (if needed)
            create_schema_path = "Assets/create_head_office_schema.sql"  # Path to schema creation script
            load_data_path = "Assets/load_head_office_data.sql"          # Path to data loading script
            execute_sql_file(cursor, create_schema_path)
            execute_sql_file(cursor, load_data_path)
            conn.commit()  # Commit the changes after executing scripts

        except Exception as e:
            # Log any errors during the setup process and rollback changes
            logger.error(f"An error occurred during database setup: {e}")
            conn.rollback()

        finally:
            cursor.close()  # Close the cursor
            conn.close()    # Close the database connection
            logger.info("Database setup completed and connection closed.")

if __name__ == "__main__":
    setup_database()  # Run the database setup when the script is executed
