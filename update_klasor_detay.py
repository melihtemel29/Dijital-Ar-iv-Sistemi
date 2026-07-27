import re

# Update app.py for klasor_detay
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_klasor = """def klasor_detay(klasor_id):
    klasorler = get_authorized_folders(session['kullanici_id'], session['rol'])
    
    secili_klasor = None
    for k in klasorler:
        if k['id'] == klasor_id:
            secili_klasor = k
            break
            
    if not secili_klasor:
        flash("Bu klasöre erişim yetkiniz yok veya klasör bulunamadı.")
        return redirect(url_for('ana_sayfa'))
        
    conn = get_db_connection()
    yuklenenler_db = conn.execute('SELECT id, evrak_tipi, dosya_adi FROM evraklar WHERE klasor_id = ?', (klasor_id,)).fetchall()
    conn.close()
    
    yuklenenler = [(row['id'], row['evrak_tipi'], row['dosya_adi']) for row in yuklenenler_db]
    
    return render_template('index.html', klasorler=klasorler, secili_klasor=secili_klasor, yuklenenler=yuklenenler)"""

new_klasor = """def klasor_detay(klasor_id):
    aktif_donem = session.get('aktif_donem', '2026')
    klasorler = get_authorized_folders(session['kullanici_id'], session['rol'], aktif_donem)
    
    secili_klasor = None
    for k in klasorler:
        if k['id'] == klasor_id:
            secili_klasor = k
            break
            
    if not secili_klasor:
        flash("Bu klasöre erişim yetkiniz yok veya klasör bulunamadı.")
        return redirect(url_for('ana_sayfa'))
        
    conn = get_db_connection()
    evraklar = conn.execute('''
        SELECT e.*, k.ad_soyad 
        FROM evraklar e 
        LEFT JOIN kullanicilar k ON e.kullanici_id = k.id 
        WHERE e.klasor_id = ? AND e.ait_oldugu_yil = ?
        ORDER BY e.yukleme_tarihi DESC
    ''', (klasor_id, aktif_donem)).fetchall()
    conn.close()
    
    return render_template('index.html', klasorler=klasorler, secili_klasor=secili_klasor, evraklar=evraklar, aktif_donem=aktif_donem)"""

content = content.replace(old_klasor, new_klasor)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)


# Update index.html
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Replace yuklenenler loop
html_content = html_content.replace('{% if yuklenenler %}', '{% if evraklar %}')
html_content = html_content.replace('{% for eid, tip, ad in yuklenenler %}', '{% for e in evraklar %}')
html_content = html_content.replace('{{ tip }}', '{{ e.evrak_tipi }}')
html_content = html_content.replace('{{ ad }}', '{{ e.dosya_adi }}')
html_content = html_content.replace('/indir/{{ ad }}', '/indir/{{ e.dosya_adi }}')
html_content = html_content.replace('/sil/{{ secili_klasor.id }}/{{ eid }}', '/sil/{{ secili_klasor.id }}/{{ e.id }}')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Updated klasor_detay logic")
