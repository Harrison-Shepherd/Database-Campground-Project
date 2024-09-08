#Models/campsite.py
from datetime import datetime

class Campsite:
    def __init__(self, site_number, size):
        self.site_number = site_number
        self.size = size
        self.bookings = []  # A list of tuples (start_date, end_date)

    def is_available(self, start_date, end_date):
        """
        Checks if the campsite is available for the given date range.
        :param start_date: Start date of the booking.
        :param end_date: End date of the booking.
        :return: True if the campsite is available, False otherwise.
        """
        for existing_start, existing_end in self.bookings:
            # Check for overlapping bookings
            if not (end_date <= existing_start or start_date >= existing_end):
                # Overlap detected
                return False
        return True

    def book_campsite(self, start_date, end_date):
        """
        Books the campsite for the given date range if available.
        :param start_date: Start date of the booking.
        :param end_date: End date of the booking.
        :return: True if booking is successful, False otherwise.
        """
        if self.is_available(start_date, end_date):
            self.bookings.append((start_date, end_date))
            print(f"Campsite {self.site_number} booked from {start_date} to {end_date}.")
            return True
        else:
            print(f"Campsite {self.site_number} is not available from {start_date} to {end_date}.")
            return False

def allocate_campsite(campsites, start_date, end_date, booking):
    """
    Allocates a campsite based on the availability between the start and end dates.
    :param campsites: List of Campsite objects.
    :param start_date: Start date of the booking.
    :param end_date: End date of the booking.
    :param booking: Booking details.
    :return: The allocated campsite object or None if no campsite is available.
    """
    for campsite in campsites:
        if campsite.is_available(start_date, end_date):
            # Book the campsite if available
            if campsite.book_campsite(start_date, end_date):
                return campsite
    # Return None if no available campsite is found
    return None
