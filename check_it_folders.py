import sqlite3
conn = sqlite3.connect('arsiv.db')
cursor = conn.cursor()
cursor.execute("SELECT id, ad, zorunlu_evraklar FROM klasorler WHERE grup = '4'")
for row in cursor.fetchall():
    print(f"{row[0]} | {row[1]} | {row[2]}")
conn.close()
