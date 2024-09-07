from azure.cosmos import CosmosClient

def connect_to_cosmos():
    endpoint = "https://harrisonshepherd.documents.azure.com:443/"
    key = "cbl5qkgWcGm0xIWYmUyEZXyXRbxXbGIwQvAwuCXkQ2W7C3768eJH6B5kIP3ji8BlhyctiJQQACTvACDb6LGWqg=="
    client = CosmosClient(endpoint, credential=key)
    database = client.get_database_client('CampgroundBookingsDB')
    container = database.get_container_client('Bookings')
    return container

def add_booking(container, booking_data):
    container.upsert_item(booking_data)
