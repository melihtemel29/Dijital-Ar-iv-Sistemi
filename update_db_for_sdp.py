import sqlite3

def update_db():
    conn = sqlite3.connect('arsiv.db')
    cursor = conn.cursor()

    # 1. Add departman column to kullanicilar if it doesn't exist
    try:
        cursor.execute("ALTER TABLE kullanicilar ADD COLUMN departman TEXT DEFAULT 'Genel'")
        print("Added 'departman' column to kullanicilar.")
    except sqlite3.OperationalError as e:
        if 'duplicate column name' in str(e).lower():
            print("'departman' column already exists.")
        else:
            print(f"Error adding column: {e}")

    # 2. Create sdp_evraklar table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS sdp_evraklar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kullanici_id INTEGER,
        departman TEXT,
        ana_sdp_kodu TEXT,
        alt_sdp_kodu TEXT,
        baslik TEXT,
        etiketler TEXT,
        aciklama TEXT,
        dosya_adi TEXT,
        yukleme_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(kullanici_id) REFERENCES kullanicilar(id)
    )
    """
    cursor.execute(create_table_sql)
    print("Created 'sdp_evraklar' table.")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    update_db()
