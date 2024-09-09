from datetime import datetime
from Database.sql_db import insert_summary
from Models.campsite import Campsite
from Models.booking import Booking

def create_and_insert_summary(sql_conn, bookings, head_office_conn):
    """
    Creates and inserts a daily summary of bookings into the SQL database and writes it back to Head Office.
    """
    total_sales = sum(booking.total_cost for booking in bookings if booking.campsite_id is not None)
    total_bookings = len(bookings)
    summary_data = {
        "campground_id": 1121132,  # Replace with your student ID
        "summary_date": datetime.now().strftime("%Y-%m-%d"),
        "total_sales": total_sales,
        "total_bookings": total_bookings
    }

    try:
        # Insert summary into local SQL database
        insert_summary(sql_conn, summary_data)
        print("Summary inserted successfully into local SQL database.")

        # Write summary back to Head Office database
        write_summary_to_head_office(head_office_conn, summary_data)
        print("Summary written back to Head Office database successfully.")
    except Exception as e:
        print(f"An error occurred while inserting summary: {e}")

def write_summary_to_head_office(head_office_conn, summary_data):
    """
    Writes the summary data back to the Head Office database.
    """
    cursor = head_office_conn.cursor()
    query = """
    INSERT INTO head_office.summary (campground_id, summary_date, total_sales, total_bookings)
    VALUES (?, ?, ?, ?)
    """
    cursor.execute(query, (summary_data["campground_id"], summary_data["summary_date"],
                           summary_data["total_sales"], summary_data["total_bookings"]))
    head_office_conn.commit()

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
