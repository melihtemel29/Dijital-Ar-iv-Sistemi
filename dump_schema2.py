import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath('app.py'))
conn = sqlite3.connect(os.path.join(BASE_DIR, 'arsiv.db'))
for row in conn.execute("SELECT sql FROM sqlite_master WHERE type='table'").fetchall():
    if row[0]: print(row[0])
