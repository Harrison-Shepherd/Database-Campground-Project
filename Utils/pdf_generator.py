from fpdf import FPDF
import os
from Utils.logging_config import logger

# Define the folder to save PDFs
PDF_FOLDER = "pdfs"

# Ensure the folder exists
os.makedirs(PDF_FOLDER, exist_ok=True)  # Create the folder if it doesn't already exist

class PDFGenerator(FPDF):
    """
    A class to generate PDFs for booking confirmations and daily summaries.
    """

    def __init__(self, title):
        """
        Initializes the PDF generator with a title.

        :param title: The title of the PDF document.
        """
        super().__init__()
        self.title = title  # Set the title of the PDF

    def header(self):
        """
        Sets the header for the PDF document.
        """
        self.set_font("Arial", "B", 12)  # Set the font for the header
        self.cell(0, 10, self.title, 0, 1, "C")  # Add the title centered at the top of the page

    def footer(self):
        """
        Sets the footer for the PDF document, including the page number.
        """
        self.set_y(-15)  # Position footer 15 units from the bottom
        self.set_font("Arial", "I", 8)  # Set the font for the footer
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")  # Add page number centered at the bottom

    def generate_confirmation(self, booking):
        """
        Generates a confirmation PDF for a booking.

        :param booking: Booking object containing booking details.
        :return: The path to the generated PDF file.
        """
        self.add_page()  # Add a new page to the PDF
        self.set_font("Arial", "", 12)  # Set the font for the content
        # Add booking details to the PDF
        self.cell(0, 10, f"Booking Confirmation - {booking.customer_name}", 0, 1) # Add the title centered on the page
        self.cell(0, 10, f"Booking ID: {booking.booking_id}", 0, 1) # Add the booking ID
        self.cell(0, 10, f"Customer: {booking.customer_name}", 0, 1) # Add the customer name
        self.cell(0, 10, f"Arrival Date: {booking.arrival_date.strftime('%Y-%m-%d')}", 0, 1) # Add the arrival date
        self.cell(0, 10, f"Campsite Size: {booking.campsite_size}", 0, 1) # Add the campsite size
        self.cell(0, 10, f"Total Sites Booked: {booking.num_campsites}", 0, 1) # Add the number of campsites
        self.cell(0, 10, f"Total Cost: ${booking.total_cost:.2f}", 0, 1) # Add the total cost

        # Define the filename and save the PDF
        filename = os.path.join(PDF_FOLDER, f"confirmation_{booking.booking_id}.pdf")
        self.output(filename)  # Output the PDF to the specified file
        logger.info(f"Confirmation PDF generated and saved as {filename}.")
        return filename  # Return the path to the generated PDF

    def generate_summary(self, summary):
        """
        Generates a summary PDF for a day's bookings.

        :param summary: Summary object containing the summary data.
        :return: The path to the generated PDF file.
        """
        self.add_page()  # Add a new page to the PDF
        self.set_font("Arial", "", 12)  # Set the font for the content
        # Add summary details to the PDF
        self.cell(0, 10, "Daily Summary Report", ln=True, align="C") # Add the title centered on the page
        self.cell(0, 10, f"Campground ID: {summary.campground_id}", ln=True) # Add the campground ID
        self.cell(0, 10, f"Summary Date: {summary.summary_date}", ln=True) # Add the summary date
        self.cell(0, 10, f"Total Sales: ${summary.total_sales:.2f}", ln=True) # Add the total sales
        self.cell(0, 10, f"Total Bookings: {summary.total_bookings}", ln=True) # Add the total bookings

        # Define the filename and save the PDF
        filename = os.path.join(PDF_FOLDER, f"summary_{summary.summary_date}.pdf")
        self.output(filename)  # Output the PDF to the specified file
        logger.info(f"Summary PDF generated and saved as {filename}.")
        return filename  # Return the path to the generated PDF
