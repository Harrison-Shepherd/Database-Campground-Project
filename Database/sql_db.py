# sql_db.py

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

def test_connection():
    try:
        conn = connect_to_sql()
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 1 * FROM daily_summary")  # Adjust this query as per your table structure
        row = cursor.fetchone()
        print("Connection successful. Sample data:", row)
    except Exception as e:
        print("Error connecting to SQL database:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    test_connection()
