# main_head_office.py

from Database.head_office_db import connect_to_head_office, fetch_bookings, update_booking_campground

def main():
    try:
        # Connect to the Head Office database
        conn = connect_to_head_office()
        if conn:
            print("Connected to Head Office database successfully.")

            # Fetch bookings where the campground ID is 1
            bookings = fetch_bookings(conn)
            if bookings:
                print(f"Fetched {len(bookings)} bookings from the Head Office database.")
                
                # Print fetched bookings
                for booking in bookings:
                    print(f"Booking ID: {booking[0]}, Customer ID: {booking[1]}, Campground ID: {booking[4]}")
                
                # Example: Update the first booking's campground ID to your student ID
                booking_id = bookings[0][0]  # Assuming booking ID is the first field; adjust if needed
                new_campground_id = 1121132  # Your student ID
                
                update_booking_campground(conn, booking_id, new_campground_id)
                print(f"Updated booking {booking_id} to new campground ID {new_campground_id}.")
            else:
                print("No bookings found with Campground ID 1.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection if it is open
        try:
            conn.close()
            print("Head Office connection closed.")
        except:
            pass

if __name__ == "__main__":
    main()
