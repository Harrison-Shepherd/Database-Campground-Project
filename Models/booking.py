# Models/booking.py

class Booking:
    def __init__(self, booking_id, customer_name, arrival_date, campsite_size, num_campsites):
        self.booking_id = booking_id
        self.customer_name = customer_name
        self.arrival_date = arrival_date
        self.campsite_size = campsite_size
        self.num_campsites = num_campsites

    def __repr__(self):
        return f"<Booking {self.booking_id} - {self.customer_name}>"
