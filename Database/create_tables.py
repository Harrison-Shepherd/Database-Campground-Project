# Database/create_tables.py

import pyodbc

def connect_to_sql():
    """
    Connects to the SQL Server database.
    """
    try:
        connection_string = (
            "Driver={ODBC Driver 18 for SQL Server};"
            "Server=campground-server.database.windows.net;"  # Replace with your server name
            "Database=CampgroundBookingsDB;"                  # Replace with your database name
            "Uid=CampgroundAdmin;"                            # Replace with your username
            "Pwd=CampgroundDatabasePassword!1;"               # Replace with your password
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
        )
        conn = pyodbc.connect(connection_string)
        print("Connected to SQL database successfully.")
        return conn
    except Exception as e:
        print(f"Error connecting to SQL database: {e}")
        return None

def create_schema_if_not_exists(cursor):
    """
    Creates the schema 'camping' if it does not exist.
    """
    try:
        # SQL command to check if schema exists and create it if it does not
        query = """
        IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'camping')
        BEGIN
            EXEC('CREATE SCHEMA camping');
        END
        """
        cursor.execute(query)
        print("Schema 'camping' checked/created successfully.")
    except Exception as e:
        print(f"Error creating schema: {e}")

def create_tables(conn):
    """
    Creates the necessary tables in the SQL database.
    """
    cursor = conn.cursor()

    # Create the schema if it doesn't exist
    create_schema_if_not_exists(cursor)

    # SQL commands to create the required tables
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
        # Execute the commands to create tables
        cursor.execute(create_customers_table)
        cursor.execute(create_booking_table)
        cursor.execute(create_summary_table)
        conn.commit()
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")
        conn.rollback()

def main():
    conn = connect_to_sql()
    if conn:
        create_tables(conn)
        conn.close()

if __name__ == "__main__":
    main()
