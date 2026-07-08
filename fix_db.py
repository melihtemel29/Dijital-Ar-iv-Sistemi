import os
import sqlite3

def fix_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'arsiv.db')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Update Admin name to Melih Temel
    cursor.execute("UPDATE kullanicilar SET ad_soyad = 'Melih Temel' WHERE kullanici_adi = 'admin'")
    
    # 2. Delete the specific folder "869-2"
    cursor.execute("DELETE FROM klasorler WHERE id = '869-2'")
    
    # Optional: Delete related belgeler if any
    try:
        cursor.execute("DELETE FROM evraklar WHERE klasor_id = '869-2'")
    except:
        pass
    
    conn.commit()
    conn.close()
    print("Database updated: Admin name changed and folder 869-2 deleted.")

if __name__ == "__main__":
    fix_db()
