from Database.cosmos_db import connect_to_cosmos, add_booking
from Database.sql_db import connect_to_sql, insert_summary
from Database.head_office_db import connect_to_head_office, fetch_bookings, update_booking_campground
from Models.booking import Booking
from Utils.confirmation import generate_confirmation

def main():
    # Connect to all databases
    cosmos_container = connect_to_cosmos()
    sql_conn = connect_to_sql()
    head_office_conn = connect_to_head_office()

    # Fetch bookings from Head Office
    bookings = fetch_bookings(head_office_conn)
    for booking_data in bookings:
        # Update booking's campground ID to match your ID
        update_booking_campground(head_office_conn, booking_data['booking_id'], YOUR_CAMPGROUND_ID)
        
        # Process booking
        booking = Booking(booking_data)
        booking.allocate_campsites()
        confirmation = generate_confirmation(booking)
        
        # Save to Cosmos DB
        add_booking(cosmos_container, booking.to_dict())
    
    # End-of-day summary
    summary_data = create_daily_summary()
    insert_summary(sql_conn, summary_data)

if __name__ == "__main__":
    main()
