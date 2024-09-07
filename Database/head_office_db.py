import pyodbc

def connect_to_head_office():
    connection_string = (
        "Driver={ODBC Driver 18 for SQL Server};"
        "Server=ict320-task3.database.windows.net;"  # Server address for Head Office
        "Database=camping;"                         # Database name at Head Office
        "Uid=student320;"                           # Username
        "Pwd=ICT320_student;"                       # Password
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    conn = pyodbc.connect(connection_string)
    return conn

def fetch_bookings(conn):
    cursor = conn.cursor()
    query = "SELECT * FROM bookings WHERE campground_id = 1"  # Adjust as necessary
    cursor.execute(query)
    bookings = cursor.fetchall()
    return bookings

def update_booking_campground(conn, booking_id, new_campground_id):
    cursor = conn.cursor()
    query = "UPDATE bookings SET campground_id = ? WHERE booking_id = ?"
    cursor.execute(query, new_campground_id, booking_id)
    conn.commit()
