from azure.cosmos import CosmosClient, exceptions
from datetime import datetime, timedelta

# Connection details for Cosmos DB
endpoint = "https://harrisonshepherd.documents.azure.com:443/"
primary_key = "cbl5qkgWcGm0xIWYmUyEZXyXRbxXbGIwQvAwuCXkQ2W7C3768eJH6B5kIP3ji8BlhyctiJQQACTvACDb6LGWqg=="
client = CosmosClient(endpoint, primary_key)
database = client.get_database_client('CampgroundBookingsDB')
campsite_container = database.get_container_client('Campsites')

def generate_available_dates(start_date, count):
    """
    Generate a list of available dates starting from a given date.
    :param start_date: The date to start from.
    :param count: Number of weeks to generate dates for.
    :return: List of available dates.
    """
    dates = []
    current_date = start_date
    for _ in range(count):
        dates.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(weeks=1)
    return dates

def create_campsite_data():
    """
    Creates campsite data for different sizes.
    """
    campsite_data = []
    sizes = [('Small', 50), ('Medium', 60), ('Large', 70)]
    start_date = datetime(2024, 10, 1)  # Example start date

    # Create 15 campsites (5 of each size)
    site_number = 1
    for size, rate in sizes:
        for _ in range(5):
            campsite = {
                "id": str(site_number),
                "site_number": site_number,
                "site_size": size,
                "daily_rate": rate,
                "available_dates": generate_available_dates(start_date, 10)  # Generate 10 weeks of availability
            }
            campsite_data.append(campsite)
            site_number += 1
    return campsite_data

def populate_campsites():
    """
    Populate the Campsites collection in Cosmos DB with sample data.
    """
    campsites = create_campsite_data()
    for campsite in campsites:
        try:
            campsite_container.upsert_item(campsite)
            print(f"Inserted campsite {campsite['site_number']} into Cosmos DB.")
        except exceptions.CosmosHttpResponseError as e:
            print(f"An error occurred while inserting campsite {campsite['site_number']}: {e}")

# Run the function to populate the campsites
populate_campsites()
