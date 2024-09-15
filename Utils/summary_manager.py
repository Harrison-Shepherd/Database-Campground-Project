# Utils/summary_manager.py

from datetime import datetime
import logging
from Database.sql_db import connect_to_sql
from Database.head_office_db import connect_to_head_office
from Models.summary import Summary
from Utils.pdf_generator import PDFGenerator
from Database.cosmos_db import connect_to_cosmos, upsert_summary_pdf_to_cosmos  # Updated to use the correct function


def create_and_insert_summary(bookings):
    """
    Creates and inserts a daily summary of bookings into the local SQL database and the Head Office database.
    Also generates a PDF confirmation of the summary and inserts it into Cosmos DB.
    
    :param bookings: List of processed Booking objects.
    """
    try:
        # Calculate the total sales and total bookings from the processed bookings
        total_sales = sum(booking.total_cost for booking in bookings if booking.campsite_id is not None)
        total_bookings = len([booking for booking in bookings if booking.campsite_id is not None])

        # Log calculated totals
        print(f"Calculated Total Sales: {total_sales}, Total Bookings: {total_bookings}")

        # Create a Summary object with the calculated data
        summary = Summary(
            campground_id=1121132,  # Replace with your student ID
            summary_date=datetime.now().date(),
            total_sales=total_sales,
            total_bookings=total_bookings
        )

        # Log the summary object creation
        print(f"Summary object created: {summary}")

        # Validate the summary data before insertion
        summary.validate()
        print("Summary data validated successfully.")

        # Insert into both databases and generate PDF
        insert_summary_into_databases(summary)

        # Generate the PDF using the new PDF generator
        pdf_gen = PDFGenerator("Daily Summary Report")
        pdf_path = pdf_gen.generate_summary(summary)
        print("Summary PDF generated and saved successfully.")

        # Connect to the "Summary_PDFs" container in Cosmos DB
        summary_container = connect_to_cosmos("Summary_PDFs")

        # Use the summary date or another unique field as the summary_id
        summary_id = f"{summary.campground_id}_{summary.summary_date.strftime('%Y-%m-%d')}"

        # Insert the generated PDF into Cosmos DB with the correct summary_id
        upsert_summary_pdf_to_cosmos(summary_container, pdf_path, summary_id)
        print("Summary PDF inserted into Cosmos DB successfully.")

    except Exception as e:
        print(f"An error occurred while creating, saving, or inserting the summary PDF: {e}")


def insert_summary_into_databases(summary):
    """
    Inserts the summary into both the local SQL and Head Office databases.
    
    :param summary: Summary object containing summary data.
    """
    try:
        print("Attempting to connect to the local SQL database...")
        sql_conn = connect_to_sql()
        print("Connected to local SQL database.")
        insert_summary(sql_conn, summary.to_dict())
        print("Summary inserted successfully into the local SQL database.")
        sql_conn.close()
    except Exception as e:
        print(f"An error occurred while inserting into the local SQL database: {e}")

    try:
        print("Attempting to connect to the Head Office SQL database...")
        head_office_conn = connect_to_head_office()
        print("Connected to Head Office SQL database.")
        write_summary_to_head_office(head_office_conn, summary.to_dict())
        print("Summary written back to the Head Office database successfully.")
        head_office_conn.close()
    except Exception as e:
        print(f"An error occurred while writing summary to Head Office: {e}")


def insert_summary(conn, summary_data):
    """
    Inserts a daily summary into the local SQL database.
    
    :param conn: Database connection object.
    :param summary_data: Dictionary containing summary details.
    """
    try:
        print(f"Attempting to insert summary into the local SQL database: {summary_data}")
        cursor = conn.cursor()
        query = """
            INSERT INTO camping.summary (campground_id, summary_date, total_sales, total_bookings)
            VALUES (?, ?, ?, ?)
        """
        cursor.execute(
            query,
            summary_data['campground_id'],
            summary_data['summary_date'],
            summary_data['total_sales'],
            summary_data['total_bookings']
        )
        conn.commit()
        print("Insert into local SQL database successful.")
    except Exception as e:
        print(f"An error occurred while inserting summary into the local SQL database: {e}")


def write_summary_to_head_office(conn, summary_data):
    """
    Inserts the summary data into the Head Office summary table.
    
    :param conn: Connection to the Head Office SQL database.
    :param summary_data: Dictionary containing summary details.
    """
    try:
        print(f"Attempting to insert summary into the Head Office database: {summary_data}")
        cursor = conn.cursor()
        query = """
        INSERT INTO head_office.summary (campground_id, summary_date, total_sales, total_bookings)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(query, (summary_data["campground_id"], summary_data["summary_date"],
                               summary_data["total_sales"], summary_data["total_bookings"]))
        conn.commit()
        print("Insert into Head Office database successful.")
    except Exception as e:
        print(f"An error occurred while writing summary to Head Office: {e}")


def generate_summary(bookings, campsites):
    """
    Generates a summary of the booking allocations and campsite utilization.
    :param bookings: List of Booking objects.
    :param campsites: List of Campsite objects.
    :return: A summary dictionary containing booking statistics and utilization data.
    """
    logging.info("Starting summary generation with booking data:")
    for booking in bookings:
        logging.info(f"Booking ID: {booking.booking_id}, Campsite ID: {booking.campsite_id}, Total Cost: {booking.total_cost}")

    total_sales = sum(booking.total_cost for booking in bookings if booking.campsite_id is not None)
    successful_allocations = sum(1 for booking in bookings if booking.campsite_id is not None)
    failed_allocations = len(bookings) - successful_allocations

    campsite_utilization = {c.site_number: {'size': c.size, 'rate_per_night': c.rate_per_night, 'bookings_count': 0} for c in campsites}

    for booking in bookings:
        if booking.campsite_id is not None:
            campsite_utilization[booking.campsite_id]['bookings_count'] += 1

    summary_data = {
        'date': datetime.now().date(),
        'total_sales': total_sales,
        'total_bookings': len(bookings),
        'successful_allocations': successful_allocations,
        'failed_allocations': failed_allocations,
        'campsite_utilization': campsite_utilization
    }

    logging.info(f"Summary Data: {summary_data}")  # Log summary data for debugging
    return summary_data


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
