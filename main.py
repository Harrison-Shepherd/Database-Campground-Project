# main.py

import logging
from Database.sql_db import connect_to_sql
from Database.head_office_db import connect_to_head_office, fetch_bookings
from Database.cosmos_db import connect_to_cosmos
from Models.booking import Booking
from Utils.booking_processor import process_bookings
from Utils.campsite_manager import initialize_campsites
from Utils.summary_manager import generate_summary, display_summary, create_and_insert_summary
from Utils.logging_config import logger  # Import the logger configured to save logs to a file

# Configure logging to display only INFO level and above, suppressing verbose logs from external libraries
logging.basicConfig(level=logging.INFO, format='%(message)s')
logging.getLogger('azure.cosmos').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

def main():
    sql_conn = None
    head_office_conn = None
    cosmos_conn = None

    try:
        #connect to databases
        sql_conn = connect_to_sql()
        head_office_conn = connect_to_head_office()
        cosmos_conn = connect_to_cosmos("Bookings")

        #initialize campsites, then fetch all bookings from head office db.
        campsites = initialize_campsites()
        raw_bookings = fetch_bookings(head_office_conn)

        bookings = []
        for record in raw_bookings:
            try:
                booking = Booking.from_db_record(record)
                bookings.append(booking)
            except Exception as e:
                logger.error(f"Error processing booking record: {e}")

        campground_id = 1121132  
        process_bookings(bookings, campsites, head_office_conn, cosmos_conn, campground_id)

        summary = generate_summary(bookings, campsites)
        display_summary(summary)
        create_and_insert_summary(bookings)

    except Exception as e:
        logger.error(f"An error occurred during the main process: {e}")
        print("An error occurred. Check the log file for details.")

    finally:
        if sql_conn:
            sql_conn.close()
            logger.info("SQL connection closed.")
        if head_office_conn:
            head_office_conn.close()
            logger.info("Head Office connection closed.")
        logger.info("Cosmos connection closed.")  

if __name__ == '__main__':
    # Set logger to INFO level to suppress DEBUG-level messages
    logger.setLevel(logging.INFO)
    main()
