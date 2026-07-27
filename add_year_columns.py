import sqlite3
import os
import datetime

BASE_DIR = os.path.dirname(os.path.abspath('app.py'))
db_path = os.path.join(BASE_DIR, 'arsiv.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def add_column_if_not_exists(table, column, type_def):
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [info[1] for info in cursor.fetchall()]
    if column not in columns:
        print(f"Adding column {column} to {table}...")
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {type_def}")

add_column_if_not_exists('evraklar', 'ait_oldugu_yil', 'TEXT DEFAULT "2026"')
add_column_if_not_exists('sdp_evraklar', 'ait_oldugu_yil', 'TEXT DEFAULT "2026"')

# Migrate old records based on their upload date, if ait_oldugu_yil is "2026" or null
print("Migrating old records...")
for table in ['evraklar', 'sdp_evraklar']:
    cursor.execute(f"SELECT id, yukleme_tarihi FROM {table}")
    rows = cursor.fetchall()
    for row in rows:
        record_id, yukleme_tarihi = row
        # yukleme_tarihi is usually YYYY-MM-DD HH:MM:SS
        if yukleme_tarihi:
            year = yukleme_tarihi[:4]
            cursor.execute(f"UPDATE {table} SET ait_oldugu_yil = ? WHERE id = ?", (year, record_id))

conn.commit()
conn.close()

print("Database updated successfully.")
