import os

routes_code = """
# --- STOK VE SARF MALZEME MODÜLÜ ---
@app.route('/stok')
@login_required
def stok_sayfasi():
    conn = get_db_connection()
    malzemeler = conn.execute('SELECT * FROM malzemeler ORDER BY malzeme_adi').fetchall()
    birimler = conn.execute('SELECT * FROM birimler ORDER BY birim_adi').fetchall()
    
    gecmis = conn.execute('''
        SELECT h.id, m.malzeme_adi, b.birim_adi, h.adet, h.tarih, m.birim_tipi 
        FROM harcamalar h
        JOIN malzemeler m ON h.malzeme_id = m.id
        JOIN birimler b ON h.birim_id = b.id
        ORDER BY h.tarih DESC LIMIT 20
    ''').fetchall()
    conn.close()
    
    return render_template('stok.html', malzemeler=malzemeler, birimler=birimler, gecmis=gecmis)

@app.route('/stok_ekle', methods=['POST'])
@login_required
def stok_ekle():
    if session.get('rol') != 'admin':
        flash("Sadece yetkililer stok ekleyebilir.")
        return redirect(url_for('stok_sayfasi'))
        
    malzeme_adi = request.form.get('malzeme_adi')
    birim_tipi = request.form.get('birim_tipi', 'Adet')
    stok_adedi = int(request.form.get('stok_adedi', 0))
    
    conn = get_db_connection()
    mevcut = conn.execute('SELECT id, stok_adedi FROM malzemeler WHERE malzeme_adi = ?', (malzeme_adi,)).fetchone()
    
    if mevcut:
        yeni_stok = mevcut['stok_adedi'] + stok_adedi
        conn.execute('UPDATE malzemeler SET stok_adedi = ?, birim_tipi = ? WHERE id = ?', (yeni_stok, birim_tipi, mevcut['id']))
        flash(f"{malzeme_adi} stoğu güncellendi. Yeni stok: {yeni_stok} {birim_tipi}")
    else:
        conn.execute('INSERT INTO malzemeler (malzeme_adi, stok_adedi, birim_tipi) VALUES (?, ?, ?)', (malzeme_adi, stok_adedi, birim_tipi))
        flash(f"Yeni malzeme eklendi: {malzeme_adi}")
        
    conn.commit()
    conn.close()
    return redirect(url_for('stok_sayfasi'))

@app.route('/stok_harca', methods=['POST'])
@login_required
def stok_harca():
    malzeme_id = request.form.get('malzeme_id')
    birim_id = request.form.get('birim_id')
    adet = int(request.form.get('adet', 0))
    
    if adet <= 0:
        flash("Geçersiz miktar!")
        return redirect(url_for('stok_sayfasi'))
        
    conn = get_db_connection()
    malzeme = conn.execute('SELECT stok_adedi, malzeme_adi, birim_tipi FROM malzemeler WHERE id = ?', (malzeme_id,)).fetchone()
    
    if not malzeme:
        flash("Malzeme bulunamadı.")
    elif malzeme['stok_adedi'] < adet:
        flash(f"Yetersiz stok! Sadece {malzeme['stok_adedi']} {malzeme['birim_tipi']} {malzeme['malzeme_adi']} kaldı.")
    else:
        yeni_stok = malzeme['stok_adedi'] - adet
        conn.execute('UPDATE malzemeler SET stok_adedi = ? WHERE id = ?', (yeni_stok, malzeme_id))
        conn.execute('INSERT INTO harcamalar (malzeme_id, birim_id, adet) VALUES (?, ?, ?)', (malzeme_id, birim_id, adet))
        conn.commit()
        flash(f"{adet} {malzeme['birim_tipi']} {malzeme['malzeme_adi']} çıkışı yapıldı.")
        
    conn.close()
    return redirect(url_for('stok_sayfasi'))

@app.route('/api/stok-grafik')
@login_required
def api_stok_grafik():
    conn = get_db_connection()
    veri = conn.execute('''
        SELECT m.malzeme_adi, SUM(h.adet) as toplam
        FROM harcamalar h
        JOIN malzemeler m ON h.malzeme_id = m.id
        GROUP BY h.malzeme_id
        ORDER BY toplam DESC LIMIT 5
    ''').fetchall()
    conn.close()
    
    labels = [row['malzeme_adi'] for row in veri]
    data = [row['toplam'] for row in veri]
    
    from flask import jsonify
    return jsonify({'labels': labels, 'data': data})

"""

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

if '/stok' not in content:
    content = content.replace("if __name__ == '__main__':", routes_code + "\nif __name__ == '__main__':")
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Routes injected.")
else:
    print("Routes already exist.")
