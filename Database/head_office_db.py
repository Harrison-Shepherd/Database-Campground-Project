from Utils.logging_config import logger
import pyodbc

def connect_to_head_office():
    """
    Connects to the Head Office SQL database and returns the connection object.

    :return: Connection object to the Head Office SQL database or None if connection fails.
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
    try:
        conn = pyodbc.connect(connection_string)
        logger.info("Connected to Head Office SQL database successfully.")
        print("Connected to Head Office SQL database successfully.")

        return conn
    except pyodbc.Error as e:
        logger.error(f"Error connecting to Head Office SQL database: {e}")
        return None

def fetch_bookings(conn):
    """
    Fetches bookings from the head_office.booking table and includes customer names.

    :param conn: The connection object to the SQL database.
    :return: A list of booking records or an empty list if an error occurs.
    """
    try:
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
        logger.info(f"Fetched {len(rows)} bookings from the Head Office database.")
        return rows
    except pyodbc.Error as e:
        logger.warning(f"Error fetching bookings from Head Office database: {e}")
        return []

def update_booking_campground(conn, booking_id, new_campground_id):
    """
    Updates the campground_id of a specific booking in the head_office.booking table.

    :param conn: The connection object to the SQL database.
    :param booking_id: The ID of the booking to be updated.
    :param new_campground_id: The new campground ID to be set.
    """
    try:
        cursor = conn.cursor()
        query = "UPDATE head_office.booking SET campground_id = ? WHERE booking_id = ?"
        cursor.execute(query, (new_campground_id, booking_id))
        conn.commit()
        logger.info(f"Booking {booking_id} updated with new campground ID {new_campground_id} successfully.")
    except pyodbc.Error as e:
        logger.warning(f"Error updating booking {booking_id} in Head Office database: {e}")
