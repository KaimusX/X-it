from flask import Flask, request, jsonify
from flask import send_from_directory
from flask_cors import CORS
import requests  # For ChatGPT API calls (OpenAI)
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)

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
    data = request.json  # Expecting JSON data from frontend
    event_type = data.get('event_type')
    attendees = data.get('attendees')
    facility = data.get('facility')

    print(f"Received reservation: {event_type}, {attendees} attendees at {facility}")

    # AI Call (ChatGPT)
    analysis = analyze_reservation(event_type, attendees, facility)

    # Insert into SQLite
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

# ---- Login Route ----
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        return jsonify({'success': False, 'message': 'Missing fields'}), 400

    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, password_hash, role FROM Users WHERE name = ?', (username,))
    user = cursor.fetchone()

    if user:
        user_id, password_hash, user_role = user
        if check_password_hash(password_hash, password):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'})
    else:
        # User does not exist, create it
        password_hash = generate_password_hash(password)
        cursor.execute('INSERT INTO Users (name, password_hash, role) VALUES (?, ?, ?)', (username, password_hash, role))
        conn.commit()
        return jsonify({'success': True, 'message': 'User created'})

# ---- AI Analysis Function ----
# ---- AI Analysis Function (Improved AI Task Bot) ----
def analyze_reservation(event_type, attendees, facility):
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }

    prompt = f"""
    You are an AI Facility Manager Bot.

    Event Details:
    - Event Type: {event_type}
    - Number of Attendees: {attendees}
    - Facility: {facility}

    Task:
    1. Predict how many custodians are needed.
    2. Predict how many security personnel are needed.
    3. List any documents that should be collected (e.g., insurance, permits).
    4. Return your answer in a clean JSON format with keys: "custodians", "security", "documents".

    Example Response:
    {{
        "custodians": 2,
        "security": 1,
        "documents": ["Liability Insurance", "Special Use Permit"]
    }}
    """

    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers=headers,
        json={
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 200
        }
    )

    if response.status_code != 200:
        return f"Error: {response.status_code} - {response.text}"

    result = response.json()
    answer = result['choices'][0]['message']['content']
    return answer

# ---- Serve Frontend Files ----
@app.route('/frontend/<path:path>')
def serve_frontend(path):
    frontend_dir = os.path.join(os.path.dirname(__file__), '../frontend')
    return send_from_directory(frontend_dir, path)

# ---- Run the Flask app ----
if __name__ == '__main__':
    app.run(debug=True)
