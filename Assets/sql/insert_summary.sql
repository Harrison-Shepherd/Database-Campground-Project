-- This query inserts a new summary record into the 'camping.summary' table using parameterized placeholders for secure execution with pyodbc

INSERT INTO camping.summary (
    campground_id,    -- Identifier of the campground for the summary record
    summary_date,     -- Date of the summary
    total_sales,      -- Total sales amount for the day
    total_bookings    -- Total number of bookings for the day
) 
VALUES (?, ?, ?, ?);  -- Parameterized placeholders to be filled with actual values when executing the query with pyodbc
