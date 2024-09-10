-- noqa: disable=all
-- This query uses a parameterized placeholder for the campground_id
SELECT 
    b.booking_id, 
    b.customer_id, 
    b.booking_date, 
    b.arrival_date, 
    b.campground_id, 
    b.campsite_size, 
    b.num_campsites, 
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name
FROM 
    head_office.booking b
JOIN 
    head_office.customers c ON b.customer_id = c.customer_id
WHERE 
    b.campground_id = ?
