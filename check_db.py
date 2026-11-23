import sqlite3
import os

db_path = os.path.join(
    os.path.dirname(__file__),
    "database",
    "cybershield.db"
)

print("Database path:", db_path)
print("Database exists:", os.path.exists(db_path))

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Tables:", cursor.fetchall())

cursor.execute("SELECT * FROM quiz_results")
rows = cursor.fetchall()

print("\nSaved quiz results:")
for row in rows:
    print(row)

print("\nTotal records:", len(rows))

connection.close()