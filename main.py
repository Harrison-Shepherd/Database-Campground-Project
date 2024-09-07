# main.py

from Database.sql_db import connect_to_sql, insert_summary
from Database.head_office_db import connect_to_head_office, fetch_bookings, update_booking_campground
from Database.cosmos_db import connect_to_cosmos, fetch_cosmos_bookings, insert_booking_to_cosmos
from Models.booking import Booking
from datetime import datetime


def main():
    try:
        # Connect to the SQL database
        sql_conn = connect_to_sql()
        print("Connected to SQL database successfully.")

        # Sample data for the summary; replace with actual logic or database data
        summary_data = {
            "campground_id": 1121132,  # Your student ID or another relevant identifier
            "summary_date": datetime.now().strftime("%Y-%m-%d"),
            "total_sales": 1500.50,
            "total_bookings": 12
        }

        # Insert the summary data into the SQL database
        insert_summary(sql_conn, summary_data)
        print("Summary inserted successfully.")

        # Connect to the Head Office database
        head_office_conn = connect_to_head_office()
        print("Connected to Head Office database successfully.")

        # Example of fetching bookings from the Head Office database
        bookings = fetch_bookings(head_office_conn)
        print(f"Fetched {len(bookings)} bookings from the Head Office database.")

        # Example of updating a booking (change the campground ID to your ID)
        for booking in bookings:
            booking_id = booking[0]  # Assuming booking ID is the first field; adjust as needed
            update_booking_campground(head_office_conn, booking_id, 1121132)  # Use your campground number
            print(f"Updated booking {booking_id} to new campground ID.")

        # Connect to the Cosmos DB
        cosmos_conn = connect_to_cosmos()
        print("Connected to Cosmos DB successfully.")

        # Fetch and insert bookings in Cosmos DB
        cosmos_bookings = fetch_cosmos_bookings(cosmos_conn)
        print(f"Fetched {len(cosmos_bookings)} bookings from Cosmos DB.")

        # Insert each booking into Cosmos DB if it's not already there
        for booking in bookings:
            booking_data = {
                "customer_name": booking[1],  # Replace with actual fields
                "booking_date": str(booking[2]),  # Replace with actual fields
                "campsite_size": booking[5],  # Replace with actual fields
                "num_campsites": booking[6],  # Replace with actual fields
                "total_cost": 420  # Sample cost; adjust according to your booking data
            }
            insert_booking_to_cosmos(cosmos_conn, booking_data)
            print(f"Inserted booking into Cosmos DB.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close database connections if they are open
        try:
            sql_conn.close()
            print("SQL connection closed.")
        except:
            pass
        try:
            head_office_conn.close()
            print("Head Office connection closed.")
        except:
            pass
        try:
            cosmos_conn.client_connection.close()
            print("Cosmos DB connection closed.")
        except:
            pass


if __name__ == "__main__":
    main()
