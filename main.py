# main.py
from Database.sql_db import connect_to_sql
from Database.head_office_db import connect_to_head_office, fetch_bookings
from Database.cosmos_db import connect_to_cosmos
from Models.booking import Booking
from Utils.booking_processor import process_bookings
from Utils.campsite_manager import initialize_campsites
from Utils.summary_manager import generate_summary, display_summary, create_and_insert_summary  # Import the summary functions
import logging

# Configure logging to suppress less relevant logs, and only show INFO and above
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Suppress lower-level logs from external libraries like Cosmos SDK
logging.getLogger('azure.cosmos').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

def main():
    sql_conn = None
    head_office_conn = None
    cosmos_conn = None

    try:
        # Step 1: Connect to SQL database
        sql_conn = connect_to_sql()
        print("Connected to SQL database successfully.")

        # Step 2: Connect to Head Office database and fetch bookings
        head_office_conn = connect_to_head_office()
        print("Connected to Head Office database successfully.")

        raw_bookings = fetch_bookings(head_office_conn)
        print(f"Fetched {len(raw_bookings)} bookings from the head office database.")

        # Convert raw rows to Booking objects
        bookings = []
        for record in raw_bookings:
            try:
                booking = Booking.from_db_record(record)
                bookings.append(booking)
            except Exception as e:
                print(f"Expected Booking object but got {type(record)}. Skipping this record.")

        # Initialize campsites
        campsites = initialize_campsites()

        # Step 4: Connect to Cosmos DB
        cosmos_conn = connect_to_cosmos()
        print("Connected to Cosmos DB successfully.")

        # Step 5: Process the bookings
        campground_id = 1121132  # Replace with your student ID
        process_bookings(bookings, campsites, head_office_conn, cosmos_conn, campground_id)

        # Step 6: Generate and display the summary
        summary = generate_summary(bookings, campsites)
        display_summary(summary)

        # Step 7: Create and insert the summary into databases and generate the PDF
        create_and_insert_summary(bookings)
        print("Summary creation, insertion, and PDF generation completed.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Step 8: Close all connections
        if sql_conn:
            sql_conn.close()
            print("SQL connection closed.")
        if head_office_conn:
            head_office_conn.close()
            print("Head Office connection closed.")
        print("Cosmos DB connection management is handled by SDK.")

if __name__ == "__main__":
    main()
