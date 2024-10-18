from Utils.logging_config import logger
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
        logger.info("Connected to Head Office SQL database successfully.")
        print("Connected to Head Office SQL database successfully.")
        return conn  # Return the active database connection object

    except FileNotFoundError as fnf_error:
        logger.error(f"Connection string file not found: {fnf_error}")
        print(f"Connection string file not found: {fnf_error}")
        return None

    except json.JSONDecodeError as json_error:
        logger.error(f"Error parsing the connection string JSON file: {json_error}")
        print(f"Error parsing the connection string JSON file: {json_error}")
        return None

    except pyodbc.Error as db_error:
        logger.error(f"Error connecting to Head Office SQL database: {db_error}")
        print(f"Error connecting to Head Office SQL database: {db_error}")
        return None

def fetch_bookings(conn):
    """
    Fetches bookings from the head_office.booking table and includes customer names.

    :param conn: The connection object to the SQL database.
    :return: A list of booking records or an empty list if an error occurs.
    """
    try:
        cursor = conn.cursor()
        # SQL query to fetch booking details and join with customer information
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
        cursor.execute(query)  # Execute the query
        rows = cursor.fetchall()  # Fetch all the rows from the executed query
        logger.info(f"Fetched {len(rows)} bookings from the Head Office database.")
        return rows  # Return the fetched booking records

    except pyodbc.Error as e:
        # Log a warning if fetching the bookings fails
        logger.warning(f"Error fetching bookings from Head Office database: {e}")
        return []  # Return an empty list if an error occurs

def update_booking_campground(conn, booking_id, new_campground_id):
    """
    Updates the campground_id of a specific booking in the head_office.booking table.

    :param conn: The connection object to the SQL database.
    :param booking_id: The ID of the booking to be updated.
    :param new_campground_id: The new campground ID to be set.
    """
    try:
        cursor = conn.cursor()
        # SQL query to update the campground_id of a specific booking
        query = "UPDATE head_office.booking SET campground_id = ? WHERE booking_id = ?"
        cursor.execute(query, (new_campground_id, booking_id))  # Execute the update query with parameters
        conn.commit()  # Commit the changes to the database
        logger.info(f"Booking {booking_id} updated with new campground ID {new_campground_id} successfully.")

    except pyodbc.Error as e:
        # Log a warning if updating the booking fails
        logger.warning(f"Error updating booking {booking_id} in Head Office database: {e}")
