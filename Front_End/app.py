import sys
import os
import logging
import io
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from Models.booking import Booking
from Utils.booking_processor import process_bookings
from Database.sql_db import connect_to_sql
from Database.cosmos_db import connect_to_cosmos, fetch_cosmos_bookings
from Utils.campsite_manager import initialize_campsites
from Utils.summary_manager import create_and_insert_summary, generate_summary, display_summary
from Database.head_office_db import connect_to_head_office, fetch_bookings
from Utils.logging_config import logger

app = Flask(__name__)
app.secret_key = b'\x89\xfa\x1d\xfe\x2c\x88\x9b\xfd\x8c\x2e\xbf\x4a\x7d\xea\x3f\xce\xa1\x23\x64\xbf\x8e\x59\x22'

# Configure logging to display only INFO level and above
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Global variable to hold processed bookings
processed_bookings = []

@app.route('/')
def index():
    """
    Route to display the main index page, showing bookings fetched from Cosmos DB.

    :return: Rendered index page with bookings data.
    """
    try:
        cosmos_conn = connect_to_cosmos("Bookings")
        bookings = fetch_cosmos_bookings(cosmos_conn)
        for booking in bookings:
            logger.info(f"Booking ID: {booking.booking_id}, Customer Name: {booking.customer_name}")

        if not bookings:
            flash('No bookings available.', 'info')
        return render_template('index.html', bookings=bookings)
    except Exception as e:
        logger.error(f"Error loading index: {str(e)}")
        flash(f'Error loading index: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/process_bookings', methods=['POST'])
def process_bookings_route():
    """
    Route to process bookings from the Head Office database, allocate campsites, and update Cosmos DB.

    :return: Redirects to the summary page if successful or index page if an error occurs.
    """
    global processed_bookings
    try:
        sql_conn = connect_to_sql()
        head_office_conn = connect_to_head_office()
        cosmos_conn = connect_to_cosmos("Bookings")

        raw_bookings = fetch_bookings(head_office_conn)
        bookings = [Booking.from_db_record(record) for record in raw_bookings]
        campsites = initialize_campsites()
        campground_id = 1121132

        process_bookings(bookings, campsites, head_office_conn, cosmos_conn, campground_id)
        processed_bookings = bookings
        flash('Bookings processed successfully!', 'success')
        return redirect(url_for('summary'))
    except Exception as e:
        logger.error(f"Error processing bookings: {str(e)}")
        flash(f'Error processing bookings: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/bookings')
def view_bookings():
    """
    Route to view all bookings currently stored in Cosmos DB.

    :return: Rendered bookings list page.
    """
    try:
        cosmos_conn = connect_to_cosmos("Bookings")
        bookings = fetch_cosmos_bookings(cosmos_conn)
        for booking in bookings:
            logger.info(f"Booking ID: {booking.booking_id}, Customer Name: {booking.customer_name}")

        return render_template('bookings_list.html', bookings=bookings)
    except Exception as e:
        logger.error(f"Error fetching bookings: {str(e)}")
        flash(f'Error fetching bookings: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/summary')
def summary():
    """
    Route to generate and display a summary of the processed bookings.

    :return: Rendered summary page with summary data.
    """
    global processed_bookings
    try:
        bookings = processed_bookings or fetch_cosmos_bookings(connect_to_cosmos("Bookings"))

        if not processed_bookings and bookings:
            campsites = initialize_campsites()
            process_bookings(bookings, campsites, connect_to_head_office(), connect_to_cosmos("Bookings"), campground_id=1121132)
            processed_bookings = bookings
            flash('Bookings were repopulated and processed!', 'info')

        if not bookings:
            flash('No bookings available. Please process the bookings first.', 'warning')
            return redirect(url_for('process_bookings_route'))

        campsites = initialize_campsites()
        summary_data = generate_summary(bookings, campsites)
        logger.info(f"Generated Summary Data: {summary_data}")
        display_summary(summary_data)
        create_and_insert_summary(bookings)
        flash('Summary generated and stored successfully!', 'success')

        return render_template('summary.html', summary=summary_data)
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        flash(f"Error generating summary: {str(e)}", 'danger')
        return redirect(url_for('index'))

@app.route('/pdf/<int:booking_id>')
def show_pdf(booking_id):
    """
    Route to fetch and display a PDF confirmation for a specific booking.

    :param booking_id: ID of the booking whose PDF is to be shown.
    :return: PDF file response for download.
    """
    try:
        cosmos_conn_bookings = connect_to_cosmos("Bookings")
        cosmos_conn_pdfs = connect_to_cosmos("PDFs")
        pdf_data = fetch_pdf_from_cosmos(cosmos_conn_bookings, cosmos_conn_pdfs, booking_id)

        return send_file(
            io.BytesIO(pdf_data),
            mimetype='application/pdf',
            download_name=f'confirmation_{booking_id}.pdf'
        )
    except Exception as e:
        logger.error(f"Error fetching PDF for Booking ID {booking_id}: {str(e)}")
        flash(f'Error fetching PDF for Booking ID {booking_id}: {str(e)}', 'danger')
        return redirect(url_for('view_bookings'))

def fetch_pdf_from_cosmos(cosmos_conn_bookings, cosmos_conn_pdfs, booking_id):
    """
    Fetches PDF data associated with a booking from Cosmos DB.

    :param cosmos_conn_bookings: Cosmos DB connection to the bookings container.
    :param cosmos_conn_pdfs: Cosmos DB connection to the PDFs container.
    :param booking_id: The ID of the booking to fetch the PDF for.
    :return: The PDF data in bytes.
    :raises: ValueError if the booking or PDF data is not found.
    """
    try:
        query_booking = f"SELECT * FROM c WHERE c.booking_id = {booking_id}"
        booking_items = cosmos_conn_bookings.query_items(query=query_booking, enable_cross_partition_query=True)
        booking_list = list(booking_items)

        if not booking_list:
            logger.error(f"Booking not found for booking ID {booking_id}")
            raise ValueError(f"Booking not found for booking ID {booking_id}")

        booking = booking_list[0]
        pdf_id = booking.get('pdf_id')

        if not pdf_id:
            logger.error(f"No pdf_id found for booking ID {booking_id}")
            raise ValueError(f"No pdf_id found for booking ID {booking_id}")

        query_pdf = f"SELECT * FROM c WHERE c.pdf_id = '{pdf_id}'"
        pdf_items = cosmos_conn_pdfs.query_items(query=query_pdf, partition_key=pdf_id, enable_cross_partition_query=True)
        pdf_list = list(pdf_items)

        if not pdf_list:
            logger.error(f"PDF not found for pdf_id {pdf_id}")
            raise ValueError(f"PDF not found for pdf_id {pdf_id}")

        pdf_document = pdf_list[0]
        pdf_data = pdf_document.get('pdf_data')

        if not pdf_data:
            logger.error(f"PDF data not found for pdf_id {pdf_id}")
            raise ValueError(f"PDF data not found for pdf_id {pdf_id}")

        if isinstance(pdf_data, str):
            import base64
            pdf_data = base64.b64decode(pdf_data)

        return pdf_data
    except Exception as e:
        logger.error(f"Failed to fetch PDF data from Cosmos DB: {e}")
        raise

if __name__ == '__main__':
    # Display the Flask app URL on startup only once
    if os.environ.get('FLASK_RUN_FROM_CLI') != 'true':  # Check if Flask is not running from CLI to avoid duplicate messages
        host = '127.0.0.1'
        port = 5000
        print(f"Flask app is running! Access it at http://{host}:{port}/")
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)  # Disable reloader to prevent duplicate messages
