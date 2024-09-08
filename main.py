# main.py

from Database.sql_db import connect_to_sql, insert_summary
from Database.head_office_db import connect_to_head_office, fetch_bookings, update_booking_campground
from Database.cosmos_db import connect_to_cosmos, insert_booking_to_cosmos
from Models.campsite import Campsite, allocate_campsite
from datetime import datetime

def main():
    sql_conn = None
    head_office_conn = None
    cosmos_conn = None

    try:
        # Step 1: Connect to SQL database and insert a summary
        sql_conn = connect_to_sql()
        print("Connected to SQL database successfully.")

        # Sample summary data
        summary_data = {
            "campground_id": 1121132,  # Your student ID
            "summary_date": datetime.now().strftime("%Y-%m-%d"),
            "total_sales": 1500.50,
            "total_bookings": 12
        }
        insert_summary(sql_conn, summary_data)
        print("Summary inserted successfully.")

        # Step 2: Connect to Head Office database and fetch bookings
        head_office_conn = connect_to_head_office()
        print("Connected to Head Office database successfully.")

        bookings = fetch_bookings(head_office_conn)
        print(f"Fetched {len(bookings)} bookings from the head office database.")

        # Step 3: Allocate campsites to bookings
        campsites = [
            Campsite(1, 'Large'),
            Campsite(2, 'Medium'),
            Campsite(3, 'Small')
        ]

        # Track allocated bookings to avoid duplicate allocations
        allocated_bookings = set()

        for booking in bookings:
            booking_id = booking[0]
            start_date = booking[2]
            end_date = booking[3]

            # Check if this booking has already been allocated
            if booking_id in allocated_bookings:
                print(f"Booking {booking_id} already allocated. Skipping.")
                continue

            # Attempt to allocate a campsite
            # Ensure that each booking is handled only once and the campsite status is updated properly.
            allocated_campsite = allocate_campsite(campsites, start_date, end_date, booking)
            if allocated_campsite:
                print(f"Booking {booking_id} allocated to Campsite {allocated_campsite.site_number}.")
                update_booking_campground(head_office_conn, booking_id, 1121132)
                print(f"Updated booking {booking_id} to new campground ID 1121132.")
            else:
                print(f"No available campsites for booking {booking_id} from {start_date} to {end_date}.")
                update_booking_campground(head_office_conn, booking_id, 1121132)


        # Step 4: Connect to Cosmos DB and insert bookings
        cosmos_conn = connect_to_cosmos()
        print("Connected to Cosmos DB successfully.")

        # Track inserted bookings to avoid duplicate insertions
        inserted_bookings = set()

        for booking in bookings:
            booking_id = booking[0]
            if booking_id in inserted_bookings:
                print(f"Booking with ID {booking_id} already exists in Cosmos DB. Skipping insertion.")
                continue

            booking_data = {
                "booking_id": booking[0],
                "customer_id": booking[1],
                "booking_date": booking[2].strftime("%Y-%m-%d"),
                "arrival_date": booking[3].strftime("%Y-%m-%d"),
                "campground_id": booking[4],
                "campsite_size": booking[5],
                "num_campsites": booking[6]
            }

            try:
                insert_booking_to_cosmos(cosmos_conn, booking_data)
                print(f"Inserted booking {booking_data['booking_id']} into Cosmos DB.")
                inserted_bookings.add(booking_id)
            except Exception as e:
                print(f"An error occurred while inserting booking {booking_data['booking_id']}: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Step 5: Close all connections
        if sql_conn:
            sql_conn.close()
            print("SQL connection closed.")
        if head_office_conn:
            head_office_conn.close()
            print("Head Office connection closed.")
        print("Cosmos DB connection management is handled by SDK.")

if __name__ == "__main__":
    main()
