
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

├── Assets                                      # Contains configuration files and SQL scripts
│   ├── connection_strings.json                 # Configuration file for database connections
│   ├── requirements.txt                        # txt file with all of the relevant python libraries you need to install.
│   └── sql                                     # SQL scripts for setting up databases
│       ├── create_head_office_schema.sql
│       ├── fetch_bookings.sql
│       ├── insert_summary.sql
│       ├── load_head_office_data.sql
│       └── write_summary_to_head_office.sql
├── Database                                    # Database connection and interaction scripts
│   ├── clean_campsite_data.py                  # Script to clean campsite data
│   ├── cosmos_db.py                            # Cosmos DB connection and operations
│   ├── head_office_db.py                       # Head Office database connection and operations
│   ├── setup_sql.py                            # Script to set up SQL database schema 
│   └── sql_db.py                               # SQL Server connection and schema setup
├── Front_End                                   # Contains the Flask front-end application and templates
│   ├── app.py                                  # Main Flask application file
│   ├── static                                  # Static files for the web interface (CSS, JS, images)
│   │   ├── css
│   │   │   └── styles.css
│   │   ├── images
│   │   └── js
│   └── templates                               # HTML templates for Flask routes
│       ├── booking_detail.html
│       ├── bookings_list.html
│       ├── index.html
│       └── summary.html
├── Models                                      # Contains data models for booking, campsite, summary, etc.
│   ├── booking.py
│   ├── campsite.py
│   └── summary.py
├── pdfs                                        # Directory for storing generated PDFs
├── Tests                                       # Contains unit and integration tests for the application
│   ├── test_booking_processor.py               # Tests for booking processing                      
│   ├── test_booking.py                         # Tests for booking functions
│   ├── test_campsite_manager.py                # Tests for campsite functionality
│   ├── test_campsite.py                        # Tests core campsite functions
│   ├── test_config_loader.py                   # Tests configuration functions such as connection strings
│   ├── test_confirmation.py                    # Tests booking confirmations
│   ├── test_cosmos_db.py                       # Tests cosmos DB connection and functions
│   ├── test_main.py                            # Tests main execution
│   ├── test_pdf_generation.py                  # Tests PDF generation
│   ├── test_sql_db.py                          # Tests SQL server queries and data
│   └── test_summary_manager.py                 # Tests summary generation
├── Utils                                       # Utility scripts for handling various functionalities
│   ├── booking_processor.py                    # Processes bookings, allocates campsites, and updates databases
│   ├── campsite_manager.py                     # Initializes and manages campsite data
│   ├── config_loader.py                        # Loads configuration settings from JSON files
│   ├── confirmation.py                         # Generates booking confirmations
│   ├── logging_config.py                       # Configures logging for the application
│   ├── pdf_generator.py                        # Generates PDFs for booking confirmations and summaries
│   └── summary_manager.py                      # Handles summary generation and database insertion                  
├── app.log                                     # Log file for the application
├── main.py                                     # Main script for running database setup and other utilities
├── README.md                                   # Project documentation (this file)
└──retrieve_booking.py                          # Script to retrieve a single booking information

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
### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Harrison-Shepherd/Database-Campground-Project
   cd Database-Campground-Project
   ```

2. **Configure Databases**:
   - Ensure the Azure SQL and Cosmos DB are set up and credentials are configured in `connection_strings.json`.

3. **Run Database Setup Scripts**:
   - Use provided SQL scripts (`create_head_office_schema.sql`, etc.) to set up the SQL database schema.

6. **Run the Application**:
   ```bash
   python app.py
   python main.py #one of these
   ```
   Access the app at `http://127.0.0.1:5000/`.

### Running Tests

- To run the tests, use:
  ```bash
  python -m unittest discover -s Tests
  ```

### For Andrew:
pip install -r requirements.txt # has all of the imports incase something is wrong

connection_strings.json has all of the connection details for Azure SQL database, Cosmos DB, and head office DB. 

python Front_End/app.py runs the Flask application | you can access it at http://127.0.0.1:5000

python main.py processes all of the bookings if you just want to see that.

python retrieve_booking.py prompts you for a booking ID to retrieve their details. 

python -m unittest discover -s Tests | This runs all of the test cases. There are 18.

Please let me know if you need anything else or a file was corrupted. HJS028@student.usc.edu.au, 1121132.


