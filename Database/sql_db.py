# Database/sql_db.py

import pyodbc

def connect_to_sql():
    # Define your connection string
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
    conn = pyodbc.connect(connection_string)
    return conn

def insert_summary(conn, summary):
    """
    Inserts a daily summary into the summary table.
    
    :param conn: Database connection object.
    :param summary: Dictionary with summary data containing
                    campground_id, summary_date, total_sales, total_bookings.
    """
    cursor = conn.cursor()
    query = """
        INSERT INTO camping.summary (campground_id, summary_date, total_sales, total_bookings)
        VALUES (?, ?, ?, ?)
    """
    cursor.execute(
        query,
        summary['campground_id'],
        summary['summary_date'],
        summary['total_sales'],
        summary['total_bookings']
    )
    conn.commit()
