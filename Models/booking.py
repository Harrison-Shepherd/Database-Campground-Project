#Models/booking.py
from datetime import datetime

class Booking:
    def __init__(self, booking_id, customer_name, booking_date, arrival_date, campsite_size, num_campsites, campground_id=None):
        self.booking_id = booking_id
        self.customer_name = customer_name
        self.booking_date = self._validate_date(booking_date)
        self.arrival_date = self._validate_date(arrival_date)
        self.campsite_size = campsite_size
        self.num_campsites = num_campsites
        self.campground_id = campground_id  # Optional, can be used to track the assigned campground

    def __repr__(self):
        return f"<Booking {self.booking_id} - {self.customer_name}>"

    def _validate_date(self, date_str):
        """
        Validates and converts a string date to a datetime object.
        :param date_str: Date string in 'YYYY-MM-DD' format.
        :return: A datetime object.
        """
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Invalid date format for {date_str}. Expected 'YYYY-MM-DD'.")

    def is_arrival_today(self):
        """
        Checks if the booking's arrival date is today.
        :return: True if arrival date is today, otherwise False.
        """
        return self.arrival_date.date() == datetime.now().date()

    def update_campsite_info(self, campsite_id, rate_per_night):
        """
        Updates the booking information with assigned campsite details.
        :param campsite_id: The ID of the assigned campsite.
        :param rate_per_night: The rate per night for the campsite.
        """
        self.campsite_id = campsite_id
        self.total_cost = rate_per_night * 7 * self.num_campsites  # Assuming all bookings are for 7 days
        print(f"Booking {self.booking_id} updated with Campsite {campsite_id} and cost {self.total_cost}.")

    def to_dict(self):
        """
        Converts the booking object into a dictionary format, useful for database operations.
        :return: A dictionary representing the booking.
        """
        return {
            "booking_id": self.booking_id,
            "customer_name": self.customer_name,
            "booking_date": self.booking_date.strftime('%Y-%m-%d'),
            "arrival_date": self.arrival_date.strftime('%Y-%m-%d'),
            "campsite_size": self.campsite_size,
            "num_campsites": self.num_campsites,
            "campground_id": self.campground_id,
        }
