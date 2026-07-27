import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_sil = """@app.route('/sdp/sil/<int:evrak_id>')
@login_required
def sdp_sil(evrak_id):
    conn = get_db_connection()
    evrak = conn.execute('SELECT * FROM sdp_evraklar WHERE id = ?', (evrak_id,)).fetchone()
    
    kategori = None
    alt_kategori = None
    
    if evrak:
        ana_kod = evrak['ana_sdp_kodu']
        if ana_kod:
            alt_kategori = ana_kod
            kategori = ana_kod.split('.')[0] if '.' in ana_kod else ana_kod

        if session.get('rol') == 'admin' or session.get('kullanici_id') == evrak['kullanici_id']:
            import os
            dosya_yolu = os.path.join(app.config['UPLOAD_FOLDER'], evrak['dosya_adi'])
            if os.path.exists(dosya_yolu):
                try:
                    os.remove(dosya_yolu)
                except:
                    pass
            conn.execute('DELETE FROM sdp_evraklar WHERE id = ?', (evrak_id,))
            # Also delete from evraklar if exists
            conn.execute('DELETE FROM evraklar WHERE dosya_adi = ?', (evrak['dosya_adi'],))
            conn.commit()
            flash("Evrak başarıyla silindi.")
        else:
            flash("Yetkiniz yok.")
    conn.close()
    
    if kategori and alt_kategori:
        return redirect(url_for('sdp_arsiv', kategori=kategori, alt_kategori=alt_kategori))
    return redirect(url_for('sdp_arsiv'))"""

# We'll just replace the whole route
pattern = re.compile(r'@app\.route\(\'/sdp/sil/<int:evrak_id>\'\)\s*@login_required\s*def sdp_sil\(evrak_id\):.*?return redirect\(url_for\(\'sdp_arsiv\'\)\)', re.DOTALL)
content = pattern.sub(new_sil, content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('app.py sdp_sil updated')
