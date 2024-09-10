# Utils/config_loader.py
import json
import os
import re

def load_config(file_name):
    """
    Loads the configuration JSON file from the assets directory.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'assets', file_name)
    with open(file_path, 'r') as file:
        return json.load(file)

def get_connection_string(db_type):
    """
    Retrieves the connection string or configuration dictionary for the specified database type.
    """
    config = load_config('connection_strings.json')
    conn_params = config.get(db_type, {})
    if db_type in ['sql_server', 'head_office']:
        # Generate a connection string for SQL-based databases
        return ';'.join([f"{k}={v}" for k, v in conn_params.items() if v])  # Exclude empty values
    else:
        # Return connection parameters for non-SQL databases like Cosmos DB
        return conn_params

def prepare_query(sql):
    """
    Replaces placeholders with question marks in SQL queries.
    """
    return re.sub(r'/\*\w+\*/\S+', '?', sql)

def get_sql_query(filename):
    """
    Reads a SQL file from the assets/sql directory.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sql_dir = os.path.join(base_dir, 'assets', 'sql')
    file_path = os.path.join(sql_dir, filename)

    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"SQL file not found: {file_path}")

def load_sql_query(query_name):
    """
    Loads a specific SQL query from the assets/sql directory.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'assets', 'sql', f"{query_name}.sql")
    with open(file_path, 'r') as file:
        return file.read()
