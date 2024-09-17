-- create_head_office_schema.sql

-- Create the 'head_office' schema if it does not exist
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'head_office')
BEGIN
    EXEC ('CREATE SCHEMA head_office')
END;

-- Create the 'customers' table within the 'head_office' schema
CREATE TABLE head_office.customers (
    customer_id INT IDENTITY(1,1) PRIMARY KEY,  -- Primary key with auto-increment
    first_name VARCHAR(255) NOT NULL,           -- Customer's first name
    last_name VARCHAR(255) NOT NULL,            -- Customer's last name
    phone VARCHAR(25) NULL,                     -- Customer's phone number (optional)
    address VARCHAR(255) NULL,                  -- Customer's address (optional)
    post_code VARCHAR(4) NULL                   -- Customer's postal code (optional)
);

-- Create the 'booking' table within the 'head_office' schema
CREATE TABLE head_office.booking (
    booking_id INT IDENTITY(1,1) PRIMARY KEY,                       -- Primary key with auto-increment
    customer_id INT NULL FOREIGN KEY REFERENCES head_office.customers(customer_id),  -- Foreign key referencing 'customers' table
    booking_date DATE NOT NULL,                                     -- Date when the booking was made
    arrival_date DATE NOT NULL,                                     -- Customer's arrival date
    campground_id INT NOT NULL,                                     -- Identifier of the campground
    campsite_size VARCHAR(10),                                      -- Size category of the campsite (e.g., 'Small', 'Medium', 'Large')
    num_campsites INT                                               -- Number of campsites booked
);

-- Create the 'summary' table within the 'head_office' schema
CREATE TABLE head_office.summary (
    summary_id INT IDENTITY(1,1) PRIMARY KEY,   -- Primary key with auto-increment
    campground_id INT NULL,                     -- Identifier of the campground
    summary_date DATE NULL,                     -- Date of the summary
    total_sales DECIMAL(10, 2) NULL,            -- Total sales amount for the day
    total_bookings INT NULL                     -- Total number of bookings for the day
);
