# Utils/confirmation.py
import os
from fpdf import FPDF
from Database.cosmos_db import connect_to_cosmos, insert_pdf_to_cosmos

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

# Function to generate confirmation and save in a folder
def generate_confirmation(booking):
    # Define the folder path
    folder_path = "pdfs"  # Updated to match the folder name
    os.makedirs(folder_path, exist_ok=True)
    filename = os.path.join(folder_path, f"confirmation_{booking.booking_id}.pdf")

    # Generate and save the PDF
    pdf = ConfirmationPDF(booking)
    pdf.generate_pdf(filename)
    print(f"Confirmation saved as {filename}.")

    # Insert the confirmation PDF into Cosmos DB
    try:
        cosmos_container = connect_to_cosmos("PDFs")
        insert_pdf_to_cosmos(cosmos_container, filename)
        print(f"Confirmation PDF {filename} inserted into Cosmos DB successfully.")
    except Exception as e:
        print(f"An error occurred while inserting the confirmation PDF: {e}")
