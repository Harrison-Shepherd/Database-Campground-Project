from datetime import timedelta
from Database.head_office_db import update_booking_campground
from Database.cosmos_db import insert_booking_to_cosmos  # Corrected import for the Cosmos DB insert function
from Models.campsite import allocate_campsite
from Models.booking import create_booking_data, Booking
from Utils.confirmation import generate_confirmation
from Utils.logging_config import logger

def process_bookings(bookings, campsites, head_office_conn, cosmos_conn, campground_id):
    """
    Processes bookings by allocating campsites and inserting booking data into Cosmos DB.
    
    :param bookings: List of Booking objects.
    :param campsites: List of Campsite objects available for allocation.
    :param head_office_conn: Connection to the Head Office database.
    :param cosmos_conn: Connection to the Cosmos DB.
    :param campground_id: The ID of the campground.
    """
    for booking in bookings:
        # Ensure booking is of the correct type
        if not isinstance(booking, Booking):
            logger.error(f"Expected Booking object but got {type(booking)}. Skipping this record.")
            continue
        
        # Adjust booking dates to Saturday and the following week
        adjusted_start_date = Booking.adjust_to_saturday(booking.arrival_date)
        adjusted_end_date = adjusted_start_date + timedelta(days=7)

        # Log processing attempt for each booking
        logger.info(f"Processing Booking {booking.booking_id}...")

        # Attempt to allocate a campsite
        allocated_campsite = allocate_campsite(campsites, adjusted_start_date, adjusted_end_date, booking)
        if allocated_campsite:
            try:
                # Update booking information in the Head Office database
                update_booking_campground(head_office_conn, booking.booking_id, campground_id)
                booking.update_campsite_info(allocated_campsite.site_number, allocated_campsite.rate_per_night)
                
                # Generate confirmation PDF
                generate_confirmation(booking)
                
                # Insert booking into Cosmos DB
                booking_data = create_booking_data(booking)
                insert_booking_to_cosmos_db(cosmos_conn, booking_data)
                
                # Log a single success message for the processed booking
                logger.info(f"Booking {booking.booking_id} processed successfully: " + f"allocated to Campsite {allocated_campsite.site_number} and inserted into Cosmos DB.")
                print(f"Booking {booking.booking_id} processed successfully: " + f"allocated to Campsite {allocated_campsite.site_number} and inserted into Cosmos DB.")
            except Exception as e:
                # Log any errors encountered during processing
                logger.error(f"Error processing Booking {booking.booking_id}: {e}")
        else:
            # Log a single failure message if no campsites are available
            logger.warning(
                f"Booking {booking.booking_id} failed: No available campsites for the week starting "
                f"{adjusted_start_date.strftime('%Y-%m-%d')}."
            )

def insert_booking_to_cosmos_db(cosmos_conn, booking_data):
    """
    Inserts booking data into Cosmos DB.
    
    :param cosmos_conn: Connection to the Cosmos DB.
    :param booking_data: Dictionary containing booking data.
    """
    try:
        # Attempt to insert booking data into Cosmos DB
        insert_booking_to_cosmos(cosmos_conn, booking_data)
        logger.info(f"Booking {booking_data['booking_id']} inserted into Cosmos DB successfully.")
    except Exception as e:
        # Log any errors encountered during the insert operation
        logger.error(f"An error occurred while inserting booking {booking_data['booking_id']}: {e}")
