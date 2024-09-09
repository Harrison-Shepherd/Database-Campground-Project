# Models/booking.py
from datetime import datetime, timedelta, date
from Models.campsite import allocate_campsite
import logging

class Booking:
    def __init__(self, booking_id, customer_id, booking_date, arrival_date, campsite_size, num_campsites, campground_id=None, customer_name=None):
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.booking_date = self._validate_date(booking_date)
        self.arrival_date = self._validate_date(arrival_date)
        self.campsite_size = campsite_size
        self.num_campsites = num_campsites
        self.campground_id = campground_id
        self.campsite_id = None
        self.total_cost = 0
        self.customer_name = customer_name

    def __repr__(self):
        return f"<Booking {self.booking_id} - Customer {self.customer_id}>"

    def _validate_date(self, date_input):
        if isinstance(date_input, datetime):
            return date_input
        elif isinstance(date_input, date):
            return datetime.combine(date_input, datetime.min.time())
        elif isinstance(date_input, str):
            try:
                return datetime.strptime(date_input, '%Y-%m-%d')
            except ValueError:
                raise ValueError(f"Invalid date format for {date_input}. Expected 'YYYY-MM-DD'.")
        else:
            raise TypeError(f"Unsupported date input type: {type(date_input)}")

    def is_arrival_today(self):
        return self.arrival_date.date() == datetime.now().date()

    def update_campsite_info(self, campsite_id, rate_per_night):
        self.campsite_id = campsite_id
        self.total_cost = rate_per_night * 7 * self.num_campsites

    def to_dict(self):
        return {
            "booking_id": self.booking_id,
            "customer_id": self.customer_id,
            "booking_date": self.booking_date.strftime('%Y-%m-%d'),
            "arrival_date": self.arrival_date.strftime('%Y-%m-%d'),
            "campsite_size": self.campsite_size,
            "num_campsites": self.num_campsites,
            "campground_id": self.campground_id,
            "campsite_id": self.campsite_id,
            "total_cost": self.total_cost
        }

    @staticmethod
    def from_db_record(record):
        # Check the length of the record to avoid index out of range errors
        if len(record) < 8:
            logging.error(f"Record does not have enough fields: {record}")
            raise ValueError(f"Record does not have enough fields. Expected 8 fields, got {len(record)}")

        # Create Booking object with all expected fields
        return Booking(
            booking_id=record[0],
            customer_id=record[1],
            booking_date=record[2],
            arrival_date=record[3],
            campground_id=record[4],
            campsite_size=record[5],
            num_campsites=record[6],
            customer_name=record[7]
        )

    @staticmethod
    def adjust_to_saturday(start_date):
        days_to_saturday = (5 - start_date.weekday() + 7) % 7
        if days_to_saturday == 0:
            return start_date
        return start_date + timedelta(days=days_to_saturday)

    def allocate_campsite(self, campsites, head_office_conn, update_booking_campground_func):
        adjusted_start_date = Booking.adjust_to_saturday(self.arrival_date)
        adjusted_end_date = adjusted_start_date + timedelta(days=7)

        allocated_campsite = allocate_campsite(campsites, adjusted_start_date, adjusted_end_date, self)
        if allocated_campsite:
            self.update_campsite_info(allocated_campsite.site_number, allocated_campsite.rate_per_night)
            update_booking_campground_func(head_office_conn, self.booking_id, self.campground_id)
            print(f"Booking {self.booking_id} successfully allocated to Campsite {allocated_campsite.site_number}.")
        else:
            print(f"No available campsites for Booking {self.booking_id} from {adjusted_start_date} to {adjusted_end_date}.")
        return allocated_campsite

def create_booking_data(booking):
    """
    Prepare booking data to be stored in Cosmos DB.
    """
    booking_data = booking.to_dict()
    booking_data["confirmation"] = f"confirmation_{booking.booking_id}.pdf"  # Reference the confirmation PDF
    # Add any additional data fields necessary
    return booking_data
