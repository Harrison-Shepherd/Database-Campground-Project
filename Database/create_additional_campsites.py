# create_additional_campsites.py
from azure.cosmos import CosmosClient, exceptions
import uuid

# Cosmos DB connection details
ENDPOINT = "https://harrisonshepherd.documents.azure.com:443/"
PRIMARY_KEY = "cbl5qkgWcGm0xIWYmUyEZXyXRbxXbGIwQvAwuCXkQ2W7C3768eJH6B5kIP3ji8BlhyctiJQQACTvACDb6LGWqg=="

def connect_to_cosmos():
    """
    Connect to Cosmos DB and return the container client.
    """
    client = CosmosClient(ENDPOINT, PRIMARY_KEY)
    database = client.get_database_client('CampgroundBookingsDB')
    container = database.get_container_client('Campsites')
    return container

def create_campsites(container):
    """
    Create additional campsites in Cosmos DB.
    """
    campsites = []

    # Add 10 Small campsites
    for i in range(1, 11):
        campsites.append({
            'id': str(uuid.uuid4()),
            'site_number': i,
            'size': 'Small',
            'rate_per_night': 50,
            'available_dates': []  # Initialize with empty available dates
        })

    # Add 10 Medium campsites
    for i in range(11, 21):
        campsites.append({
            'id': str(uuid.uuid4()),
            'site_number': i,
            'size': 'Medium',
            'rate_per_night': 60,
            'available_dates': []
        })

    # Add 10 Large campsites
    for i in range(21, 31):
        campsites.append({
            'id': str(uuid.uuid4()),
            'site_number': i,
            'size': 'Large',
            'rate_per_night': 70,
            'available_dates': []
        })

    # Insert each campsite into the Cosmos DB container
    for campsite in campsites:
        try:
            container.create_item(body=campsite)
            print(f"Campsite {campsite['site_number']} added successfully.")
        except exceptions.CosmosResourceExistsError:
            print(f"Campsite {campsite['site_number']} already exists in the database.")
        except exceptions.CosmosHttpResponseError as e:
            print(f"Failed to add campsite {campsite['site_number']}: {e}")

if __name__ == "__main__":
    container = connect_to_cosmos()
    create_campsites(container)
