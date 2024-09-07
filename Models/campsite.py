# Models/campsite.py

from datetime import datetime, timedelta

class Campsite:
    def __init__(self, site_number, size, rate):
        self.site_number = site_number
        self.size = size  # 'Small', 'Medium', 'Large'
        self.rate = rate  # Daily rate
        self.available_dates = []  # List of dates when the campsite is available

    def is_available(self, start_date, end_date):
        # Check if the campsite is available between the given start and end dates
        current_date = start_date
        while current_date <= end_date:
            if current_date in self.available_dates:
                return False
            current_date += timedelta(days=1)
        return True

    def book(self, start_date, end_date):
        # Mark dates as booked
        current_date = start_date
        while current_date <= end_date:
            self.available_dates.append(current_date)
            current_date += timedelta(days=1)
