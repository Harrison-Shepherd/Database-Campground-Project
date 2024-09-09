#Utils/summary_manager.py
from datetime import datetime
from Database.sql_db import insert_summary

def create_and_insert_summary(sql_conn):
    """
    Creates and inserts a daily summary of bookings into the SQL database.
    """
    summary_data = {
        "campground_id": 1121132,  # Replace with your student ID or relevant identifier
        "summary_date": datetime.now().strftime("%Y-%m-%d"),
        "total_sales": 1500.50,  # Example data, replace with actual calculations
        "total_bookings": 12     # Example data, replace with actual calculations
    }
    try:
        insert_summary(sql_conn, summary_data)
        print("Summary inserted successfully.")
    except Exception as e:
        print(f"An error occurred while inserting summary: {e}")
