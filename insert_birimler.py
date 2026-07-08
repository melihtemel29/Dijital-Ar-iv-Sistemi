import sqlite3

units = [
    "Diş Hekimliği Fakültesi",
    "Eczacılık Fakültesi",
    "Edebiyat Fakültesi",
    "Fen Fakültesi",
    "İktisadi ve İdari Bilimler Fakültesi",
    "Mimarlık Fakültesi",
    "Mühendislik Fakültesi",
    "Of Teknoloji Fakültesi",
    "Orman Fakültesi",
    "Sağlık Bilimleri Fakültesi",
    "Sürmene Deniz Bilimleri Fakültesi",
    "Tıp Fakültesi",
    "Adli Bilimler Enstitüsü",
    "Deniz Bilimleri ve Teknolojileri Enstitüsü",
    "Fen Bilimleri Enstitüsü",
    "Karadeniz Araştırmaları Enstitüsü",
    "Sağlık Bilimleri Enstitüsü",
    "Sosyal Bilimler Enstitüsü",
    "Yabancı Diller Yüksekokulu",
    "Araklı Ali Cevat Özyurt Meslek Yüksekokulu",
    "Arsin Meslek Yüksekokulu",
    "Maçka Meslek Yüksekokulu",
    "Sağlık Hizmetleri Meslek Yüksekokulu",
    "Sürmene Abdullah Kanca Meslek Yüksekokulu",
    "Trabzon Meslek Yüksekokulu",
    "Bilgi İşlem Daire Başkanlığı"
]

def import_units():
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'arsiv.db')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get existing units to avoid duplicates
    cursor.execute('SELECT birim_adi FROM birimler')
    existing = [row[0] for row in cursor.fetchall()]
    
    count = 0
    for u in units:
        if u not in existing:
            cursor.execute('INSERT INTO birimler (birim_adi) VALUES (?)', (u,))
            count += 1
            
    conn.commit()
    conn.close()
    print(f"Başarıyla {count} yeni birim veritabanına eklendi!")

if __name__ == "__main__":
    import_units()
