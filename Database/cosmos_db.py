import uuid
import json
from datetime import datetime
from azure.cosmos import CosmosClient, exceptions
import base64
from Models.booking import Booking  
from Utils.logging_config import logger


#connection_strings.json file 
def load_config():
    """
    Loads the database connection configurations from a JSON file.

    :return: A dictionary of configuration settings.
    """
    with open('Assets/connection_strings.json', 'r') as file:
        return json.load(file)  # Load and return the JSON configuration data

# Function to connect to Cosmos DB
def connect_to_cosmos(container_name):
    """
    Connects to the specified Cosmos DB container.

    :param container_name: Name of the container to connect to.
    :return: Cosmos DB container client.
    """
    # Load the configuration settings for Cosmos DB
    config = load_config()['cosmos_db']
    # Initialize the CosmosClient using endpoint and key from the config
    client = CosmosClient(config['endpoint'], config['key'])
    # Get the database and container clients
    database = client.get_database_client(config['database_name'])
    container = database.get_container_client(container_name)
    logger.info(f"Connected to Cosmos DB container '{container_name}' successfully.")
    return container

# Function to fetch bookings from Cosmos DB
def fetch_cosmos_bookings(container):
    """
    Fetches bookings from the Cosmos DB container and converts them to Booking objects.

    :param container: Cosmos DB container client.
    :return: List of Booking objects from Cosmos DB.
    """
    try:
        query = "SELECT * FROM c"  # Query to fetch all items from the container
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        # Convert the fetched items into Booking objects using the from_dict method
        bookings = [Booking.from_dict(item) for item in items]
        logger.info(f"Fetched {len(bookings)} bookings from Cosmos DB.")
        return bookings
    except exceptions.CosmosHttpResponseError as e:
        # Log any errors 
        logger.error(f"Error fetching bookings from Cosmos DB: {e}")
        return []

# Function to fetch a booking by ID from Cosmos DB
def insert_booking_to_cosmos(container, booking_data):
    """
    Inserts a booking into the Cosmos DB container if it does not already exist.

    :param container: Cosmos DB container client.
    :param booking_data: The booking data to insert.
    """
    booking_id = booking_data.get('booking_id')
    if not booking_id:
        logger.error("Booking data is missing the 'booking_id'. Skipping insertion.")
        return

    # Try to insert the booking into the container
    try:
        # Check if the booking already exists in the container
        query = "SELECT * FROM c WHERE c.booking_id = @booking_id"
        parameters = [{"name": "@booking_id", "value": booking_id}]
        existing_booking = list(container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True))

        if existing_booking:
            logger.info(f"Booking with ID {booking_id} already exists in Cosmos DB. Skipping insertion.")
        else:
            # Generate a unique ID for the item and insert it into the container
            booking_data['id'] = str(uuid.uuid4())
            container.create_item(booking_data)
            logger.info(f"Booking {booking_id} inserted into Cosmos DB successfully.")
    except exceptions.CosmosHttpResponseError as e:
        # Log HTTP errors
        logger.error(f"HTTP error while inserting booking {booking_id} into Cosmos DB: {e.status_code} {e.message}")
    except Exception as e:
        # Log other exceptions
        logger.error(f"Error inserting booking {booking_id} into Cosmos DB: {e}")

# Function to upsert a booking into Cosmos DB
def upsert_booking_pdf_to_cosmos(container, pdf_path, booking_id):
    """
    Upserts a PDF file into the Cosmos DB container with the pdf_id matching the booking_id.

    :param container: Cosmos DB container client.
    :param pdf_path: Path to the PDF file to insert.
    :param booking_id: The booking ID to use as the pdf_id in the Cosmos DB document.
    """
    try:
        # Read the PDF file and encode it as a base64 string
        with open(pdf_path, 'rb') as pdf_file:
            pdf_data = pdf_file.read()
            pdf_data_base64 = base64.b64encode(pdf_data).decode('utf-8')

        # Create a document structure for the PDF and upsert it into the container
        pdf_document = {
            'id': str(booking_id),
            'pdf_id': str(booking_id),
            'filename': pdf_path.split('/')[-1],
            'upload_date': str(datetime.utcnow()),
            'pdf_data': pdf_data_base64
        }

        container.upsert_item(body=pdf_document)
        logger.info(f"PDF {pdf_document['filename']} upserted into Cosmos DB successfully with pdf_id {pdf_document['pdf_id']}.")
    except exceptions.CosmosHttpResponseError as e:
        # Log HTTP errors
        logger.error(f"HTTP error while upserting PDF for booking {booking_id}: {e.status_code} {e.message}")
    except Exception as e:
        # Log other exceptions
        logger.error(f"Error upserting PDF for booking {booking_id}: {e}")

# Function to upsert a summary PDF into Cosmos DB
def upsert_summary_pdf_to_cosmos(container, pdf_path, summary_id):
    """
    Upserts a summary PDF file into the Cosmos DB container with the summary_id.

    :param container: Cosmos DB container client.
    :param pdf_path: Path to the summary PDF file to insert.
    :param summary_id: The summary ID to use as the partition key in the Cosmos DB document.
    """
    try:
        # Read the summary PDF file and encode it as a base64 string
        with open(pdf_path, 'rb') as pdf_file:
            pdf_data = pdf_file.read()
            pdf_data_base64 = base64.b64encode(pdf_data).decode('utf-8')

        # Create a document structure for the summary PDF and upsert it into the container
        pdf_document = {
            'id': str(summary_id),
            'summary_id': str(summary_id),
            'filename': pdf_path.split('/')[-1],
            'upload_date': str(datetime.utcnow()),
            'pdf_data': pdf_data_base64
        }

        container.upsert_item(body=pdf_document)
        logger.info(f"Summary PDF {pdf_document['filename']} upserted into Cosmos DB successfully with summary_id {pdf_document['summary_id']}.")
    except exceptions.CosmosHttpResponseError as e:
        # Log HTTP errors
        logger.error(f"HTTP error while upserting summary PDF: {e.status_code} {e.message}")
    except Exception as e:
        # Log other exceptions
        logger.error(f"Error upserting summary PDF: {e}")

# Function to fetch a PDF file from Cosmos DB
def update_booking_in_cosmos(container, booking_id, update_data):
    """
    Updates a booking document in Cosmos DB with the given booking ID.

    :param container: Cosmos DB container client.
    :param booking_id: The ID of the booking to update.
    :param update_data: A dictionary containing the data to update.
    """
    try:
        # Read the existing booking document from the container
        booking = container.read_item(item=booking_id, partition_key=booking_id)
        booking.update(update_data)  # Update the document with the new data
        container.replace_item(item=booking['id'], body=booking)  # Replace the existing document with the updated version
        logger.info(f"Booking with ID {booking_id} updated successfully in Cosmos DB.")
    except exceptions.CosmosResourceNotFoundError:
        # Log if the booking is not found
        logger.error(f"Booking with ID {booking_id} not found in Cosmos DB.")
    except Exception as e:
        # Log other exceptions
        logger.error(f"Error updating booking {booking_id} in Cosmos DB: {e}")

# Function to delete a booking from Cosmos DB
def delete_booking_from_cosmos(container, booking_id):
    """
    Deletes a booking document from Cosmos DB using the booking ID.

    :param container: Cosmos DB container client.
    :param booking_id: The ID of the booking to delete.
    """
    try:
        # Delete the booking document from the container
        container.delete_item(item=booking_id, partition_key=booking_id)
        logger.info(f"Booking with ID {booking_id} deleted successfully from Cosmos DB.")
    except exceptions.CosmosResourceNotFoundError:
        # Log if the booking is not found
        logger.error(f"Booking with ID {booking_id} not found in Cosmos DB.")
    except Exception as e:
        # Log other exceptions
        logger.error(f"Error deleting booking {booking_id} from Cosmos DB: {e}")
