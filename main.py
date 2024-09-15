# main.py

import logging
from Database.sql_db import connect_to_sql
from Database.head_office_db import connect_to_head_office, fetch_bookings
from Database.cosmos_db import connect_to_cosmos
from Models.booking import Booking
from Utils.booking_processor import process_bookings
from Utils.campsite_manager import initialize_campsites
from Utils.summary_manager import generate_summary, display_summary, create_and_insert_summary


# Configure logging to display only INFO level and above, suppressing verbose logs from external libraries
logging.basicConfig(level=logging.INFO, format='%(message)s')
logging.getLogger('azure.cosmos').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

def main():
    # Initialize connections to None to ensure clean closure in the finally block
    sql_conn = None
    head_office_conn = None
    cosmos_conn = None

    try:
        # Step 1: Establish connection to the SQL database for core data operations
        sql_conn = connect_to_sql()
        print("Connected to SQL database successfully.")

        # Step 2: Connect to Head Office database to fetch booking records
        head_office_conn = connect_to_head_office()
        print("Connected to Head Office database successfully.")

        # Fetch raw bookings data; these are expected to be rows from the Head Office database
        raw_bookings = fetch_bookings(head_office_conn)
        print(f"Fetched {len(raw_bookings)} bookings from the head office database.")

        # Convert raw booking data into Booking objects, filtering out any records that don't conform
        bookings = []
        for record in raw_bookings:
            try:
                # Attempt to create a Booking object; skip if the record is invalid
                booking = Booking.from_db_record(record)
                bookings.append(booking)
            except Exception as e:
                print(f"Expected Booking object but got {type(record)}. Skipping this record.")

        # Step 3: Initialize campsites configuration and state
        campsites = initialize_campsites()

        # Step 4: Connect to Cosmos DB for cloud-based data storage and operations
        cosmos_conn = connect_to_cosmos("Bookings")  # Provide the correct container name
        print("Connected to Cosmos DB successfully.")

        # Step 5: Process the bookings by updating database entries and synchronizing data
        campground_id = 1121132  # Example campground ID; ensure this is correctly set based on context
        process_bookings(bookings, campsites, head_office_conn, cosmos_conn, campground_id)

        # Step 6: Generate a summary of processed bookings and display it to the user
        summary = generate_summary(bookings, campsites)
        display_summary(summary)

        # Step 7: Finalize the summary by inserting it into the necessary databases and generating any required reports
        create_and_insert_summary(bookings)
        print("Summary creation, insertion, and PDF generation completed.")

    except Exception as e:
        # Generic error handler to capture and report unexpected issues
        print(f"An error occurred: {e}")

    finally:
        # Step 8: Ensure all database connections are properly closed
        if sql_conn:
            sql_conn.close()
            print("SQL connection closed.")
        if head_office_conn:
            head_office_conn.close()
            print("Head Office connection closed.")
        print("Cosmos DB connection management is handled by SDK.")  # Cosmos SDK handles connection cleanup

if __name__ == "__main__":
    main()
