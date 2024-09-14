# Database/cosmos_db.py
import uuid
import json
import logging
from datetime import datetime
from azure.cosmos import CosmosClient, exceptions
import base64
from Models.booking import Booking  # Ensure you import the Booking model


# Configure logging to suppress verbose outputs from external libraries and show only necessary information
logging.basicConfig(level=logging.INFO, format='%(message)s')
logging.getLogger('azure').setLevel(logging.WARNING)  # Suppresses lower-level logs from Azure SDK

def load_config():
    """
    Loads the database connection configurations from a JSON file.
    :return: A dictionary of configuration settings.
    """
    with open('Assets/connection_strings.json', 'r') as file:
        return json.load(file)

def connect_to_cosmos(container_name):
    """
    Connects to the specified Cosmos DB container.
    
    :param container_name: Name of the container to connect to.
    :return: Cosmos DB container client.
    """
    config = load_config()['cosmos_db']
    client = CosmosClient(config['endpoint'], config['key'])
    database = client.get_database_client(config['database_name'])
    container = database.get_container_client(container_name)
    return container

def fetch_cosmos_bookings(container):
    """
    Fetches bookings from the Cosmos DB container and converts them to Booking objects.
    :param container: Cosmos DB container client.
    :return: List of Booking objects from Cosmos DB.
    """
    try:
        query = "SELECT * FROM c"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        bookings = [Booking.from_dict(item) for item in items]  # Convert dictionaries to Booking objects
        logging.info(f"Fetched {len(bookings)} bookings from Cosmos DB.")
        return bookings
    except exceptions.CosmosHttpResponseError as e:
        logging.error(f"An error occurred while fetching bookings: {e}")
        return []

def insert_booking_to_cosmos(container, booking_data):
    """
    Inserts a booking into the Cosmos DB container if it does not already exist.
    :param container: Cosmos DB container client.
    :param booking_data: The booking data to insert.
    """
    booking_id = booking_data.get('booking_id')
    if not booking_id:
        logging.error("Booking data is missing the 'booking_id'. Skipping insertion.")
        return

    try:
        # Check if the booking already exists
        query = "SELECT * FROM c WHERE c.booking_id = @booking_id"
        parameters = [{"name": "@booking_id", "value": booking_id}]
        existing_booking = list(container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True))

        if existing_booking:
            logging.info(f"Booking with ID {booking_id} already exists in Cosmos DB. Skipping insertion.")
        else:
            booking_data['id'] = str(uuid.uuid4())  # Generates a unique ID for the Cosmos DB item
            container.create_item(booking_data)
            logging.info(f"Booking {booking_id} inserted into Cosmos DB successfully.")
    except exceptions.CosmosHttpResponseError as e:
        logging.error(f"An HTTP error occurred while inserting the booking {booking_id}: {e.status_code} {e.message}")
    except Exception as e:
        logging.error(f"An error occurred while inserting the booking {booking_id}: {e}")

def insert_pdf_to_cosmos(container, pdf_path):
    """
    Inserts a PDF file into the Cosmos DB container.

    :param container: Cosmos DB container client.
    :param pdf_path: Path to the PDF file to insert.
    """
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_data = pdf_file.read()
            pdf_data_base64 = base64.b64encode(pdf_data).decode('utf-8')  # Encode as base64 string

        # Create a document with the PDF data and metadata
        pdf_document = {
            'id': str(uuid.uuid4()),  # Adding 'id' field as required by Cosmos DB
            'pdf_id': str(uuid.uuid4()),  # Use this as the partition key
            'filename': pdf_path.split('/')[-1],  # Extract the filename from the path
            'upload_date': str(datetime.utcnow()),  # Store the upload date
            'pdf_data': pdf_data_base64  # Store the encoded PDF data as a base64 string
        }

        # Insert the document into the Cosmos DB container
        container.create_item(body=pdf_document)
        logging.info(f"PDF {pdf_document['filename']} inserted into Cosmos DB successfully.")
    
    except exceptions.CosmosHttpResponseError as e:
        logging.error(f"An HTTP error occurred while inserting the PDF: {e.status_code} {e.message}")
    except Exception as e:
        logging.error(f"An error occurred while inserting the PDF: {e}")

def update_booking_in_cosmos(container, booking_id, update_data):
    """
    Updates a booking document in Cosmos DB with the given booking ID.
    :param container: Cosmos DB container client.
    :param booking_id: The ID of the booking to update.
    :param update_data: A dictionary containing the data to update.
    """
    try:
        # Fetch the existing booking document by ID
        booking = container.read_item(item=booking_id, partition_key=booking_id)
        # Update the booking document with the provided data
        booking.update(update_data)
        container.replace_item(item=booking['id'], body=booking)
        logging.info(f"Booking with ID {booking_id} updated successfully.")
    except exceptions.CosmosResourceNotFoundError:
        logging.error(f"Booking with ID {booking_id} not found.")
    except Exception as e:
        logging.error(f"An error occurred while updating the booking {booking_id}: {e}")

def delete_booking_from_cosmos(container, booking_id):
    """
    Deletes a booking document from Cosmos DB using the booking ID.
    :param container: Cosmos DB container client.
    :param booking_id: The ID of the booking to delete.
    """
    try:
        # Attempt to delete the booking document by ID
        container.delete_item(item=booking_id, partition_key=booking_id)
        logging.info(f"Booking with ID {booking_id} deleted successfully.")
    except exceptions.CosmosResourceNotFoundError:
        logging.error(f"Booking with ID {booking_id} not found.")
    except Exception as e:
        logging.error(f"An error occurred while deleting the booking {booking_id}: {e}")
