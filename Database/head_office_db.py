# Database/head_office_db.py
import pyodbc
from Database.sql_db import connect_to_sql  # Import connect_to_sql from sql_db.py

def connect_to_head_office():
    """
    Connects to the Head Office SQL database and returns the connection object.
    """
    connection_string = (
        "Driver={ODBC Driver 18 for SQL Server};"
        "Server=campground-server.database.windows.net;"  # Server address for Head Office
        "Database=CampgroundBookingsDB;"                  # Database name
        "Uid=CampgroundAdmin;"                            # Username
        "Pwd=CampgroundDatabasePassword!1;"               # Password
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=60;"                          # Increased connection timeout
    )
    conn = pyodbc.connect(connection_string)
    return conn

def fetch_bookings(conn):
    """
    Fetches bookings from the head_office.booking table and includes customer names.
    :param conn: The connection object to the SQL database.
    :return: A list of booking records.
    """
    cursor = conn.cursor()
    
    query = """
    SELECT 
        b.booking_id, 
        b.customer_id, 
        b.booking_date, 
        b.arrival_date, 
        b.campground_id, 
        b.campsite_size, 
        b.num_campsites, 
        CONCAT(c.first_name, ' ', c.last_name) AS customer_name
    FROM 
        head_office.booking b
    JOIN 
        head_office.customers c ON b.customer_id = c.customer_id
    WHERE 
        b.campground_id = 1121132;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

def update_booking_campground(conn, booking_id, new_campground_id):
    """
    Updates the campground_id of a specific booking in the head_office.booking table.
    :param conn: The connection object to the SQL database.
    :param booking_id: The ID of the booking to be updated.
    :param new_campground_id: The new campground ID to be set.
    """
    cursor = conn.cursor()
    query = "UPDATE head_office.booking SET campground_id = ? WHERE booking_id = ?"
    cursor.execute(query, (new_campground_id, booking_id))
    conn.commit()

if __name__ == "__main__":
    sql_conn = None
    head_office_conn = None
    cosmos_conn = None

    try:
        # Step 1: Connect to SQL database
        sql_conn = connect_to_sql()
        print("Connected to SQL database successfully.")

        # Step 2: Connect to Head Office database and fetch bookings
        head_office_conn = connect_to_head_office()
        print("Connected to Head Office database successfully.")
        bookings = fetch_bookings(head_office_conn)
        print(f"Fetched {len(bookings)} bookings from the head office database.")

        # Step 3: Import other functions inside the function scope to avoid circular imports
        from Utils.booking_processor import process_bookings
        from Database.cosmos_db import connect_to_cosmos, insert_booking_to_cosmos
        from Models.booking import Booking, create_booking_data
        from Utils.campsite_manager import initialize_campsites
        from Utils.summary_manager import generate_summary, display_summary, create_and_insert_summary

        # Step 4: Connect to Cosmos DB
        cosmos_conn = connect_to_cosmos()
        print("Connected to Cosmos DB successfully.")

        # Step 5: Initialize campsites
        campsites = initialize_campsites()

        # Step 6: Process the bookings to allocate campsites
        process_bookings(bookings, campsites, head_office_conn, cosmos_conn, 1121132)

        # Step 7: Generate summary and write back to Head Office
        summary = generate_summary(bookings, campsites)
        display_summary(summary)
        create_and_insert_summary(sql_conn, bookings)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close connections properly
        if sql_conn:
            sql_conn.close()
            print("SQL connection closed.")
        if head_office_conn:
            head_office_conn.close()
            print("Head Office connection closed.")
        print("Cosmos DB connection management is handled by SDK.")