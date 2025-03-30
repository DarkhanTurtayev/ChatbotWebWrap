import sqlite3
from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

# CONNECT to database (from sql_table.py generated file)
def connect_db():
    conn = sqlite3.connect('hotel_booking.db')
    print('Connection to database succesfull')
    return conn

# Checking if given dates and roomtype is avaialble
def check_room_availability(roomtype, start_date, end_date):
    conn = connect_db()
    cursor = conn.cursor()

    # SQL query to check availability
    query = """
    SELECT * FROM bookings
    WHERE roomtype = ?
    AND (
        (start_date <= ? AND end_date >= ?)
        OR (start_date BETWEEN ? AND ?)
        OR (end_date BETWEEN ? AND ?)
    );
    """
    cursor.execute(query, (roomtype, end_date, start_date, start_date, end_date, start_date, end_date))
    bookings = cursor.fetchall()

    conn.close()

    # Negative responce for occupancy scenario
    return len(bookings) == 0

# Adding new booking func
def insert_booking(person, start_date, end_date, roomtype, number_guests, email, card):
    conn = connect_db()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO bookings (person, start_date, end_date, roomtype, number_guests, email, card)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """
    cursor.execute(insert_query, (person, start_date, end_date, roomtype, number_guests, email, card))

    conn.commit()
    conn.close()
    print("Booking succesfull")

#=========================FLASK route==============================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/webhook', methods=['POST'])

def webhook():
    # receiving info (JSON) from dialogflow 
    req = request.get_json(silent=True, force=True)

    # getting info from JSON
    output_contexts = req.get('queryResult').get('outputContexts', [])
    extracted_params = {}

    # filtering parameters
    for context in output_contexts:
        if 'parameters' in context:
            parameters = context['parameters']
            extracted_params.update(parameters)

    # getting information we need
    person = extracted_params.get('person', {}).get('name')
    roomtype = extracted_params.get('roomtype')
    roomtype = roomtype.lower() 
    number_guests = extracted_params.get('number_guests')
    card_number = extracted_params.get('card')
    email = extracted_params.get('email')
    date_period = extracted_params.get('date-period')
    
    # formating data to more accuarte format (refactoring ISO format)
    start_date_iso = date_period.get('startDate')
    end_date_iso = date_period.get('endDate')
    start_date = datetime.fromisoformat(start_date_iso[:-6]).date()
    end_date = datetime.fromisoformat(end_date_iso[:-6]).date()

    # applying availability check logic
    if check_room_availability(roomtype, start_date, end_date):
        insert_booking(person, start_date, end_date, roomtype, number_guests, email, card_number)
        response_text = ("Thank you, your booking succesfull!")
    else:
        response_text = f"Sorry, the {roomtype} room is not available from {start_date} to {end_date}. Please try again for another dates."


    return jsonify({
        "fulfillmentText": response_text
    })


#==========Mainloop=========

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 6000, debug=True) 