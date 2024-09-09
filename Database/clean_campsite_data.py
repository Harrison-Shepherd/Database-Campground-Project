# clean_campsite_data.py

from azure.cosmos import CosmosClient, exceptions
import pyodbc
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# SQL Database Connection Details
SQL_CONNECTION_STRING = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=campground-server.database.windows.net;"
    "Database=CampgroundBookingsDB;"
    "Uid=CampgroundAdmin;"
    "Pwd=CampgroundDatabasePassword!1;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

# Cosmos DB Connection Details
COSMOS_ENDPOINT = "https://harrisonshepherd.documents.azure.com:443/"
COSMOS_PRIMARY_KEY = "cbl5qkgWcGm0xIWYmUyEZXyXRbxXbGIwQvAwuCXkQ2W7C3768eJH6B5kIP3ji8BlhyctiJQQACTvACDb6LGWqg=="
COSMOS_DATABASE_NAME = "CampgroundBookingsDB"
COSMOS_CONTAINER_NAME = "Bookings"

def clean_sql_campsite_data():
    """
    Cleans campsite-related data from SQL tables.
    """
    try:
        conn = pyodbc.connect(SQL_CONNECTION_STRING)
        cursor = conn.cursor()

        # List of tables to clean
        tables_to_clean = [
            "camping.booking",
            "camping.summary"
        ]

        # Iterate over each table and delete the data
        for table in tables_to_clean:
            cursor.execute(f"DELETE FROM {table}")
            conn.commit()
            logging.info(f"Cleaned table {table} successfully.")

        conn.close()
        logging.info("SQL campsite data cleaned successfully.")
    except Exception as e:
        logging.error(f"An error occurred while cleaning SQL campsite data: {e}")

def clean_cosmos_campsite_data():
    """
    Cleans campsite-related data from the Cosmos DB container.
    """
    try:
        client = CosmosClient(COSMOS_ENDPOINT, COSMOS_PRIMARY_KEY)
        database = client.get_database_client(COSMOS_DATABASE_NAME)
        container = database.get_container_client(COSMOS_CONTAINER_NAME)

        # Fetch all items from the container
        items = list(container.read_all_items())
        if not items:
            logging.info("No items found in Cosmos DB to clean.")
            return

        # Delete each item individually
        for item in items:
            try:
                container.delete_item(item=item['id'], partition_key=item['booking_id'])
                logging.info(f"Deleted item with ID {item['id']} from Cosmos DB.")
            except exceptions.CosmosResourceNotFoundError:
                logging.warning(f"Item with ID {item['id']} not found; it may have already been deleted.")
            except exceptions.CosmosHttpResponseError as e:
                logging.error(f"An error occurred while deleting item with ID {item['id']}: {e}")

        logging.info("Cosmos DB campsite data cleaned successfully.")
    except exceptions.CosmosHttpResponseError as e:
        logging.error(f"An error occurred while cleaning Cosmos DB campsite data: {e}")
    except Exception as e:
        logging.error(f"An error occurred while cleaning Cosmos DB campsite data: {e}")

def main():
    # Clean SQL campsite data
    clean_sql_campsite_data()

    # Clean Cosmos DB campsite data
    clean_cosmos_campsite_data()

if __name__ == "__main__":
    main()
