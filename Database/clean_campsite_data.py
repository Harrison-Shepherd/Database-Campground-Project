import logging
from azure.cosmos import CosmosClient, exceptions
import pyodbc
from Utils.config_loader import get_connection_string
from Utils.logging_config import logger

# Define a filter class to suppress detailed HTTP logs
class SuppressHttpLogsFilter(logging.Filter):
    def filter(self, record):
        # Suppress logs that contain specific HTTP-related keywords
        return 'Request URL:' not in record.getMessage() and \
               'Request headers:' not in record.getMessage() and \
               'Response headers:' not in record.getMessage()

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Apply the custom filter to suppress HTTP logs
suppress_http_filter = SuppressHttpLogsFilter()
for handler in logger.handlers:
    handler.addFilter(suppress_http_filter)

# Suppress detailed logs from specific libraries
logging.getLogger('azure.core.pipeline.policies.http_logging_policy').setLevel(logging.WARNING)
logging.getLogger('azure.cosmos').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)

# Get SQL and Cosmos DB connection details dynamically
SQL_CONNECTION_STRING = get_connection_string('sql_server')
cosmos_config = get_connection_string('cosmos_db')

# Cosmos DB connection details
COSMOS_ENDPOINT = cosmos_config['endpoint']
COSMOS_PRIMARY_KEY = cosmos_config['key']
COSMOS_DATABASE_NAME = cosmos_config['database_name']
BOOKINGS_CONTAINER_NAME = "Bookings"
PDFS_CONTAINER_NAME = "PDFs"
SUMMARY_PDFS_CONTAINER_NAME = "Summary_PDFs"

def clean_sql_campsite_data():
    """
    Cleans campsite-related data from specified SQL tables.

    Deletes all data from the 'camping.booking' and 'camping.summary' tables
    to reset the campsite data in the SQL database.
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
            cursor.execute(f"DELETE FROM {table}")  # Delete all records from the table
            conn.commit()  # Commit changes to the database
            logger.info(f"Cleaned table {table} successfully.")
            print(f"Cleaned table {table} successfully.")

        conn.close()  # Close the SQL connection
        logger.info("SQL campsite data cleaned successfully.")
        print("SQL campsite data cleaned successfully.")
    except Exception as e:
        # Log any errors encountered during the cleanup process
        logger.error(f"An error occurred while cleaning SQL campsite data: {e}")
        print(f"An error occurred while cleaning SQL campsite data: {e}")

def clean_cosmos_container_data(container_name, partition_key_name):
    """
    Cleans data from the specified Cosmos DB container based on the provided partition key.

    :param container_name: Name of the Cosmos DB container.
    :param partition_key_name: The name of the partition key used in the container.
    """
    try:
        # Connect to the specified Cosmos DB container
        client = CosmosClient(COSMOS_ENDPOINT, COSMOS_PRIMARY_KEY)
        database = client.get_database_client(COSMOS_DATABASE_NAME)
        container = database.get_container_client(container_name)

        # Fetch all items from the container
        items = list(container.read_all_items())
        if not items:
            logger.info(f"No items found in {container_name} to clean.")
            print(f"No items found in {container_name} to clean.")
            return

        # Iterate over each item and delete it using the correct partition key
        for item in items:
            item_id = item.get('id')
            partition_key_value = item.get(partition_key_name)

            # Log details for debugging
            logger.info(f"Attempting to delete item with ID: {item_id} and Partition Key: {partition_key_value}")

            try:
                # Delete the item using its ID and the exact partition key value
                container.delete_item(item=item_id, partition_key=partition_key_value)
                logger.info(f"Deleted item with ID {item_id} from {container_name}.")
                print(f"Deleted item with ID {item_id} from {container_name}.")
            except exceptions.CosmosResourceNotFoundError:
                # Handle case where the item was not found or partition key mismatch
                logger.warning(f"Item with ID {item_id} not found; it may have already been deleted or there is a partition key mismatch.")
            except exceptions.CosmosHttpResponseError as e:
                # Log errors that occur during deletion
                logger.error(f"An error occurred while deleting item with ID {item_id}: {e}")
                print(f"An error occurred while deleting item with ID {partition_key_value}: {e}")

        logger.info(f"{container_name} data cleaned successfully.")
    except exceptions.CosmosHttpResponseError as e:
        # Log HTTP response errors from Cosmos DB
        logger.warning(f"An error occurred while cleaning {container_name} data: {e}")
    except Exception as e:
        # Log other exceptions encountered during cleanup
        logger.warning(f"An error occurred while cleaning {container_name} data: {e}")

def main():
    """
    Main function to clean campsite data from SQL and Cosmos DB.

    It sequentially cleans data from the SQL database and various Cosmos DB containers.
    """
    # Clean SQL campsite data
    clean_sql_campsite_data()

    # Clean Cosmos DB Bookings data
    clean_cosmos_container_data(BOOKINGS_CONTAINER_NAME, 'booking_id')

    # Clean Cosmos DB PDFs data
    clean_cosmos_container_data(PDFS_CONTAINER_NAME, 'pdf_id')

    # Clean Cosmos DB Summary PDFs data
    clean_cosmos_container_data(SUMMARY_PDFS_CONTAINER_NAME, 'summary_id')

if __name__ == "__main__":
    main()
