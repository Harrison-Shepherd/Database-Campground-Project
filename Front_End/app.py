# Front_End/app.py

import sys
import os
from flask import Flask, render_template, request, redirect, url_for

# Add the root directory of your project to the Python path
# This ensures that Python can locate the 'Models' directory when importing
sys.path.insert(0, r"C:\Users\kreti\Database Campground Project")

# Import the Booking model
from Models.booking import Booking

# Initialize the Flask application
app = Flask(__name__)

# Sample data for bookings; replace with actual database integration later
bookings = [
    Booking(1, "John Doe", "2024-09-07", "Large", 1),
    Booking(2, "Jane Smith", "2024-09-14", "Medium", 2),
]

@app.route('/')
def index():
    """
    Route to display the bookings overview page.
    """
    return render_template('index.html', bookings=bookings)

@app.route('/booking/<int:booking_id>')
def booking_details(booking_id):
    """
    Route to display the details of a specific booking.
    """
    booking = next((b for b in bookings if b.booking_id == booking_id), None)
    if not booking:
        return "Booking not found", 404
    return render_template('booking.html', booking=booking)

@app.route('/summary')
def summary():
    """
    Route to display the daily summary page.
    """
    # Placeholder data; replace with actual database integration later
    summary_data = {
        "date": "2024-09-07",
        "total_sales": 1000,
        "total_bookings": 10
    }
    return render_template('summary.html', summary=summary_data)

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
