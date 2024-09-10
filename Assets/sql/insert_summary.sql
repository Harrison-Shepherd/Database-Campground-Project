-- noqa: disable=all
-- This query uses parameterized placeholders for use with pyodbc
INSERT INTO camping.summary (campground_id, summary_date, total_sales, total_bookings)
VALUES (?, ?, ?, ?)