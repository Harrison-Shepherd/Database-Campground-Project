# app.py

import sys
import os
import logging
import io

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from Models.booking import Booking
from Utils.booking_processor import process_bookings
from Database.sql_db import connect_to_sql
from Database.cosmos_db import connect_to_cosmos, fetch_cosmos_bookings
from Utils.campsite_manager import initialize_campsites
from Utils.summary_manager import create_and_insert_summary, generate_summary, display_summary
from Database.head_office_db import connect_to_head_office, fetch_bookings

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Global variable to hold processed bookings
processed_bookings = []

@app.route('/')
def index():
    """
    Home page displaying options for processing bookings, viewing summaries, etc.
    """
    try:
        cosmos_conn = connect_to_cosmos("Bookings")
        bookings = fetch_cosmos_bookings(cosmos_conn)

        # Debugging step: Log bookings to ensure customer_name is fetched correctly
        for booking in bookings:
            logging.info(f"Booking ID: {booking.booking_id}, Customer Name: {booking.customer_name}")

        if not bookings:
            flash('No bookings available.', 'info')
        return render_template('index.html', bookings=bookings)
    except Exception as e:
        logging.error(f"Error loading index: {str(e)}")
        flash(f'Error loading index: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/process_bookings', methods=['POST'])
def process_bookings_route():
    """
    Route to process bookings from Head Office and store in Cosmos DB.
    """
    global processed_bookings
    try:
        sql_conn = connect_to_sql()
        head_office_conn = connect_to_head_office()
        cosmos_conn = connect_to_cosmos("Bookings")

        # Fetch bookings from the Head Office database
        raw_bookings = fetch_bookings(head_office_conn)
        bookings = [Booking.from_db_record(record) for record in raw_bookings]
        campsites = initialize_campsites()
        campground_id = 1121132

        # Process bookings and keep them in the global variable for later use
        process_bookings(bookings, campsites, head_office_conn, cosmos_conn, campground_id)
        processed_bookings = bookings  # Store processed bookings for summary use
        flash('Bookings processed successfully!', 'success')
        return redirect(url_for('summary'))
    except Exception as e:
        logging.error(f"Error processing bookings: {str(e)}")
        flash(f'Error processing bookings: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/bookings')
def view_bookings():
    """
    Route to display all stored bookings from Cosmos DB.
    """
    try:
        cosmos_conn = connect_to_cosmos("Bookings")
        bookings = fetch_cosmos_bookings(cosmos_conn)

        # Debug: Print customer names to ensure they are fetched correctly
        for booking in bookings:
            logging.info(f"Booking ID: {booking.booking_id}, Customer Name: {booking.customer_name}")

        return render_template('bookings_list.html', bookings=bookings)
    except Exception as e:
        logging.error(f"Error fetching bookings: {str(e)}")
        flash(f'Error fetching bookings: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/summary')
def summary():
    """
    Route to display the daily summary of bookings.
    """
    global processed_bookings
    try:
        # Check if processed bookings exist; if not, fetch from Cosmos DB as a fallback
        bookings = processed_bookings or fetch_cosmos_bookings(connect_to_cosmos("Bookings"))

        # If bookings are fetched but not processed, process them
        if not processed_bookings and bookings:
            campsites = initialize_campsites()
            process_bookings(bookings, campsites, connect_to_head_office(), connect_to_cosmos("Bookings"), campground_id=1121132)
            processed_bookings = bookings  # Store processed bookings for future use
            flash('Bookings were repopulated and processed!', 'info')

        # If still no bookings, trigger repopulation
        if not bookings:
            flash('No bookings available. Please process the bookings first.', 'warning')
            return redirect(url_for('process_bookings_route'))

        campsites = initialize_campsites()

        # Generate the summary from the processed bookings
        summary_data = generate_summary(bookings, campsites)

        # Log the generated summary data for debugging
        logging.info(f"Generated Summary Data: {summary_data}")

        # Display the summary data to confirm accuracy
        display_summary(summary_data)

        # Create and insert summary into databases and generate a PDF
        create_and_insert_summary(bookings)
        flash('Summary generated and stored successfully!', 'success')

        # Render the summary template with the summary data
        return render_template('summary.html', summary=summary_data)
    except Exception as e:
        logging.error(f"Error generating summary: {str(e)}")
        flash(f"Error generating summary: {str(e)}", 'danger')
        return redirect(url_for('index'))

@app.route('/pdf/<int:booking_id>')
def show_pdf(booking_id):
    """
    Route to fetch and display the PDF file for a specific booking.
    """
    try:
        # Connect to both Bookings and PDFs containers
        cosmos_conn_bookings = connect_to_cosmos("Bookings")
        cosmos_conn_pdfs = connect_to_cosmos("PDFs")

        # Fetch the PDF data from the PDFs container
        pdf_data = fetch_pdf_from_cosmos(cosmos_conn_bookings, cosmos_conn_pdfs, booking_id)

        # Create an in-memory file-like object to serve the PDF
        return send_file(
            io.BytesIO(pdf_data),
            mimetype='application/pdf',
            download_name=f'confirmation_{booking_id}.pdf'
        )
    except Exception as e:
        logging.error(f"Error fetching PDF for Booking ID {booking_id}: {str(e)}")
        flash(f'Error fetching PDF for Booking ID {booking_id}: {str(e)}', 'danger')
        return redirect(url_for('view_bookings'))

def fetch_pdf_from_cosmos(cosmos_conn_bookings, cosmos_conn_pdfs, booking_id):
    """
    Fetches the PDF data for a given booking ID from Cosmos DB.
    
    :param cosmos_conn_bookings: The connection object to the Bookings container in Cosmos DB.
    :param cosmos_conn_pdfs: The connection object to the PDFs container in Cosmos DB.
    :param booking_id: The ID of the booking for which the PDF is to be fetched.
    :return: The PDF data as bytes.
    """
    try:
        # Step 1: Fetch the booking document to get the pdf_id
        query_booking = f"SELECT * FROM c WHERE c.booking_id = {booking_id}"
        booking_items = cosmos_conn_bookings.query_items(query=query_booking, enable_cross_partition_query=True)
        booking_list = list(booking_items)

        # Check if the booking was found
        if not booking_list:
            logging.error(f"Booking not found for booking ID {booking_id}")
            raise ValueError(f"Booking not found for booking ID {booking_id}")

        booking = booking_list[0]
        pdf_id = booking.get('pdf_id')  # Adjust this key based on your schema

        # Step 2: Use the pdf_id to fetch the corresponding PDF from the PDFs container
        if not pdf_id:
            logging.error(f"No pdf_id found for booking ID {booking_id}")
            raise ValueError(f"No pdf_id found for booking ID {booking_id}")

        query_pdf = f"SELECT * FROM c WHERE c.pdf_id = '{pdf_id}'"
        pdf_items = cosmos_conn_pdfs.query_items(query=query_pdf, partition_key=pdf_id, enable_cross_partition_query=True)
        pdf_list = list(pdf_items)

        # Check if the PDF was found
        if not pdf_list:
            logging.error(f"PDF not found for pdf_id {pdf_id}")
            raise ValueError(f"PDF not found for pdf_id {pdf_id}")

        pdf_document = pdf_list[0]
        pdf_data = pdf_document.get('pdf_data')

        # Check if PDF data is present
        if not pdf_data:
            logging.error(f"PDF data not found for pdf_id {pdf_id}")
            raise ValueError(f"PDF data not found for pdf_id {pdf_id}")

        # If PDF data is stored as a string (like base64), decode it appropriately
        if isinstance(pdf_data, str):
            import base64
            pdf_data = base64.b64decode(pdf_data)

        return pdf_data
    except Exception as e:
        logging.error(f"Failed to fetch PDF data from Cosmos DB: {e}")
        raise


if __name__ == '__main__':
    app.run(debug=True)
