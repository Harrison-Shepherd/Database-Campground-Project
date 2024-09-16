from fpdf import FPDF
import os
from Utils.logging_config import logger

# Define the folder to save PDFs
PDF_FOLDER = "pdfs"

# Ensure the folder exists
os.makedirs(PDF_FOLDER, exist_ok=True)

class PDFGenerator(FPDF):
    def __init__(self, title):
        """
        Initializes the PDF generator with a title.

        :param title: The title of the PDF document.
        """
        super().__init__()
        self.title = title

    def header(self):
        """
        Sets the header for the PDF document.
        """
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, self.title, 0, 1, "C")

    def footer(self):
        """
        Sets the footer for the PDF document, including the page number.
        """
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def generate_confirmation(self, booking):
        """
        Generates a confirmation PDF for a booking.

        :param booking: Booking object containing booking details.
        :return: The path to the generated PDF file.
        """
        self.add_page()
        self.set_font("Arial", "", 12)
        self.cell(0, 10, f"Booking Confirmation - {booking.customer_name}", 0, 1)
        self.cell(0, 10, f"Booking ID: {booking.booking_id}", 0, 1)
        self.cell(0, 10, f"Customer: {booking.customer_name}", 0, 1)
        self.cell(0, 10, f"Arrival Date: {booking.arrival_date.strftime('%Y-%m-%d')}", 0, 1)
        self.cell(0, 10, f"Campsite Size: {booking.campsite_size}", 0, 1)
        self.cell(0, 10, f"Total Sites Booked: {booking.num_campsites}", 0, 1)
        self.cell(0, 10, f"Total Cost: ${booking.total_cost:.2f}", 0, 1)

        filename = os.path.join(PDF_FOLDER, f"confirmation_{booking.booking_id}.pdf")
        self.output(filename)
        logger.info(f"Confirmation PDF generated and saved as {filename}.")
        return filename

    def generate_summary(self, summary):
        """
        Generates a summary PDF for a day's bookings.

        :param summary: Summary object containing the summary data.
        :return: The path to the generated PDF file.
        """
        self.add_page()
        self.set_font("Arial", "", 12)
        self.cell(0, 10, "Daily Summary Report", ln=True, align="C")
        self.cell(0, 10, f"Campground ID: {summary.campground_id}", ln=True)
        self.cell(0, 10, f"Summary Date: {summary.summary_date}", ln=True)
        self.cell(0, 10, f"Total Sales: ${summary.total_sales:.2f}", ln=True)
        self.cell(0, 10, f"Total Bookings: {summary.total_bookings}", ln=True)

        filename = os.path.join(PDF_FOLDER, f"summary_{summary.summary_date}.pdf")
        self.output(filename)
        logger.info(f"Summary PDF generated and saved as {filename}.")
        return filename
