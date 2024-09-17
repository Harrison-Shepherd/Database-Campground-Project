-- This query inserts a new summary record into the 'HeadOfficeSummaries' table using named parameters

INSERT INTO HeadOfficeSummaries (
    campground_id,   -- Identifier of the campground for the summary record
    summary_date,    -- Date of the summary record
    total_sales,     -- Total sales amount for the given date
    total_bookings   -- Total number of bookings for the given date
) 
VALUES (
    @campground_id,   -- Parameter for the campground ID
    @summary_date,    -- Parameter for the summary date
    @total_sales,     -- Parameter for the total sales amount
    @total_bookings   -- Parameter for the total number of bookings
);
