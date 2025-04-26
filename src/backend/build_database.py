import sqlite3
import os
from werkzeug.security import generate_password_hash

# --- Always start fresh: Delete old database if it exists ---
if os.path.exists('reservations.db'):
    os.remove('reservations.db')
    print("Old reservations.db deleted.")

# --- Connect to create a new database ---
conn = sqlite3.connect('reservations.db')
cursor = conn.cursor()

# --- Create Users Table ---
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('renter', 'staff'))
)
''')

# --- Create Facilities Table ---
cursor.execute('''
CREATE TABLE IF NOT EXISTS Facilities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    capacity INTEGER NOT NULL,
    amenities TEXT
)
''')

# --- Create Reservations Table ---
cursor.execute('''
CREATE TABLE IF NOT EXISTS Reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    facility_id INTEGER,
    event_type TEXT,
    attendees INTEGER,
    date TEXT,
    time_start TEXT,
    time_end TEXT,
    status TEXT CHECK(status IN ('pending', 'approved', 'rejected')) DEFAULT 'pending',
    analysis TEXT,
    documents TEXT,
    payment_status TEXT CHECK(payment_status IN ('unpaid', 'paid')) DEFAULT 'unpaid',
    invoice_link TEXT,
    FOREIGN KEY(user_id) REFERENCES Users(id),
    FOREIGN KEY(facility_id) REFERENCES Facilities(id)
)
''')

# --- Insert Sample Users ---
sample_users = [
   ('John Doe', generate_password_hash('password123'), 'renter'),
   ('Jane Staff', generate_password_hash('adminpass456'), 'staff')
]

cursor.executemany('''
INSERT INTO Users (name, password_hash, role)
VALUES (?, ?, ?)
''', sample_users)

# --- Insert Sample Facilities ---
sample_facilities = [
    ('Main Gym', '123 Main St', 100, 'basketball court, bleachers, scoreboard'),
    ('Auditorium', '456 School Ave', 300, 'stage, sound system, projector')
]

cursor.executemany('''
INSERT INTO Facilities (name, location, capacity, amenities)
VALUES (?, ?, ?, ?)
''', sample_facilities)
