# main.py

from Database.sql_db import connect_to_sql
from Database.head_office_db import connect_to_head_office, fetch_bookings
from Database.cosmos_db import connect_to_cosmos
from Models.campsite import Campsite
from Utils.booking_processor import process_bookings

import logging

# Configure logging to suppress less relevant logs, and only show INFO and above
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Suppress lower-level logs from external libraries like Cosmos SDK
logging.getLogger('azure.cosmos').setLevel(logging.WARNING)  # Adjust 'azure.cosmos' to the actual SDK being too verbose
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

        bookings = fetch_bookings(head_office_conn)
        print(f"Fetched {len(bookings)} bookings from the head office database.")

        # Step 3: Setup campsites for allocation
        campsites = [
            Campsite(1, 'Large', 70),  # Adding the rate per night for Large campsites
            Campsite(2, 'Medium', 60),  # Adding the rate per night for Medium campsites
            Campsite(3, 'Small', 50)    # Adding the rate per night for Small campsites
        ]


        # Step 4: Connect to Cosmos DB
        cosmos_conn = connect_to_cosmos()
        print("Connected to Cosmos DB successfully.")

        # Step 5: Process the bookings
        campground_id = 1121132  # Replace with your student ID
        process_bookings(bookings, campsites, head_office_conn, cosmos_conn, campground_id)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Step 6: Close all connections
        if sql_conn:
            sql_conn.close()
            print("SQL connection closed.")
        if head_office_conn:
            head_office_conn.close()
            print("Head Office connection closed.")
        print("Cosmos DB connection management is handled by SDK.")

if __name__ == "__main__":
    main()
