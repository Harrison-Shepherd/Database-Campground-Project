import sys
import json
from azure.cosmos import CosmosClient, exceptions
from Utils.logging_config import logger  

# loads connection string
def load_config():
    try:
        with open('Assets/connection_strings.json', 'r') as file:
            return json.load(file)['cosmos_db']
    except FileNotFoundError:
        logger.error("Configuration file not found.")
        sys.exit(1)

# Connects to the Cosmos DB container
def connect_to_cosmos(container_name):
    config = load_config()
    client = CosmosClient(config['endpoint'], config['key'])
    database = client.get_database_client(config['database_name'])
    container = database.get_container_client(container_name)
    return container

# Function to retrieve booking details by booking ID or customer name
def retrieve_booking(cosmos_container, identifier):
    try:
        # Check if identifier is numeric; if so, search by booking ID; otherwise, search by customer name
        if identifier.isdigit():
            query = "SELECT * FROM c WHERE c.booking_id = @booking_id"
            parameters = [{"name": "@booking_id", "value": int(identifier)}]
        else:
            query = "SELECT * FROM c WHERE CONTAINS(c.customer_name, @customer_name)"
            parameters = [{"name": "@customer_name", "value": identifier}]

        items = list(cosmos_container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True))

        if items:
            for item in items:
                print(f"\nBooking ID: {item.get('booking_id')}")
                print(f"Customer Name: {item.get('customer_name')}")
                print(f"Arrival Date: {item.get('arrival_date')}")
                print(f"Campsite Size: {item.get('campsite_size')}")
                print(f"Total Cost: ${item.get('total_cost'):.2f}")
                print(f"Number of Campsites: {item.get('num_campsites')}")
                # Display campsite allocations correctly
                allocations = item.get('campsite_allocations', 'None')
                if isinstance(allocations, list) and allocations:
                    print(f"Campsite Allocations: {', '.join(map(str, allocations))}\n")
                else:
                    print(f"Campsite Allocations: None\n")
        else:
            print(f"No bookings found for identifier: {identifier}")
    except exceptions.CosmosHttpResponseError as e:
        logger.error(f"Error retrieving booking from Cosmos DB: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

def main():
    # Connect to the Cosmos DB container
    container_name = "Bookings" 
    cosmos_container = connect_to_cosmos(container_name)

    print("Welcome to the Booking Retrieval System!")
    identifier = input("Enter Booking ID or Customer Name to retrieve booking details: ").strip()

    # Retrieve and display booking details
    retrieve_booking(cosmos_container, identifier)

if __name__ == "__main__":
    main()
