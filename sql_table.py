import sqlite3

table = sqlite3.connect('hotel_booking.db')
cursor = table.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,      
    person TEXT NOT NULL,                      
    start_date DATE NOT NULL,                  
    end_date DATE NOT NULL,                    
    roomtype TEXT CHECK (roomtype IN ('normal', 'deluxe', 'suite')) NOT NULL,  
    number_guests INTEGER NOT NULL,            
    email TEXT NOT NULL,                       
    card TEXT NOT NULL                     
);
"""

cursor.execute(create_table_query)
table.commit()
table.close()
