# Utils/confirmation.py

from fpdf import FPDF

class ConfirmationPDF(FPDF):
    def __init__(self, booking):
        super().__init__()
        self.booking = booking

    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"Booking Confirmation - {self.booking.customer_name}", 0, 1, "C")

    def add_booking_details(self):
        self.set_font("Arial", "", 12)
        self.cell(0, 10, f"Booking ID: {self.booking.booking_id}", 0, 1)
        self.cell(0, 10, f"Customer: {self.booking.customer_name}", 0, 1)
        self.cell(0, 10, f"Arrival Date: {self.booking.arrival_date}", 0, 1)
        self.cell(0, 10, f"Campsite Size: {self.booking.campsite_size}", 0, 1)
        self.cell(0, 10, f"Total Sites Booked: {self.booking.num_campsites}", 0, 1)

    def generate_pdf(self, filename):
        self.add_page()
        self.add_booking_details()
        self.output(filename)

# Example usage:
def generate_confirmation(booking):
    pdf = ConfirmationPDF(booking)
    filename = f"confirmation_{booking.booking_id}.pdf"
    pdf.generate_pdf(filename)
    print(f"Confirmation saved as {filename}.")
