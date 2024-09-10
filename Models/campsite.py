#Models/campsite.py
from datetime import datetime, timedelta

class Campsite:
    def __init__(self, site_number, size, rate_per_night):
        self.site_number = site_number
        self.size = size
        self.rate_per_night = rate_per_night
        self.bookings = []  # A list of tuples (start_date, end_date)

    def is_available(self, start_date, end_date):
        """
        Checks if the campsite is available for the given date range.
        :param start_date: Start date of the booking.
        :param end_date: End date of the booking.
        :return: True if the campsite is available, False otherwise.
        """
        # Check availability for each week in the booking period
        current_date = start_date
        while current_date < end_date:
            next_week = current_date + timedelta(days=7)
            for existing_start, existing_end in self.bookings:
                # Check for overlaps with existing bookings
                if current_date < existing_end and next_week > existing_start:
                    return False
            current_date = next_week
        return True

    def book_campsite(self, start_date, end_date):
        """
        Books the campsite for the given date range if available.
        :param start_date: Start date of the booking.
        :param end_date: End date of the booking.
        :return: True if booking is successful, False otherwise.
        """
        if self.is_available(start_date, end_date):
            # Book campsite week-by-week within the requested period
            current_date = start_date
            while current_date < end_date:
                next_week = current_date + timedelta(days=7)
                self.bookings.append((current_date, next_week))
                current_date = next_week
            return True
        return False

def allocate_campsite(campsites, start_date, end_date, booking):
    """
    Allocates a campsite based on the availability between the start and end dates.
    :param campsites: List of Campsite objects.
    :param start_date: Start date of the booking.
    :param end_date: End date of the booking.
    :param booking: Booking object containing booking details.
    :return: The allocated campsite object or None if no campsite is available.
    """
    print(f"Attempting to allocate Booking {booking.booking_id} from {start_date.date()} to {end_date.date()}...")
    for campsite in campsites:
        # Try to allocate an available campsite
        if campsite.is_available(start_date, end_date):
            if campsite.book_campsite(start_date, end_date):
                print(f"Booking {booking.booking_id} successfully allocated to Campsite {campsite.site_number}.")
                return campsite
    print(f"No available campsites for Booking {booking.booking_id} from {start_date.date()} to {end_date.date()}.")
    return None
