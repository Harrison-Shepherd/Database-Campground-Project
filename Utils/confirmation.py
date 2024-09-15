# Utils/confirmation.py
import os
from fpdf import FPDF
from Database.cosmos_db import connect_to_cosmos, insert_booking_pdfs_to_cosmos  # Updated to use the correct function

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

def generate_confirmation(booking):
    """
    Generates a confirmation PDF for the given booking and inserts it into the Cosmos DB.
    
    :param booking: The booking object containing the details to be included in the PDF.
    """
    # Define the folder path for saving PDFs
    folder_path = "pdfs"
    os.makedirs(folder_path, exist_ok=True)
    filename = os.path.join(folder_path, f"confirmation_{booking.booking_id}.pdf")

    # Generate and save the PDF
    pdf = ConfirmationPDF(booking)
    pdf.generate_pdf(filename)
    print(f"Confirmation saved as {filename}.")

    # Insert the confirmation PDF into Cosmos DB with the correct parameters
    try:
        cosmos_container = connect_to_cosmos("PDFs")  # Connect to the PDFs container
        insert_booking_pdfs_to_cosmos(cosmos_container, filename, booking.booking_id)  # Insert using the refactored function
        print(f"Confirmation PDF {filename} inserted into Cosmos DB successfully.")
    except Exception as e:
        print(f"An error occurred while inserting the confirmation PDF: {e}")
