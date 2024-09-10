import json
import os
import re

def load_config(file_name):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'assets', file_name)
    with open(file_path, 'r') as file:
        return json.load(file)

def get_connection_string(db_type):
    config = load_config('connection_strings.json')
    conn_params = config.get(db_type, {})
    if db_type in ['sql_server', 'head_office']:
        return ';'.join([f"{k}={v}" for k, v in conn_params.items()])
    else:
        return conn_params  # Return the dictionary for Cosmos DB

def prepare_query(sql):
    # Replace commented placeholders with question marks
    return re.sub(r'/\*\w+\*/\S+', '?', sql)

def get_sql_query(filename):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sql_dir = os.path.join(base_dir, 'assets', 'sql')
    file_path = os.path.join(sql_dir, filename)
    
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"SQL file not found: {file_path}")

def load_sql_query(query_name):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'assets', 'sql', f"{query_name}.sql")
    with open(file_path, 'r') as file:
        return file.read()