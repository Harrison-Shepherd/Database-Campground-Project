# Front_End/app.py

from flask import Flask, render_template, request, redirect, url_for
from ..Models.booking import Booking  # Import the Booking model

app = Flask(__name__)

# Sample data for bookings; replace with actual database integration later
bookings = [
    Booking(1, "John Doe", "2024-09-07", "Large", 1),
    Booking(2, "Jane Smith", "2024-09-14", "Medium", 2),
]

@app.route('/')
def index():
    # Render the home page with booking information
    return render_template('index.html', bookings=bookings)

@app.route('/booking/<int:booking_id>')
def booking_details(booking_id):
    # Fetch booking details based on booking_id
    booking = next((b for b in bookings if b.booking_id == booking_id), None)
    if not booking:
        return "Booking not found", 404
    return render_template('booking.html', booking=booking)

@app.route('/summary')
def summary():
    # Placeholder until database is integrated
    return render_template('summary.html', summary={"date": "2024-09-07", "total_sales": 1000, "total_bookings": 10})

if __name__ == '__main__':
    app.run(debug=True)
