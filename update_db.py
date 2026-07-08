import sqlite3

def upgrade_db():
    conn = sqlite3.connect('arsiv.db')
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE malzemeler ADD COLUMN birim_tipi TEXT DEFAULT 'Adet'")
        print("Column birim_tipi added successfully.")
    except sqlite3.OperationalError as e:
        print("Column might already exist or error:", e)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    upgrade_db()
