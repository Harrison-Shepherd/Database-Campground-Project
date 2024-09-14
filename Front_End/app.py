# Front_End/app.py
import sys
import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash

# Configure logging to display errors and debug information
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now, you can import your modules
from Models.booking import Booking
from Utils.booking_processor import process_bookings
from Utils.campsite_manager import initialize_campsites
from Utils.summary_manager import create_and_insert_summary, generate_summary, display_summary
from Database.sql_db import connect_to_sql
from Database.cosmos_db import connect_to_cosmos, fetch_cosmos_bookings
from Database.head_office_db import connect_to_head_office, fetch_bookings

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flashing messages

@app.route('/')
def index():
    """
    Home page displaying options for processing bookings, viewing summaries, etc.
    """
    return render_template('index.html')

@app.route('/process_bookings', methods=['POST'])
def process_bookings_route():
    """
    Route to process bookings from Head Office and store in Cosmos DB.
    """
    try:
        sql_conn = connect_to_sql()
        head_office_conn = connect_to_head_office()
        cosmos_conn = connect_to_cosmos(container_name="Bookings")  # Make sure to pass the correct container name

        # Fetch bookings from the Head Office database
        raw_bookings = fetch_bookings(head_office_conn)
        bookings = [Booking.from_db_record(record) for record in raw_bookings]

        # Initialize campsites
        campsites = initialize_campsites()

        # Process bookings
        campground_id = 1121132  # Replace with your specific ID
        process_bookings(bookings, campsites, head_office_conn, cosmos_conn, campground_id)

        flash('Bookings processed successfully!', 'success')
        return redirect(url_for('index'))
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
        cosmos_conn = connect_to_cosmos(container_name="Bookings")
        bookings_data = fetch_cosmos_bookings(cosmos_conn)
        bookings = [Booking.from_dict(b) for b in bookings_data]  # Ensure that bookings are converted to Booking objects
        return render_template('bookings.html', bookings=bookings)
    except Exception as e:
        logging.error(f"Error fetching bookings: {str(e)}")
        flash(f'Error fetching bookings: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/summary')
def summary():
    """
    Route to display the daily summary of bookings.
    """
    try:
        cosmos_conn = connect_to_cosmos(container_name="Bookings")
        bookings_data = fetch_cosmos_bookings(cosmos_conn)
        bookings = [Booking.from_dict(b) for b in bookings_data]  # Convert fetched data to Booking objects
        campsites = initialize_campsites()  # Initialize campsites if needed for the summary

        # Generate and display the summary
        summary_data = generate_summary(bookings, campsites)
        display_summary(summary_data)

        # Create and insert summary into the database
        create_and_insert_summary(bookings)
        flash('Summary generated and stored successfully!', 'success')
        return render_template('summary.html', summary=summary_data)
    except Exception as e:
        logging.error(f"Error generating summary: {str(e)}")
        flash(f'Error generating summary: {str(e)}', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
