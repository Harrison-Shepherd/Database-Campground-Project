# Database/head_office_db.py

import pyodbc

# Connect to the Head Office database
def connect_to_head_office():
    connection_string = (
        "Driver={ODBC Driver 18 for SQL Server};"
        "Server=tcp:ict320-task3.database.windows.net,1433;"
        "Database=camping;"
        "Uid=student320;"
        "Pwd=ICT320_student;"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    try:
        conn = pyodbc.connect(connection_string)
        print("Connection to Head Office database successful.")
        return conn
    except pyodbc.Error as e:
        print("Error connecting to Head Office database:", e)
        return None

# Fetch a customer by ID
def get_customer_by_id(conn, customer_id):
    cursor = conn.cursor()
    query = "SELECT * FROM camping.customers WHERE customer_id = ?"
    cursor.execute(query, (customer_id,))
    return cursor.fetchone()

# Fetch bookings by campground_id
def get_bookings_by_campground_id(conn, campground_id):
    cursor = conn.cursor()
    query = "SELECT * FROM camping.booking WHERE campground_id = ?"
    cursor.execute(query, (campground_id,))
    return cursor.fetchall()

# Insert a summary record
def insert_summary(conn, summary):
    cursor = conn.cursor()
    query = """
        INSERT INTO camping.summary (campground_id, summary_date, total_sales, total_bookings)
        VALUES (?, ?, ?, ?)
    """
    cursor.execute(query, (summary.campground_id, summary.summary_date, summary.total_sales, summary.total_bookings))
    conn.commit()
