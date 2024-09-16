# Models/summary.py

from Utils.logging_config import logger


class Summary:
    def __init__(self, campground_id, summary_date, total_sales, total_bookings):
        self.campground_id = campground_id
        self.summary_date = summary_date
        self.total_sales = total_sales
        self.total_bookings = total_bookings

    def to_dict(self):
        """
        Converts the summary object into a dictionary format suitable for database insertion.
        """
        return {
            "campground_id": self.campground_id,
            "summary_date": self.summary_date,
            "total_sales": self.total_sales,
            "total_bookings": self.total_bookings
        }

    def validate(self):
        """
        Validates the summary data to ensure it meets expected constraints.
        """
        if not self.campground_id or not self.summary_date:
            raise ValueError("Campground ID and summary date must not be empty.")
        if self.total_sales < 0 or self.total_bookings < 0:
            raise ValueError("Total sales and bookings cannot be negative.")
