import json
import os
import re
from Utils.logging_config import logger

def load_config(file_name):
    """
    Loads the configuration JSON file from the assets folder.

    :param file_name: The name of the JSON configuration file.
    :return: A dictionary containing the configuration settings.
    :raises FileNotFoundError: If the configuration file does not exist.
    :raises JSONDecodeError: If the file content is not valid JSON.
    """
    # Defines the base directory and file path for the configuration file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'assets', file_name)
    
    try:
        # Open and read the JSON configuration file
        with open(file_path, 'r') as file:
            config = json.load(file)
            logger.info(f"Configuration loaded from {file_name}.")
            return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {file_path}")
        raise
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from the configuration file: {file_path}")
        raise

# helps to normalise connection setup
def get_connection_string(db_type):
    """
    Retrieves the connection string or configuration dictionary for the specified database type.

    :param db_type: The type of database (e.g., 'sql_server', 'head_office', or other).
    :return: A connection string for SQL-based databases or a configuration dictionary for non-SQL databases.
    :raises KeyError: If the specified database type is not found in the configuration.
    :raises Exception: For other errors encountered during the retrieval process.
    """
    try:
        # Load connection settings from the configuration file
        config = load_config('connection_strings.json')
        conn_params = config.get(db_type, {})
        
        if db_type in ['sql_server', 'head_office']:
            # Generate a connection string for SQL-based databases, excluding empty values
            connection_string = ';'.join([f"{k}={v}" for k, v in conn_params.items() if v])
            logger.info(f"Connection string prepared for {db_type}.")
            return connection_string
        else:
            # Return connection parameters for non-SQL databases like Cosmos DB
            logger.info(f"Configuration parameters retrieved for {db_type}.")
            return conn_params
    except KeyError:
        logger.error(f"Database type {db_type} not found in the configuration.")
        raise
    except Exception as e:
        logger.error(f"Error retrieving connection string for {db_type}: {e}")
        raise

def prepare_query(sql): #TODO not sure if needed anymore?, sql files just have "?" placeholders for pyodbc
    """
    Replaces placeholders with question marks in SQL queries.

    :param sql: The SQL query string with placeholders.
    :return: The SQL query with placeholders replaced by '?'.
    """
    # Replace placeholders (e.g., /*param*/value) in SQL with '?'
    prepared_sql = re.sub(r'/\*\w+\*/\S+', '?', sql)
    logger.info("SQL query prepared with placeholders.")
    return prepared_sql

def get_sql_query(filename):
    """
    Reads a SQL file from the assets/sql directory.

    :param filename: The name of the SQL file to read.
    :return: The content of the SQL file as a string.
    :raises FileNotFoundError: If the SQL file does not exist.
    """
    # Define the base directory and file path for the SQL file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sql_dir = os.path.join(base_dir, 'assets', 'sql')
    file_path = os.path.join(sql_dir, filename)

    try:
        # Open and read the SQL file
        with open(file_path, 'r') as file:
            sql_query = file.read()
            logger.info(f"SQL query loaded from {filename}.")
            return sql_query
    except FileNotFoundError:
        logger.error(f"SQL file not found: {file_path}")
        raise

def load_sql_query(query_name):
    """
    Loads a specific SQL query from the assets/sql directory.

    :param query_name: The name of the SQL query file without extension.
    :return: The content of the SQL query file as a string.
    :raises FileNotFoundError: If the SQL file does not exist.
    :raises Exception: For other errors encountered during the file read operation.
    """
    # Define the base directory and file path for the SQL query file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'assets', 'sql', f"{query_name}.sql")
    
    try:
        # Open and read the SQL query file
        with open(file_path, 'r') as file:
            sql_query = file.read()
            logger.info(f"SQL query {query_name} loaded successfully.")
            return sql_query
    except FileNotFoundError:
        logger.error(f"SQL file not found: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Error loading SQL query {query_name}: {e}")
        raise
