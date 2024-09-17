from Utils.logging_config import logger

class Summary:
    def __init__(self, campground_id, summary_date, total_sales, total_bookings):
        """
        Initializes a Summary object.

        :param campground_id: ID of the campground.
        :param summary_date: Date of the summary.
        :param total_sales: Total sales amount for the summary period.
        :param total_bookings: Total number of bookings for the summary period.
        """
        self.campground_id = campground_id
        self.summary_date = summary_date
        self.total_sales = total_sales
        self.total_bookings = total_bookings

    def to_dict(self):
        """
        Converts the Summary object into a dictionary format suitable for database insertion.

        :return: Dictionary containing summary details.
        """
        return {
            "campground_id": self.campground_id,
            "summary_date": self.summary_date,
            "total_sales": self.total_sales,
            "total_bookings": self.total_bookings
        }

    def validate(self):
        """
        Validates the Summary object data to ensure it meets expected constraints.

        :raises ValueError: If any required fields are empty or if any values are negative.
        """
        # Check if campground_id and summary_date are not empty
        if not self.campground_id or not self.summary_date:
            logger.error("Validation Error: Campground ID and summary date must not be empty.")
            raise ValueError("Campground ID and summary date must not be empty.")
        
        # Ensure total sales and bookings are non-negative
        if self.total_sales < 0 or self.total_bookings < 0:
            logger.error("Validation Error: Total sales and bookings cannot be negative.")
            raise ValueError("Total sales and bookings cannot be negative.")
