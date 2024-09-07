# Database/head_office_db.py
import pyodbc

def connect_to_head_office():
    """
    Connects to the Head Office database. This connection is currently set up for your local SQL database for testing.
    Update the connection string when switching to the official Head Office database.
    :return: Connection object
    """
    # Connection string updated for local testing; change server and database when the main database is available
    connection_string = (
        "Driver={ODBC Driver 18 for SQL Server};"
        "Server=campground-server.database.windows.net;"  # Use your local server if different
        "Database=CampgroundBookingsDB;"                  # Ensure this is the correct database name
        "Uid=CampgroundAdmin;"                            # Your SQL credentials
        "Pwd=CampgroundDatabasePassword!1;"               # Your SQL password
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    
    try:
        conn = pyodbc.connect(connection_string)
        print("Connected to Head Office database successfully.")
        return conn
    except Exception as e:
        print(f"Error connecting to Head Office database: {e}")
        return None


def fetch_bookings(conn):
    """
    Fetches bookings from the Head Office database where the campground_id is set to 1.
    :param conn: Connection object
    :return: List of bookings
    """
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM camping.booking WHERE campground_id = 1"  # Make sure the schema and table exist
        cursor.execute(query)
        bookings = cursor.fetchall()
        print(f"Fetched {len(bookings)} bookings from the database.")
        return bookings
    except Exception as e:
        print(f"Error fetching bookings: {e}")
        return []


def update_booking_campground(conn, booking_id, new_campground_id):
    """
    Updates a booking's campground_id in the Head Office database.
    :param conn: Connection object
    :param booking_id: The ID of the booking to update
    :param new_campground_id: New campground ID (e.g., your student ID)
    """
    try:
        cursor = conn.cursor()
        query = "UPDATE camping.booking SET campground_id = ? WHERE booking_id = ?"
        cursor.execute(query, (new_campground_id, booking_id))
        conn.commit()
        print(f"Updated booking {booking_id} to new campground ID {new_campground_id}.")
    except Exception as e:
        print(f"Error updating booking: {e}")


def close_connection(conn):
    """
    Closes the database connection.
    :param conn: Connection object
    """
    try:
        conn.close()
        print("Connection closed.")
    except:
        print("Error closing the connection.")


if __name__ == "__main__":
    # Test the functions
    connection = connect_to_head_office()
    if connection:
        bookings = fetch_bookings(connection)
        for booking in bookings:
            booking_id = booking[0]  # Assuming booking ID is the first column
            update_booking_campground(connection, booking_id, 1121132)  # Replace with your actual campground number
        close_connection(connection)
