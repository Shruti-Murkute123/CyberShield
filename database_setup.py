
import sqlite3
import os

# Database location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "database",
    "cybershield.db"
)

os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

# Connect to SQLite
connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()

# Security assessment results
cursor.execute("""
CREATE TABLE IF NOT EXISTS assessment_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total_score INTEGER NOT NULL,
    maximum_score INTEGER NOT NULL,
    risk_percentage REAL NOT NULL,
    risk_level TEXT NOT NULL,
    created_at TEXT NOT NULL
)
""")

# Phishing quiz results
cursor.execute("""
CREATE TABLE IF NOT EXISTS quiz_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    score INTEGER NOT NULL,
    total INTEGER NOT NULL,
    percentage INTEGER NOT NULL,
    awareness_level TEXT NOT NULL,
    created_at TEXT NOT NULL
)
""")

# Save changes
connection.commit()

# Display database tables
cursor.execute("""
SELECT name FROM sqlite_master
WHERE type = 'table'
AND name NOT LIKE 'sqlite_%'
""")

print("Database created successfully!")
print("Database location:", DATABASE_PATH)
print("Tables:", cursor.fetchall())

connection.close()
