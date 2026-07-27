import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix evrak_yukle
old_evrak_yukle = r"""    dosya = request\.files\['dosya'\]
    evrak_tipi = request\.form\.get\('evrak_tipi'\)
    
    if dosya\.filename == '':
        flash\("Dosya seilmedi\."\)
        return redirect\(url_for\('klasor_detay', klasor_id=klasor_id\)\)
        
    dosya_adi = dosya\.filename
    dosya\.save\(os\.path\.join\(app\.config\['UPLOAD_FOLDER'\], dosya_adi\)\)
    
    conn = get_db_connection\(\)
    conn\.execute\('INSERT INTO evraklar \(klasor_id, evrak_tipi, dosya_adi\) VALUES \(\?, \?, \?\)', \(klasor_id, evrak_tipi, dosya_adi\)\)"""

# In case encoding failed, I'll use a safer regex:
evrak_yukle_pattern = re.compile(r"(def evrak_yukle\(klasor_id\):.*?evrak_tipi = request\.form\.get\('evrak_tipi'\))(.*?)(conn\.execute\('INSERT INTO evraklar \(klasor_id, evrak_tipi, dosya_adi\) VALUES \(\?, \?, \?\)', \(klasor_id, evrak_tipi, dosya_adi\)\))", re.DOTALL)
new_evrak_yukle = r"\1\n    ait_oldugu_yil = request.form.get('ait_oldugu_yil', session.get('aktif_donem', '2026'))\2conn.execute('INSERT INTO evraklar (klasor_id, evrak_tipi, dosya_adi, ait_oldugu_yil) VALUES (?, ?, ?, ?)', (klasor_id, evrak_tipi, dosya_adi, ait_oldugu_yil))"
content = evrak_yukle_pattern.sub(new_evrak_yukle, content)

# Fix sdp_yukle
sdp_yukle_pattern = re.compile(r"INSERT INTO sdp_evraklar \(kullanici_id, departman, ana_sdp_kodu, alt_sdp_kodu, baslik, etiketler, aciklama, dosya_adi, ait_oldugu_yil\)\s*VALUES \(\?, \?, \?, \?, \?, \?, \?, \?\), \?\)", re.DOTALL)
new_sdp_yukle = r"INSERT INTO sdp_evraklar (kullanici_id, departman, ana_sdp_kodu, alt_sdp_kodu, baslik, etiketler, aciklama, dosya_adi, ait_oldugu_yil)\n        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
content = sdp_yukle_pattern.sub(new_sdp_yukle, content)

# Also sdp_yukle has a second insert into evraklar!
sdp_evraklar_insert_pattern = re.compile(r"conn\.execute\('INSERT INTO evraklar \(klasor_id, evrak_tipi, dosya_adi\) VALUES \(\?, \?, \?\)', \(ana_kod, evrak_gorunum_ismi, filename\)\)")
new_sdp_evraklar_insert = r"conn.execute('INSERT INTO evraklar (klasor_id, evrak_tipi, dosya_adi, ait_oldugu_yil) VALUES (?, ?, ?, ?)', (ana_kod, evrak_gorunum_ismi, filename, ait_oldugu_yil))"
content = sdp_evraklar_insert_pattern.sub(new_sdp_evraklar_insert, content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("File upload functions fixed")
