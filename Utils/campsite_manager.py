# If needed, add functions to validate campsite data, check availability, etc.
# Utils/campsite_manager.py 

from Models.campsite import Campsite

def initialize_campsites():
    # Create a list of campsites with more entries
    campsites = []

    # Add 10 Small campsites
    for i in range(1, 11):
        campsites.append(Campsite(site_number=i, size='Small', rate_per_night=50))

    # Add 10 Medium campsites
    for i in range(11, 21):
        campsites.append(Campsite(site_number=i, size='Medium', rate_per_night=60))

    # Add 10 Large campsites
    for i in range(21, 31):
        campsites.append(Campsite(site_number=i, size='Large', rate_per_night=70))

    # Add more campsites if needed, adjust numbers and prices as per requirements
    return campsites
