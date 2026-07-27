import sqlite3
import os

def backup_and_clear():
    db_path = os.path.join(os.path.dirname(__file__), 'arsiv.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create backup tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS klasorler_yedek (
            id TEXT PRIMARY KEY,
            ad TEXT NOT NULL,
            grup TEXT NOT NULL,
            zorunlu_evraklar TEXT,
            bitis_tarihi_var_mi BOOLEAN NOT NULL DEFAULT 0
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS klasor_yetkileri_yedek (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici_id INTEGER,
            klasor_id TEXT
        )
    ''')

    # Copy old non-SDP folders to yedek
    c.execute("INSERT OR IGNORE INTO klasorler_yedek SELECT * FROM klasorler WHERE grup != 'SDP Arşivi' OR grup IS NULL")
    
    # Copy permissions for those folders to yedek
    c.execute('''
        INSERT OR IGNORE INTO klasor_yetkileri_yedek (kullanici_id, klasor_id)
        SELECT ky.kullanici_id, ky.klasor_id FROM klasor_yetkileri ky
        JOIN klasorler k ON ky.klasor_id = k.id
        WHERE k.grup != 'SDP Arşivi' OR k.grup IS NULL
    ''')

    # Delete them from active tables
    c.execute("DELETE FROM klasor_yetkileri WHERE klasor_id IN (SELECT id FROM klasorler WHERE grup != 'SDP Arşivi' OR grup IS NULL)")
    c.execute("DELETE FROM klasorler WHERE grup != 'SDP Arşivi' OR grup IS NULL")

    # Keep evraklar intact just in case, but they won't show up if the folder is gone.
    # We could also delete them from evraklar, but let's just leave them as orphans for now, 
    # or better, let's not delete files from disk.

    conn.commit()
    conn.close()
    print("Backup and clear completed successfully.")

if __name__ == '__main__':
    backup_and_clear()
