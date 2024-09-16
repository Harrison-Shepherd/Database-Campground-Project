from datetime import datetime
import logging
from Database.sql_db import connect_to_sql
from Database.head_office_db import connect_to_head_office
from Models.summary import Summary
from Utils.pdf_generator import PDFGenerator
from Database.cosmos_db import connect_to_cosmos, upsert_summary_pdf_to_cosmos
from Utils.logging_config import logger

def create_and_insert_summary(bookings):
    """
    Creates and inserts a daily summary of bookings into the local SQL database and the Head Office database.
    Also generates a PDF confirmation of the summary and inserts it into Cosmos DB.

    :param bookings: List of processed Booking objects.
    """
    try:
        total_sales = sum(booking.total_cost for booking in bookings if booking.campsite_id is not None)
        total_bookings = len([booking for booking in bookings if booking.campsite_id is not None])

        summary = Summary(
            campground_id=1121132,
            summary_date=datetime.now().date(),
            total_sales=total_sales,
            total_bookings=total_bookings
        )

        summary.validate()
        logger.info(f"Summary validated and created for {summary.summary_date}.")
        
        insert_summary_into_databases(summary)
        
        pdf_gen = PDFGenerator("Daily Summary Report")
        pdf_path = pdf_gen.generate_summary(summary)
        logger.info("Summary PDF generated and saved.")

        summary_container = connect_to_cosmos("Summary_PDFs")
        summary_id = f"{summary.campground_id}_{summary.summary_date.strftime('%Y-%m-%d')}"
        upsert_summary_pdf_to_cosmos(summary_container, pdf_path, summary_id)
        logger.info("Summary PDF upserted into Cosmos DB successfully.")

        print(f"Summary successfully created and processed for {summary.summary_date}.")

    except Exception as e:
        logger.error(f"Error during summary creation and processing: {e}")
        print(f"An error occurred while processing the summary.")

def insert_summary_into_databases(summary):
    """
    Inserts the summary into both the local SQL and Head Office databases.

    :param summary: Summary object containing summary data.
    """
    try:
        sql_conn = connect_to_sql()
        insert_summary(sql_conn, summary.to_dict())
        sql_conn.close()
        logger.info("Summary inserted into the local SQL database.")

    except Exception as e:
        logger.error(f"Error inserting into the local SQL database: {e}")

    try:
        head_office_conn = connect_to_head_office()
        write_summary_to_head_office(head_office_conn, summary.to_dict())
        head_office_conn.close()
        logger.info("Summary written to the Head Office database.")

    except Exception as e:
        logger.error(f"Error writing summary to Head Office: {e}")

def insert_summary(conn, summary_data):
    """
    Inserts a daily summary into the local SQL database.

    :param conn: Database connection object.
    :param summary_data: Dictionary containing summary details.
    """
    try:
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
        logger.info("Insert into local SQL database successful.")

    except Exception as e:
        logger.error(f"Error inserting summary into the local SQL database: {e}")

def write_summary_to_head_office(conn, summary_data):
    """
    Inserts the summary data into the Head Office summary table.

    :param conn: Connection to the Head Office SQL database.
    :param summary_data: Dictionary containing summary details.
    """
    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO head_office.summary (campground_id, summary_date, total_sales, total_bookings)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(query, (
            summary_data["campground_id"], 
            summary_data["summary_date"],
            summary_data["total_sales"], 
            summary_data["total_bookings"]
        ))
        conn.commit()
        logger.info("Insert into Head Office database successful.")

    except Exception as e:
        logger.error(f"Error writing summary to Head Office: {e}")

def generate_summary(bookings, campsites):
    """
    Generates a summary of the booking allocations and campsite utilization.

    :param bookings: List of Booking objects.
    :param campsites: List of Campsite objects.
    :return: A summary dictionary containing booking statistics and utilization data.
    """
    logger.info("Generating summary from booking data.")
    
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

    logger.info(f"Summary Data: {summary_data}")
    return summary_data

def display_summary(summary):
    """
    Displays the summary of booking allocations and campsite utilization.

    :param summary: A dictionary containing summary details.
    """
    print("\nSummary of Booking Allocations:")
    print(f"Total Bookings: {summary['total_bookings']}")
    print(f"Successful Allocations: {summary['successful_allocations']}")
    print(f"Failed Allocations: {summary['failed_allocations']}")

    print("\nCampsite Utilization:")
    for site_number, details in summary['campsite_utilization'].items():
        print(f"Campsite {site_number}: Size - {details['size']}, Rate - ${details['rate_per_night']} per night, "
              f"Total Bookings - {details['bookings_count']}")
