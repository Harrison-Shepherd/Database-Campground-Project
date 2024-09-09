# Utils/summary_manager.py
from datetime import datetime
from Database.sql_db import insert_summary
from Database.head_office_db import write_summary_to_head_office
from Models.summary import Summary

def create_and_insert_summary(sql_conn, bookings, head_office_conn):
    """
    Creates and inserts a daily summary of bookings into the local SQL database and the Head Office database.
    
    :param sql_conn: SQL database connection for local summary insertion.
    :param bookings: List of processed Booking objects.
    :param head_office_conn: Connection to the Head Office SQL database.
    """
    # Calculate the total sales and total bookings from the processed bookings
    total_sales = sum(booking.total_cost for booking in bookings if booking.campsite_id is not None)
    total_bookings = len([booking for booking in bookings if booking.campsite_id is not None])

    # Create a Summary object with the calculated data
    summary = Summary(
        campground_id=1121132,  # Replace with your student ID
        summary_date=datetime.now().date(),
        total_sales=total_sales,
        total_bookings=total_bookings
    )

    try:
        # Validate the summary data before insertion
        summary.validate()

        # Insert the summary into the local SQL database
        insert_summary(sql_conn, summary.to_dict())
        print("Summary inserted successfully into the local SQL database.")

        # Insert the summary into the Head Office database
        write_summary_to_head_office(head_office_conn, summary.to_dict())
        print("Summary written back to the Head Office database successfully.")
    except Exception as e:
        print(f"An error occurred while inserting the summary: {e}")

def generate_summary(bookings, campsites):
    """
    Generates a summary of booking allocations and campsite utilization.

    :param bookings: List of Booking objects.
    :param campsites: List of Campsite objects.
    :return: A dictionary containing summary details.
    """
    summary = {
        "total_bookings": len(bookings),
        "successful_allocations": 0,
        "failed_allocations": 0,
        "campsite_utilization": {}
    }

    # Track successful and failed allocations
    for booking in bookings:
        if booking.campsite_id is not None:
            summary["successful_allocations"] += 1
        else:
            summary["failed_allocations"] += 1

    # Calculate campsite utilization
    for campsite in campsites:
        site_number = campsite.site_number
        utilization_count = len(campsite.bookings)
        summary["campsite_utilization"][site_number] = {
            "size": campsite.size,
            "rate_per_night": campsite.rate_per_night,
            "bookings_count": utilization_count
        }

    return summary

def display_summary(summary):
    """
    Displays the summary of booking allocations and campsite utilization.

    :param summary: A dictionary containing summary details.
    """
    print("\nSummary of Booking Allocations:")
    print(f"Total Bookings: {summary['total_bookings']}")
    print(f"Successful Allocations: {summary['successful_allocations']}")
    print(f"Failed Allocations: {summary['failed_allocations']}\n")

    print("Campsite Utilization:")
    for site_number, details in summary['campsite_utilization'].items():
        print(f"Campsite {site_number}: Size - {details['size']}, Rate - ${details['rate_per_night']} per night, "
              f"Total Bookings - {details['bookings_count']}")
