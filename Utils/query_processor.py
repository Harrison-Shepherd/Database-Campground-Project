from Utils.config_loader import get_connection_string
import pyodbc

def connect_to_database(db_type):
    """
    Generic function to connect to a database.
    :param db_type: String indicating the database type ('sql_server' or 'head_office')
    :return: Connection object to the database.
    """
    try:
        connection_string = get_connection_string(db_type)
        conn = pyodbc.connect(connection_string, autocommit=False)
        print(f"Connected to {db_type} database successfully.")
        return conn
    except Exception as e:
        print(f"Error connecting to {db_type} database: {e}")
        return None

def execute_query(conn, query, params=None):
    """
    Execute a SQL query with optional parameters.
    :param conn: Database connection object.
    :param query: SQL query string.
    :param params: Optional tuple of parameters for the query.
    :return: Cursor object with query results.
    """
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
