# Utils/summary_manager.py

from datetime import datetime
from Database.sql_db import connect_to_sql
from Database.head_office_db import connect_to_head_office
from Models.summary import Summary
from fpdf import FPDF  # Ensure you have installed fpdf using pip install fpdf
import os

# Define the folder to save confirmation PDFs
CONFIRMATION_FOLDER = "confirmation_pdfs"

# Ensure the folder exists
os.makedirs(CONFIRMATION_FOLDER, exist_ok=True)


def create_and_insert_summary(bookings):
    """
    Creates and inserts a daily summary of bookings into the local SQL database and the Head Office database.
    Also generates a PDF confirmation of the summary.
    
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
        generate_summary_pdf(summary)
        print("Summary PDF generated and saved successfully.")

    except Exception as e:
        print(f"An error occurred while creating and inserting the summary: {e}")


def insert_summary_into_databases(summary):
    """
    Inserts the summary into both the local SQL and Head Office databases.
    
    :param summary: Summary object containing summary data.
    """
    # Attempt to insert into the local SQL database
    try:
        print("Attempting to connect to the local SQL database...")
        sql_conn = connect_to_sql()
        print("Connected to local SQL database.")
        insert_summary(sql_conn, summary.to_dict())
        print("Summary inserted successfully into the local SQL database.")
        sql_conn.close()
    except Exception as e:
        print(f"An error occurred while inserting into the local SQL database: {e}")

    # Attempt to insert into the Head Office database
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


def generate_summary_pdf(summary):
    """
    Generates a PDF file for the summary and saves it in the 'confirmation_pdfs' folder.
    
    :param summary: Summary object containing the summary data.
    """
    try:
        print(f"Generating PDF for summary: {summary}")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add content to the PDF
        pdf.cell(200, 10, txt="Daily Summary Report", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Campground ID: {summary.campground_id}", ln=True)
        pdf.cell(200, 10, txt=f"Summary Date: {summary.summary_date}", ln=True)
        pdf.cell(200, 10, txt=f"Total Sales: ${summary.total_sales:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Total Bookings: {summary.total_bookings}", ln=True)

        # Define the filename and save the PDF
        filename = os.path.join(CONFIRMATION_FOLDER, f"summary_{summary.summary_date}.pdf")
        pdf.output(filename)
        print(f"Summary PDF saved as {filename}")
    except Exception as e:
        print(f"An error occurred while generating the summary PDF: {e}")


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
