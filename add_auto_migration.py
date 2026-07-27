import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# I will add an auto-migration script block right after `get_db_connection` definition or inside it.
# Actually, it's better to do it once when app.py runs.
# Let's find `def init_db():` if it exists, or just put it at the bottom.
# Is there an init_db?
init_code = """
def auto_migrate_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check evraklar table
    cursor.execute("PRAGMA table_info(evraklar)")
    columns = [info['name'] for info in cursor.fetchall()]
    if 'ait_oldugu_yil' not in columns:
        cursor.execute('ALTER TABLE evraklar ADD COLUMN ait_oldugu_yil TEXT DEFAULT "2026"')
        # Migrate old records
        cursor.execute("SELECT id, yukleme_tarihi FROM evraklar WHERE ait_oldugu_yil IS NULL OR ait_oldugu_yil = '2026'")
        for row in cursor.fetchall():
            if row['yukleme_tarihi']:
                year = str(row['yukleme_tarihi'])[:4]
                conn.execute("UPDATE evraklar SET ait_oldugu_yil = ? WHERE id = ?", (year, row['id']))
    
    # Check sdp_evraklar table
    cursor.execute("PRAGMA table_info(sdp_evraklar)")
    columns = [info['name'] for info in cursor.fetchall()]
    if 'ait_oldugu_yil' not in columns:
        cursor.execute('ALTER TABLE sdp_evraklar ADD COLUMN ait_oldugu_yil TEXT DEFAULT "2026"')
        # Migrate old records
        cursor.execute("SELECT id, yukleme_tarihi FROM sdp_evraklar WHERE ait_oldugu_yil IS NULL OR ait_oldugu_yil = '2026'")
        for row in cursor.fetchall():
            if row['yukleme_tarihi']:
                year = str(row['yukleme_tarihi'])[:4]
                conn.execute("UPDATE sdp_evraklar SET ait_oldugu_yil = ? WHERE id = ?", (year, row['id']))
                
    conn.commit()
    conn.close()

# Run migrations at startup
try:
    auto_migrate_db()
except Exception as e:
    print("Auto migration error:", e)
"""

if "def auto_migrate_db():" not in content:
    # insert it right before if __name__ == '__main__':
    content = content.replace("if __name__ == '__main__':", init_code + "\nif __name__ == '__main__':")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added auto_migrate_db to app.py")
