# Database/cosmos_db.py
import uuid
from azure.cosmos import CosmosClient, exceptions

def connect_to_cosmos():
    """
    Connects to the Cosmos DB and returns the container client.
    :return: Cosmos DB container client.
    """
    # Define the connection parameters for Cosmos DB
    endpoint = "https://harrisonshepherd.documents.azure.com:443/"
    primary_key = "cbl5qkgWcGm0xIWYmUyEZXyXRbxXbGIwQvAwuCXkQ2W7C3768eJH6B5kIP3ji8BlhyctiJQQACTvACDb6LGWqg=="
    client = CosmosClient(endpoint, primary_key)
    database = client.get_database_client('CampgroundBookingsDB')
    container = database.get_container_client('Bookings')
    return container

def fetch_cosmos_bookings(container):
    """
    Fetches bookings from the Cosmos DB container.
    :param container: Cosmos DB container client.
    :return: List of booking documents from Cosmos DB.
    """
    try:
        query = "SELECT * FROM Bookings"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        return items
    except exceptions.CosmosHttpResponseError as e:
        print(f"An error occurred while fetching bookings: {e}")
        return []

def insert_booking_to_cosmos(client, booking_data):
    """
    Inserts a booking into the Cosmos DB container.
    :param client: Cosmos DB container client.
    :param booking_data: The booking data to insert.
    """
    try:
        # Ensure the booking_data contains a unique 'id'
        booking_data['id'] = str(uuid.uuid4())  # Generates a unique ID
        client.create_item(booking_data)
        print("Booking inserted into Cosmos DB successfully.")
    except exceptions.CosmosHttpResponseError as e:
        print(f"An error occurred while inserting the booking: {e}")
    except Exception as e:
        print(f"An error occurred while inserting the booking: {e}")

def update_booking_in_cosmos(client, booking_id, update_data):
    """
    Updates a booking document in Cosmos DB with the given booking ID.
    :param client: Cosmos DB container client.
    :param booking_id: The ID of the booking to update.
    :param update_data: A dictionary containing the data to update.
    """
    try:
        # Fetch the existing booking document by ID
        booking = client.read_item(item=booking_id, partition_key=booking_id)
        # Update the booking document with the provided data
        for key, value in update_data.items():
            booking[key] = value
        client.replace_item(item=booking_id, body=booking)
        print(f"Booking with ID {booking_id} updated successfully.")
    except exceptions.CosmosResourceNotFoundError:
        print(f"Booking with ID {booking_id} not found.")
    except Exception as e:
        print(f"An error occurred while updating the booking: {e}")

def delete_booking_from_cosmos(client, booking_id):
    """
    Deletes a booking document from Cosmos DB using the booking ID.
    :param client: Cosmos DB container client.
    :param booking_id: The ID of the booking to delete.
    """
    try:
        # Attempt to delete the booking document by ID
        client.delete_item(item=booking_id, partition_key=booking_id)
        print(f"Booking with ID {booking_id} deleted successfully.")
    except exceptions.CosmosResourceNotFoundError:
        print(f"Booking with ID {booking_id} not found.")
    except Exception as e:
        print(f"An error occurred while deleting the booking: {e}")
