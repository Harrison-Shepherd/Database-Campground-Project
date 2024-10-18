-- This query retrieves booking information, including customer details, using a parameterized placeholder for the campground_id

SELECT 
    b.booking_id,                  -- Booking identifier
    b.customer_id,                 -- Customer identifier associated with the booking
    b.booking_date,                -- Date when the booking was made
    b.arrival_date,                -- Customer's arrival date
    b.campground_id,               -- Identifier of the campground where the booking was made
    b.campsite_size,               -- Size category of the campsite booked (e.g., 'Small', 'Medium', 'Large')
    b.num_campsites,               -- Number of campsites booked
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name  -- Full name of the customer (first and last name concatenated)
FROM 
    camping.booking b
JOIN 
    camping.customers c ON b.customer_id = c.customer_id  -- Join customers to bookings based on customer_id
WHERE 
    b.campground_id = ?  -- Placeholder for the campground_id to be supplied when executing the query
