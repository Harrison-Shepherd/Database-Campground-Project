import pyodbc
import json
import os

def connect_to_head_office():
    """
    Connects to the Head Office SQL database using values from the connection_strings.json file in the Assets folder.

    :return: Connection object to the Head Office SQL database or None if connection fails.
    """
    # Define the path to the connection_strings.json file
    json_file_path = os.path.join('Assets', 'connection_strings.json')

    try:
        # Load connection details from the JSON file
        with open(json_file_path, 'r') as config_file:
            config = json.load(config_file)

        # Extract the head_office connection details
        head_office_config = config['head_office']

        # Define the connection string using parameters from the JSON configuration
        connection_string = (
            f"Driver={head_office_config['driver']};"
            f"Server={head_office_config['server']};"
            f"Database={head_office_config['database']};"
            f"Uid={head_office_config['uid']};"
            f"Pwd={head_office_config['pwd']};"
            f"Encrypt={head_office_config['encrypt']};"
            f"TrustServerCertificate={head_office_config['trust_server_certificate']};"
            f"Connection Timeout={head_office_config['connection_timeout']};"
        )

        # Attempt to connect to the Head Office SQL database
        conn = pyodbc.connect(connection_string)
        print("Connected to Head Office SQL database successfully.")
        return conn  # Return the active database connection object

    except FileNotFoundError as fnf_error:
        print(f"Connection string file not found: {fnf_error}")
        return None

    except json.JSONDecodeError as json_error:
        print(f"Error parsing the connection string JSON file: {json_error}")
        return None

    except pyodbc.Error as db_error:
        print(f"Error connecting to Head Office SQL database: {db_error}")
        return None

def fetch_table_names(conn):
    """
    Fetches and prints the names of all tables in the connected SQL database.

    :param conn: The connection object to the SQL database.
    """
    try:
        cursor = conn.cursor()
        query = """
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE';
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            print("Available tables in the Head Office database:")
            for row in rows:
                print(row[0])
        else:
            print("No tables found in the database.")
        
    except pyodbc.Error as e:
        print(f"Error fetching table names: {e}")

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    conn = connect_to_head_office()
    if conn:
        fetch_table_names(conn)
