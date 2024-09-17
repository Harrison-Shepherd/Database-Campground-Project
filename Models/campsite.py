from datetime import datetime, timedelta
from Utils.logging_config import logger

class Campsite:
    def __init__(self, site_number, size, rate_per_night):
        """
        Initializes a Campsite object.

        :param site_number: The number of the campsite.
        :param size: The size category of the campsite (e.g., 'Small', 'Medium', 'Large').
        :param rate_per_night: The rate per night for the campsite.
        """
        self.site_number = site_number
        self.size = size
        self.rate_per_night = rate_per_night
        self.bookings = []  # A list to keep track of booked periods as tuples (start_date, end_date)

    def is_available(self, start_date, end_date):
        """
        Checks if the campsite is available for the given date range.

        :param start_date: Start date of the booking.
        :param end_date: End date of the booking.
        :return: True if the campsite is available, False otherwise.
        """
        # Check each week within the requested booking period
        current_date = start_date
        while current_date < end_date:
            next_week = current_date + timedelta(days=7)
            for existing_start, existing_end in self.bookings:
                # Check for overlapping bookings
                if current_date < existing_end and next_week > existing_start:
                    return False  # Return False if any overlap is found
            current_date = next_week
        return True  # Return True if no overlaps are detected

    def book_campsite(self, start_date, end_date):
        """
        Books the campsite for the given date range if available.

        :param start_date: Start date of the booking.
        :param end_date: End date of the booking.
        :return: True if booking is successful, False otherwise.
        """
        if self.is_available(start_date, end_date):
            # Book the campsite week-by-week within the specified period
            current_date = start_date
            while current_date < end_date:
                next_week = current_date + timedelta(days=7)
                self.bookings.append((current_date, next_week))  # Add each week to the bookings list
                current_date = next_week
            return True
        return False  # Return False if the campsite is not available

def allocate_campsite(campsites, start_date, end_date, booking):
    """
    Allocates a campsite based on the availability between the start and end dates.

    :param campsites: List of Campsite objects.
    :param start_date: Start date of the booking.
    :param end_date: End date of the booking.
    :param booking: Booking object containing booking details.
    :return: The allocated campsite object or None if no campsite is available.
    """
    logger.info(f"Attempting to allocate Booking {booking.booking_id} from {start_date.date()} to {end_date.date()}...")
    for campsite in campsites:
        # Check each campsite for availability
        if campsite.is_available(start_date, end_date):
            # Book the first available campsite found
            if campsite.book_campsite(start_date, end_date):
                logger.info(f"Booking {booking.booking_id} successfully allocated to Campsite {campsite.site_number}.")
                return campsite  # Return the successfully allocated campsite
    logger.warning(f"No available campsites for Booking {booking.booking_id} from {start_date.date()} to {end_date.date()}.")
    return None  # Return None if no campsites are available
