import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update yukle
old_yukle = """def yukle():
    if 'dosya' not in request.files:
        flash("Dosya seçilmedi.")
        return redirect(url_for('ana_sayfa'))
        
    dosya = request.files['dosya']
    klasor_id = request.form.get('klasor_id')
    evrak_tipi = request.form.get('evrak_tipi')
    
    if dosya.filename == '':
        flash("Geçerli bir dosya seçin.")
        return redirect(url_for('ana_sayfa'))
        
    if dosya and klasor_id and evrak_tipi:
        from werkzeug.utils import secure_filename
        filename = secure_filename(dosya.filename)
        dosya.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        conn = get_db_connection()
        conn.execute('INSERT INTO evraklar (klasor_id, evrak_tipi, dosya_adi, kullanici_id) VALUES (?, ?, ?, ?)', 
                    (klasor_id, evrak_tipi, filename, session['kullanici_id']))
        conn.commit()
        conn.close()
        flash("Evrak başarıyla yüklendi.")"""

new_yukle = """def yukle():
    if 'dosya' not in request.files:
        flash("Dosya seçilmedi.")
        return redirect(url_for('ana_sayfa'))
        
    dosya = request.files['dosya']
    klasor_id = request.form.get('klasor_id')
    evrak_tipi = request.form.get('evrak_tipi')
    ait_oldugu_yil = request.form.get('ait_oldugu_yil', session.get('aktif_donem', '2026'))
    
    if dosya.filename == '':
        flash("Geçerli bir dosya seçin.")
        return redirect(url_for('ana_sayfa'))
        
    if dosya and klasor_id and evrak_tipi:
        from werkzeug.utils import secure_filename
        filename = secure_filename(dosya.filename)
        dosya.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        conn = get_db_connection()
        conn.execute('INSERT INTO evraklar (klasor_id, evrak_tipi, dosya_adi, kullanici_id, ait_oldugu_yil) VALUES (?, ?, ?, ?, ?)', 
                    (klasor_id, evrak_tipi, filename, session['kullanici_id'], ait_oldugu_yil))
        conn.commit()
        conn.close()
        flash("Evrak başarıyla yüklendi.")"""

content = content.replace(old_yukle, new_yukle)

# 2. Update sdp_arsiv
old_sdp = """def sdp_arsiv():
    user_dept = session.get('departman', 'Genel')
    allowed_categories = {}
    
    for group_key, group_val in SDP_KODLARI.items():
        if group_key == "000-099" or group_val["departman_adi"] == user_dept or user_dept == "Sistem Yöneticisi" or user_dept == "Genel":
            allowed_categories[group_key] = group_val
            
    kategori = request.args.get('kategori')
    alt_kategori = request.args.get('alt_kategori')
    
    conn = get_db_connection()
    if alt_kategori:
        evraklar = conn.execute('''
            SELECT s.*, k.ad_soyad 
            FROM sdp_evraklar s 
            LEFT JOIN kullanicilar k ON s.kullanici_id = k.id 
            WHERE s.ana_sdp_kodu = ?
            ORDER BY s.yukleme_tarihi DESC
        ''', (alt_kategori,)).fetchall()
    else:
        evraklar = []
    conn.close()
    
    # Find the title and subcodes for the selected category
    secili_kategori_data = None
    if kategori:
        for group in allowed_categories.values():
            if kategori in group['codes']:
                secili_kategori_data = group['codes'][kategori]
                break
                
    return render_template('sdp_arsiv.html', 
                           categories=allowed_categories, 
                           evraklar=evraklar, 
                           kategori=kategori, 
                           alt_kategori=alt_kategori,
                           secili_kategori_data=secili_kategori_data)"""

new_sdp = """def sdp_arsiv():
    aktif_donem = session.get('aktif_donem', '2026')
    user_dept = session.get('departman', 'Genel')
    allowed_categories = {}
    
    for group_key, group_val in SDP_KODLARI.items():
        if group_key == "000-099" or group_val["departman_adi"] == user_dept or user_dept == "Sistem Yöneticisi" or user_dept == "Genel":
            allowed_categories[group_key] = group_val
            
    kategori = request.args.get('kategori')
    alt_kategori = request.args.get('alt_kategori')
    
    conn = get_db_connection()
    if alt_kategori:
        evraklar = conn.execute('''
            SELECT s.*, k.ad_soyad 
            FROM sdp_evraklar s 
            LEFT JOIN kullanicilar k ON s.kullanici_id = k.id 
            WHERE s.ana_sdp_kodu = ? AND s.ait_oldugu_yil = ?
            ORDER BY s.yukleme_tarihi DESC
        ''', (alt_kategori, aktif_donem)).fetchall()
    else:
        evraklar = []
    conn.close()
    
    # Find the title and subcodes for the selected category
    secili_kategori_data = None
    if kategori:
        for group in allowed_categories.values():
            if kategori in group['codes']:
                secili_kategori_data = group['codes'][kategori]
                break
                
    return render_template('sdp_arsiv.html', 
                           categories=allowed_categories, 
                           evraklar=evraklar, 
                           kategori=kategori, 
                           alt_kategori=alt_kategori,
                           secili_kategori_data=secili_kategori_data,
                           aktif_donem=aktif_donem)"""

content = content.replace(old_sdp, new_sdp)

# 3. Update sdp_yukle
old_sdp_yukle = """def sdp_yukle():
    if 'dosya' not in request.files:
        flash("Dosya seçilmedi.")
        return redirect(url_for('sdp_arsiv'))
        
    dosya = request.files['dosya']
    ana_kod = request.form.get('ana_sdp_kodu')
    alt_kod = request.form.get('alt_sdp_kodu', '')
    baslik = request.form.get('baslik', '')
    etiketler = request.form.get('etiketler', '')
    aciklama = request.form.get('aciklama', '')
    departman = session.get('departman', 'Genel')
    
    if dosya.filename == '':
        flash("Geçerli bir dosya seçin.")
        return redirect(url_for('sdp_arsiv'))
        
    filename = secure_filename(dosya.filename)
    dosya.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO sdp_evraklar (kullanici_id, departman, ana_sdp_kodu, alt_sdp_kodu, baslik, etiketler, aciklama, dosya_adi)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (session['kullanici_id'], departman, ana_kod, alt_kod, baslik, etiketler, aciklama, filename))
    conn.commit()"""

new_sdp_yukle = """def sdp_yukle():
    if 'dosya' not in request.files:
        flash("Dosya seçilmedi.")
        return redirect(url_for('sdp_arsiv'))
        
    dosya = request.files['dosya']
    ana_kod = request.form.get('ana_sdp_kodu')
    alt_kod = request.form.get('alt_sdp_kodu', '')
    baslik = request.form.get('baslik', '')
    etiketler = request.form.get('etiketler', '')
    aciklama = request.form.get('aciklama', '')
    ait_oldugu_yil = request.form.get('ait_oldugu_yil', session.get('aktif_donem', '2026'))
    departman = session.get('departman', 'Genel')
    
    if dosya.filename == '':
        flash("Geçerli bir dosya seçin.")
        return redirect(url_for('sdp_arsiv'))
        
    filename = secure_filename(dosya.filename)
    dosya.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO sdp_evraklar (kullanici_id, departman, ana_sdp_kodu, alt_sdp_kodu, baslik, etiketler, aciklama, dosya_adi, ait_oldugu_yil)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (session['kullanici_id'], departman, ana_kod, alt_kod, baslik, etiketler, aciklama, filename, ait_oldugu_yil))
    conn.commit()"""

content = content.replace(old_sdp_yukle, new_sdp_yukle)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Second batch of app.py changes done.")
