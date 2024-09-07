# Database/load_head_office_data.py
import pyodbc

def execute_sql_file(conn, file_path):
    """
    Executes an SQL script from a file.
    :param conn: The database connection object.
    :param file_path: Path to the .sql file to be executed.
    """
    try:
        cursor = conn.cursor()
        with open(file_path, 'r') as file:
            sql_script = file.read()

        # Execute the SQL script
        cursor.execute(sql_script)
        conn.commit()
        print(f"SQL script {file_path} executed successfully.")
    except Exception as e:
        print(f"Error executing SQL script: {e}")

def connect_to_sql():
    """
    Connects to the SQL database using provided connection details.
    :return: A connection object.
    """
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

if __name__ == "__main__":
    # Connect to SQL database
    conn = connect_to_sql()

    # Paths to the SQL files in the Assets folder
    create_schema_path = "Assets/create_head_office_schema.sql"
    load_data_path = "Assets/load_head_office_data.sql"

    # Execute the SQL files
    execute_sql_file(conn, create_schema_path)
    execute_sql_file(conn, load_data_path)

    # Close the connection
    conn.close()
    print("Connection closed.")
