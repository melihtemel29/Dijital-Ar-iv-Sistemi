import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'arsiv.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()

try:
    c.execute("ALTER TABLE klasorler ADD COLUMN is_deleted BOOLEAN DEFAULT 0")
    print("Column 'is_deleted' added successfully.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("Column 'is_deleted' already exists.")
    else:
        print("Error:", e)

conn.commit()
conn.close()
