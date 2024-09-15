import logging
from azure.cosmos import CosmosClient, exceptions
import pyodbc
from Utils.config_loader import get_connection_string

# Define a filter class to suppress detailed HTTP logs
class SuppressHttpLogsFilter(logging.Filter):
    def filter(self, record):
        # Suppress logs that contain specific HTTP-related keywords
        if 'Request URL:' in record.getMessage() or 'Request headers:' in record.getMessage() or 'Response headers:' in record.getMessage():
            return False
        return True

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Filter specific detailed logs from Azure SDK
logging.getLogger('azure.core.pipeline.policies.http_logging_policy').setLevel(logging.WARNING)

# Apply the custom filter to suppress HTTP logs
suppress_http_filter = SuppressHttpLogsFilter()
for handler in logger.handlers:
    handler.addFilter(suppress_http_filter)

# Suppress detailed logs from specific libraries
logging.getLogger('azure.cosmos').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)

# Get SQL and Cosmos DB connection details dynamically
SQL_CONNECTION_STRING = get_connection_string('sql_server')
cosmos_config = get_connection_string('cosmos_db')

COSMOS_ENDPOINT = cosmos_config['endpoint']
COSMOS_PRIMARY_KEY = cosmos_config['key']
COSMOS_DATABASE_NAME = cosmos_config['database_name']
BOOKINGS_CONTAINER_NAME = "Bookings"
PDFS_CONTAINER_NAME = "PDFs"

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

def clean_cosmos_container_data(container_name, partition_key_name):
    """
    Cleans data from the specified Cosmos DB container based on the provided partition key.

    :param container_name: Name of the Cosmos DB container.
    :param partition_key_name: The name of the partition key used in the container.
    """
    try:
        client = CosmosClient(COSMOS_ENDPOINT, COSMOS_PRIMARY_KEY)
        database = client.get_database_client(COSMOS_DATABASE_NAME)
        container = database.get_container_client(container_name)

        # Fetch all items from the container
        items = list(container.read_all_items())
        if not items:
            logging.info(f"No items found in {container_name} to clean.")
            return

        # Iterate over each item and delete it using the correct partition key
        for item in items:
            item_id = item.get('id')
            partition_key_value = item.get(partition_key_name)

            # Log details for debugging
            logging.info(f"Attempting to delete item with ID: {item_id} and Partition Key: {partition_key_value}")

            try:
                # Delete the item using its ID and the exact partition key value
                container.delete_item(item=item_id, partition_key=partition_key_value)
                logging.info(f"Deleted item with ID {item_id} from {container_name}.")
            except exceptions.CosmosResourceNotFoundError:
                logging.warning(f"Item with ID {item_id} not found; it may have already been deleted or there is a partition key mismatch.")
            except exceptions.CosmosHttpResponseError as e:
                logging.error(f"An error occurred while deleting item with ID {item_id}: {e}")

        logging.info(f"{container_name} data cleaned successfully.")
    except exceptions.CosmosHttpResponseError as e:
        logging.error(f"An error occurred while cleaning {container_name} data: {e}")
    except Exception as e:
        logging.error(f"An error occurred while cleaning {container_name} data: {e}")

def main():
    # Clean SQL campsite data
    clean_sql_campsite_data()

    # Clean Cosmos DB Bookings data
    clean_cosmos_container_data(BOOKINGS_CONTAINER_NAME, 'booking_id')

    # Clean Cosmos DB PDFs data
    clean_cosmos_container_data(PDFS_CONTAINER_NAME, 'pdf_id')

if __name__ == "__main__":
    main()
