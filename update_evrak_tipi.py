with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_str = "conn.execute('INSERT INTO evraklar (klasor_id, evrak_tipi, dosya_adi) VALUES (?, ?, ?)', (ana_kod, baslik, filename))"
new_str = """evrak_gorunum_ismi = f"{baslik} ({ana_kod} - {kategori_adi})"
    conn.execute('INSERT INTO evraklar (klasor_id, evrak_tipi, dosya_adi) VALUES (?, ?, ?)', (ana_kod, evrak_gorunum_ismi, filename))"""

new_content = content.replace(old_str, new_str)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Updated app.py successfully.")
