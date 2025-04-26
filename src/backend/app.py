from flask import Flask, request, jsonify
import requests  # For ChatGPT API calls (OpenAI)
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

# ---- Initialize SQLite Database ----
def init_db():
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    # Create reservations table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            attendees INTEGER NOT NULL,
            facility TEXT NOT NULL,
            analysis TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Call this at startup
init_db()

# ---- Home Route ----
@app.route('/')
def home():
    return 'Facility Rental Portal API is running!'

# ---- Reservation Route ----
@app.route('/reserve', methods=['POST'])
def reserve():
    print(f"Received reservation: {event_type}, {attendees} attendees at {facility}")
    data = request.json  # Expecting JSON data from frontend
    event_type = data.get('event_type')
    attendees = data.get('attendees')
    facility = data.get('facility')

# ---- AI Call (ChatGPT) ----
    analysis = analyze_reservation(event_type, attendees, facility)

# ---- Insert into SQLite ----
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO reservations (event_type, attendees, facility, analysis)
        VALUES (?, ?, ?, ?)
    ''', (event_type, attendees, facility, analysis))
    conn.commit()
    conn.close()

    return jsonify({
        'message': 'Reservation received and stored!',
        'analysis': analysis
    })

# ---- AI Analysis Function ----
def analyze_reservation(event_type, attendees, facility):
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }

    prompt = f"""
    Event Type: {event_type}
    Attendees: {attendees}
    Facility: {facility}

    What staffing (custodians, security) is needed for this event? Are there any documents (insurance, permits) typically required?
    """

    # Call OpenAI API (ChatGPT)
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers=headers,
        json={
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 150
        }
    )

    if response.status_code != 200:
        return f"Error: {response.status_code} - {response.text}"

    result = response.json()
    answer = result['choices'][0]['message']['content']
    return answer

# ---- Run the Flask app ----
if __name__ == '__main__':
    app.run(debug=True)
