# Database/head_office_db.py
import pyodbc

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
    Fetches bookings from the head_office.booking table where campground_id matches your student ID.
    :param conn: The connection object to the SQL database.
    :return: A list of bookings fetched from the database.
    """
    cursor = conn.cursor()
    # Adjust the query to match your specific campground_id (student ID)
    query = "SELECT * FROM head_office.booking WHERE campground_id = 1121132;"  # Adjust if needed
    cursor.execute(query)
    bookings = cursor.fetchall()
    return bookings

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
    try:
        # Attempt to connect to the Head Office database
        conn = connect_to_head_office()
        print("Connected to Head Office database successfully.")
        
        # Fetch and print the number of bookings
        bookings = fetch_bookings(conn)
        print(f"Fetched {len(bookings)} bookings from the database.")
        
        # Example of updating a booking's campground ID (using the first booking fetched)
        if bookings:
            first_booking_id = bookings[0][0]  # Assuming the first column is booking_id
            update_booking_campground(conn, first_booking_id, 1121132)  # Replace 1121132 with your student ID
            print(f"Updated booking {first_booking_id} to new campground ID 1121132.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Ensure the connection is closed to avoid resource leaks
        if conn:
            conn.close()
            print("Connection closed.")
