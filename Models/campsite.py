from datetime import datetime, timedelta

class Campsite:
    def __init__(self, site_number, size, rate, available_dates=None):
        self.site_number = site_number
        self.size = size
        self.rate = rate
        self.available_dates = available_dates if available_dates else []

    def is_available(self, start_date, end_date):
        """
        Check if the campsite is available between the given start and end dates.
        """
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        available = [datetime.strptime(date, "%Y-%m-%d") for date in self.available_dates]

        # Check that all dates in the range from start to end are available
        current_date = start
        while current_date <= end:
            if current_date not in available:
                return False
            current_date += timedelta(days=1)
        return True
