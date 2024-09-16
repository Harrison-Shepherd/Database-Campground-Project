import pyodbc
from Utils.logging_config import logger

def connect_to_sql():
    """
    Connects to the SQL Server database.

    :return: Connection object or None if connection fails.
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
    try:
        conn = pyodbc.connect(connection_string)
        logger.info("Connected to SQL database successfully.")
        return conn
    except pyodbc.Error as e:
        logger.error(f"Error connecting to SQL database: {e}")
        return None

def create_schema_if_not_exists(cursor):
    """
    Creates the schema 'camping' if it does not exist.

    :param cursor: Database cursor object.
    """
    try:
        query = """
        IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'camping')
        BEGIN
            EXEC('CREATE SCHEMA camping');
        END
        """
        cursor.execute(query)
        logger.info("Schema 'camping' checked/created successfully.")
    except pyodbc.Error as e:
        logger.error(f"Error creating schema: {e}")

def create_tables(cursor):
    """
    Creates the necessary tables in the SQL database if they do not exist.

    :param cursor: Database cursor object.
    """
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
        cursor.execute(create_customers_table)
        cursor.execute(create_booking_table)
        cursor.execute(create_summary_table)
        logger.info("Tables created successfully.")
    except pyodbc.Error as e:
        logger.error(f"Error creating tables: {e}")

def execute_sql_file(cursor, file_path):
    """
    Executes an SQL script from a file.

    :param cursor: Cursor object for the SQL connection.
    :param file_path: Path to the .sql file to be executed.
    """
    try:
        with open(file_path, 'r') as file:
            sql_script = file.read()

        cursor.execute(sql_script)
        logger.info(f"SQL script {file_path} executed successfully.")
    except FileNotFoundError:
        logger.error(f"SQL file not found: {file_path}")
    except pyodbc.Error as e:
        logger.error(f"Error executing SQL script: {e}")

def setup_database():
    """
    Main function to set up the SQL database: create schema, tables, and load initial data.
    """
    conn = connect_to_sql()
    if conn:
        cursor = conn.cursor()
        try:
            # Step 1: Create schema if not exists
            create_schema_if_not_exists(cursor)

            # Step 2: Create required tables
            create_tables(cursor)
            conn.commit()

            # Step 3: Execute initial setup SQL files (if needed)
            create_schema_path = "Assets/create_head_office_schema.sql"
            load_data_path = "Assets/load_head_office_data.sql"
            execute_sql_file(cursor, create_schema_path)
            execute_sql_file(cursor, load_data_path)
            conn.commit()

        except Exception as e:
            logger.error(f"An error occurred during database setup: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
            logger.info("Database setup completed and connection closed.")

if __name__ == "__main__":
    setup_database()
