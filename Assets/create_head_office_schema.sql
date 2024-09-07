-- create_head_office_schema.sql

-- Create the 'head_office' schema
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'head_office')
BEGIN
    EXEC ('CREATE SCHEMA head_office')
END;

-- Create tables within the 'head_office' schema
CREATE TABLE head_office.customers (
    customer_id INT IDENTITY(1,1) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    phone VARCHAR(25) NULL,
    address VARCHAR(255) NULL,
    post_code VARCHAR(4) NULL
);

CREATE TABLE head_office.booking (
    booking_id INT IDENTITY(1,1) PRIMARY KEY,
    customer_id INT NULL FOREIGN KEY REFERENCES head_office.customers(customer_id),
    booking_date DATE NOT NULL,
    arrival_date DATE NOT NULL,
    campground_id INT NOT NULL,
    campsite_size VARCHAR(10),
    num_campsites INT
);

CREATE TABLE head_office.summary (
    summary_id INT IDENTITY(1,1) PRIMARY KEY,
    campground_id INT NULL,
    summary_date DATE NULL,
    total_sales DECIMAL(10, 2) NULL,
    total_bookings INT NULL
);
