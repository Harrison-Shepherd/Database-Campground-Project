import pyodbc

def connect_to_sql():
    connection_string = (
        "Driver={ODBC Driver 18 for SQL Server};"
        "Server=tcp:campground-server.database.windows.net,1433;"
        "Database=CampgroundBookingsDB;"
        "Uid=CampgroundAdmin;"
        "Pwd=CampgroundDatabasePassword!1;"  # Replace with your actual password
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    conn = pyodbc.connect(connection_string)
    return conn

def insert_summary(conn, summary_data):
    cursor = conn.cursor()
    query = """
        INSERT INTO daily_summary (campground_id, summary_date, total_sales, total_bookings)
        VALUES (?, ?, ?, ?)
    """
    cursor.execute(query, summary_data['campground_id'], summary_data['summary_date'], summary_data['total_sales'], summary_data['total_bookings'])
    conn.commit()
