# Models/customer.py
class Customer:
    def __init__(self, customer_id, first_name, last_name, phone, address, post_code):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.address = address
        self.post_code = post_code

# Models/booking.py
class Booking:
    def __init__(self, booking_id, customer_id, booking_date, arrival_date, campground_id, campsite_size, num_campsites):
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.booking_date = booking_date
        self.arrival_date = arrival_date
        self.campground_id = campground_id
        self.campsite_size = campsite_size
        self.num_campsites = num_campsites

# Models/summary.py
class Summary:
    def __init__(self, summary_id, campground_id, summary_date, total_sales, total_bookings):
        self.summary_id = summary_id
        self.campground_id = campground_id
        self.summary_date = summary_date
        self.total_sales = total_sales
        self.total_bookings = total_bookings
