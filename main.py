import logging
from Database.sql_db import connect_to_sql
from Database.head_office_db import connect_to_head_office, fetch_bookings
from Database.cosmos_db import connect_to_cosmos
from Models.booking import Booking
from Utils.booking_processor import process_bookings
from Utils.campsite_manager import initialize_campsites
from Utils.summary_manager import generate_summary, display_summary, create_and_insert_summary
from Utils.logging_config import logger  

# Configure logging to display only INFO level and above, suppressing verbose logs from external libraries
logging.basicConfig(level=logging.INFO, format='%(message)s')
logging.getLogger('azure.cosmos').setLevel(logging.WARNING)  # Suppress detailed Cosmos DB logs
logging.getLogger('urllib3').setLevel(logging.WARNING)       # Suppress detailed urllib3 logs

def main():
    """
    Main function that handles the workflow of connecting to databases, processing bookings,
    initializing campsites, and generating summaries.

    The function performs the following steps:
    1. Connects to SQL, Head Office, and Cosmos DB.
    2. Initializes campsite data.
    3. Fetches and processes booking records from Head Office.
    4. Generates and displays a summary of the bookings.
    5. Creates and inserts the summary data into relevant databases.
    """
    sql_conn = None
    head_office_conn = None
    cosmos_conn = None

    try:
        # Connect to SQL, Head Office, and Cosmos DB
        sql_conn = connect_to_sql()
        head_office_conn = connect_to_head_office()
        cosmos_conn = connect_to_cosmos("Bookings")

        # Initialize campsites and fetch all bookings from Head Office database
        campsites = initialize_campsites()
        raw_bookings = fetch_bookings(head_office_conn)

        # Convert raw booking records into Booking objects
        bookings = []
        for record in raw_bookings:
            try:
                booking = Booking.from_db_record(record)  # Convert database record to Booking object
                bookings.append(booking)  # Add to bookings list
            except Exception as e:
                logger.error(f"Error processing booking record: {e}")

        # Process bookings, allocate campsites, and update databases
        campground_id = 1121132  # Set campground ID to my student ID
        process_bookings(bookings, campsites, head_office_conn, cosmos_conn, campground_id)

        # Generate and display a summary of the bookings
        summary = generate_summary(bookings, campsites)
        display_summary(summary)

        # Create and insert the summary into the relevant databases
        create_and_insert_summary(bookings)

    except Exception as e:
        # Log any errors that occur during the main process
        logger.error(f"An error occurred during the main process: {e}")
        print("An error occurred. Check the log file for details.")

    finally:
        # Close all database connections and log the closure
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
