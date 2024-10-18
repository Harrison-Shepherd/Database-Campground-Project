-- This query inserts a new summary record into the 'camping.summary' table using placeholders for parameters

INSERT INTO camping.summary (
    campground_id,   -- Identifier of the campground for the summary record
    summary_date,    -- Date of the summary record
    total_sales,     -- Total sales amount for the given date
    total_bookings   -- Total number of bookings for the given date
) 
VALUES (
    ?,   -- Placeholder for the campground ID
    ?,   -- Placeholder for the summary date
    ?,   -- Placeholder for the total sales amount
    ?    -- Placeholder for the total number of bookings
);
