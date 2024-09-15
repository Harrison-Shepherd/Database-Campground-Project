# Utils/booking_processor.py

from Database.head_office_db import update_booking_campground
from Database.cosmos_db import insert_booking_to_cosmos
from Models.campsite import allocate_campsite
from Models.booking import create_booking_data, Booking
from Utils.confirmation import generate_confirmation
from datetime import timedelta
import logging

# Configure logging to reduce output verbosity
logging.basicConfig(level=logging.INFO, format='%(message)s')

def process_bookings(bookings, campsites, head_office_conn, cosmos_conn, campground_id):
    """
    Processes bookings by allocating campsites and inserting booking data into Cosmos DB.
    
    :param bookings: List of Booking objects.
    :param campsites: List of Campsite objects available for allocation.
    :param head_office_conn: Connection to the Head Office database.
    :param cosmos_conn: Connection to the Cosmos DB.
    :param campground_id: The ID of the campground.
    """
    allocated_bookings = set()
    inserted_bookings = set()

    for booking in bookings:
        if not isinstance(booking, Booking):
            logging.error(f"Expected Booking object but got {type(booking)}. Skipping this record.")
            continue
        
        # Adjust start and end dates to Saturday and the following week
        adjusted_start_date = Booking.adjust_to_saturday(booking.arrival_date)
        adjusted_end_date = adjusted_start_date + timedelta(days=7)

        # Skip previously allocated bookings
        if booking.booking_id in allocated_bookings:
            logging.info(f"Booking {booking.booking_id} already allocated. Skipping.")
            continue

        logging.info(f"Attempting to allocate Booking {booking.booking_id}...")

        # Attempt to allocate a campsite
        allocated_campsite = allocate_campsite(campsites, adjusted_start_date, adjusted_end_date, booking)
        if allocated_campsite:
            logging.info(f"Booking {booking.booking_id} successfully allocated to Campsite {allocated_campsite.site_number}.")
            
            # Update booking in the head office database
            try:
                update_booking_campground(head_office_conn, booking.booking_id, campground_id)
                allocated_bookings.add(booking.booking_id)
                booking.update_campsite_info(allocated_campsite.site_number, allocated_campsite.rate_per_night)
            except Exception as e:
                logging.error(f"Failed to update booking in Head Office database: {e}")

            # Generate booking confirmation PDF
            try:
                generate_confirmation(booking)
                logging.info(f"Confirmation PDF for Booking {booking.booking_id} generated successfully.")
            except Exception as e:
                logging.error(f"Error generating confirmation PDF for Booking {booking.booking_id}: {e}")
        else:
            logging.warning(f"Booking {booking.booking_id} failed: No available campsites for the week starting {adjusted_start_date.strftime('%Y-%m-%d')}.")

        # Insert booking data into Cosmos DB if not already inserted
        if booking.booking_id not in inserted_bookings:
            booking_data = create_booking_data(booking)
            try:
                insert_booking_to_cosmos_db(cosmos_conn, booking_data)
                inserted_bookings.add(booking.booking_id)
            except Exception as e:
                logging.error(f"Error inserting Booking {booking.booking_id} into Cosmos DB: {e}")

def insert_booking_to_cosmos_db(cosmos_conn, booking_data):
    """
    Inserts booking data into Cosmos DB.
    
    :param cosmos_conn: Connection to the Cosmos DB.
    :param booking_data: Dictionary containing booking data.
    """
    try:
        insert_booking_to_cosmos(cosmos_conn, booking_data)
        logging.info(f"Booking {booking_data['booking_id']} inserted into Cosmos DB successfully.")
    except Exception as e:
        logging.error(f"An error occurred while inserting booking {booking_data['booking_id']}: {e}")
