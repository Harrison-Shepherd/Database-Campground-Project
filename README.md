
# Campground Booking Management System

## Overview

This project is a **Campground Booking Management System** designed to help manage bookings, allocate campsites, generate customer confirmations, and create daily summaries. It integrates multiple databases, including SQL Server and Cosmos DB on Microsoft Azure, to handle data storage and retrieval. The application includes a web-based interface built using Flask, enabling users to view, process, and manage bookings seamlessly.

## Features

- **Booking Management**: Download bookings from Head Office, process them, allocate campsites, and update databases.
- **Campsite Allocation**: Dynamically allocates campsites based on availability and size requirements.
- **PDF Generation**: Creates PDF confirmations for bookings and stores them in Cosmos DB.
- **Daily Summaries**: Generates daily summaries of bookings and updates them in SQL Server.
- **Web Interface**: User-friendly web interface built with Flask for viewing and managing bookings and summaries.

## Technologies Used

- **Python**: Core programming language for the application logic.
- **Flask**: Web framework used to build the application's front-end.
- **SQL Server (Microsoft Azure)**: Used for storing customer, booking, and summary data.
- **Cosmos DB (Microsoft Azure)**: NoSQL database used for storing booking records and associated PDF files.
- **PyODBC**: Python library for connecting and interacting with SQL Server.
- **Azure Cosmos SDK**: Library used for connecting and interacting with Cosmos DB.
- **FPDF**: Library used for generating PDFs of booking confirmations and daily summaries.

## Project Structure

```
.
├── app.py                         # Main Flask application file
├── Models                         # Contains data models for booking, campsite, summary, etc.
│   ├── booking.py
│   ├── campsite.py
│   └── summary.py
├── Database                       # Database connection and interaction scripts
│   ├── clean_campsite_data.py     # Script to clean campsite data
│   ├── cosmos_db.py               # Cosmos DB connection and operations
│   ├── head_office_db.py          # Head Office database connection and operations
│   ├── setup_sql.py               # Script to set up SQL database schema
│   └── sql_db.py                  # SQL Server connection and schema setup
├── Front_End                      # Contains the Flask front-end application and templates
│   ├── static                     # Static files for the web interface (CSS, JS, images)
│   │   ├── css
│   │   │   └── styles.css
│   │   ├── images
│   │   └── js
│   └── templates                  # HTML templates for Flask routes
│       ├── booking_detail.html
│       ├── bookings_list.html
│       ├── index.html
│       └── summary.html
├── Utils                          # Utility scripts for handling various functionalities
│   ├── booking_processor.py       # Processes bookings, allocates campsites, and updates databases
│   ├── campsite_manager.py        # Initializes and manages campsite data
│   ├── config_loader.py           # Loads configuration settings from JSON files
│   ├── confirmation.py            # Generates booking confirmations
│   ├── logging_config.py          # Configures logging for the application
│   ├── pdf_generator.py           # Generates PDFs for booking confirmations and summaries
│   └── summary_manager.py         # Handles summary generation and database insertion
├── Tests                          # Contains unit and integration tests for the application
│   ├── test_app.py                # Tests for the Flask application
│   ├── test_booking.py            # Tests for booking functionality
│   ├── test_campsite.py           # Tests for campsite functionality
│   ├── test_booking_processor.py  # Tests for booking processing
│   └── ... (additional test files)
├── pdfs                           # Directory for storing generated PDFs
├── Assets                         # Contains configuration files and SQL scripts
│   ├── connection_strings.json    # Configuration file for database connections
│   └── sql                        # SQL scripts for setting up databases
├── app.log                        # Log file for the application
├── main.py                        # Main script for running database setup and other utilities
└── README.md                      # Project documentation (this file)
```

## Databases Used

### 1. SQL Server (Microsoft Azure)
- **Purpose**: Stores customer, booking, and summary data.
- **Connection Details**:
  - **Server**: `campground-server.database.windows.net`
  - **Database**: `CampgroundBookingsDB`
  - **Authentication**: Uses secure credentials stored in the configuration.

### 2. Cosmos DB (Microsoft Azure)
- **Purpose**: Stores booking records, PDFs of booking confirmations, and summary reports.
- **Connection Details**:
  - **Endpoint**: Provided in the project configuration (`connection_strings.json`)
  - **Key**: Securely stored in configuration files.
  - **Containers**: 
    - `Bookings`: Stores individual booking records.
    - `PDFs`: Stores PDF confirmations.
    - `Summary_PDFs`: Stores summary reports in PDF format.

## Setup Instructions

### Prerequisites

- Python 3.8 or above installed
- Access to Azure SQL Server and Cosmos DB with appropriate credentials
- Virtual environment for managing dependencies

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Databases**:
   - Ensure your Azure SQL and Cosmos DB are set up and credentials are configured in `connection_strings.json`.

5. **Run Database Setup Scripts**:
   - Use provided SQL scripts (`create_head_office_schema.sql`, etc.) to set up your SQL database schema.

6. **Run the Application**:
   ```bash
   python app.py
   ```
   Access the app at `http://127.0.0.1:5000/`.

### Running Tests

- To run the tests, use:
  ```bash
  python -m unittest discover -s Tests
  ```

## Usage

- **Home Page**: View existing bookings fetched from Cosmos DB.
- **Process Bookings**: Download and process new bookings, allocate campsites, and generate confirmations.
- **View Bookings**: View the list of all bookings.
- **Summary**: Generate and view daily summaries of bookings and sales.
- **PDF Viewer**: View booking confirmation PDFs.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any issues or questions, please contact [your-email@example.com](mailto:your-email@example.com).
