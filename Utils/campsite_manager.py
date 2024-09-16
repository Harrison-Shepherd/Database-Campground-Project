from Models.campsite import Campsite
from Utils.logging_config import logger

def initialize_campsites():
    """
    Initializes a list of campsites with predefined sizes and rates.

    :return: A list of Campsite objects.
    """
    campsites = []

    # Add 10 Small campsites with a rate of 50 per night
    for i in range(1, 11):
        campsites.append(Campsite(site_number=i, size='Small', rate_per_night=50))

    # Add 10 Medium campsites with a rate of 60 per night
    for i in range(11, 21):
        campsites.append(Campsite(site_number=i, size='Medium', rate_per_night=60))

    # Add 10 Large campsites with a rate of 70 per night
    for i in range(21, 31):
        campsites.append(Campsite(site_number=i, size='Large', rate_per_night=70))

    logger.info(f"Initialized {len(campsites)} campsites: 10 Small, 10 Medium, 10 Large.")
    
    return campsites
