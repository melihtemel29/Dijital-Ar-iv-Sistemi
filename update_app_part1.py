import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add set_donem route
if "@app.route('/set_donem/<yil>')" not in content:
    set_donem_route = """
@app.route('/set_donem/<yil>')
@login_required
def set_donem(yil):
    session['aktif_donem'] = yil
    return redirect(request.referrer or url_for('dashboard'))

"""
    # Insert it before def dashboard()
    content = content.replace('@app.route(\'/dashboard\')', set_donem_route + '@app.route(\'/dashboard\')')


# 2. Update get_authorized_folders
old_get_auth = """def get_authorized_folders(user_id, rol):
    conn = get_db_connection()
    if rol == 'admin':
        klasorler = conn.execute('SELECT * FROM klasorler WHERE is_deleted = 0 OR is_deleted IS NULL').fetchall()
    else:
        klasorler = conn.execute('''
            SELECT k.* FROM klasorler k
            JOIN klasor_yetkileri ky ON k.id = ky.klasor_id
            WHERE ky.kullanici_id = ? AND (k.is_deleted = 0 OR k.is_deleted IS NULL)
        ''', (user_id,)).fetchall()
        
    sonuc = []
    for k in klasorler:
        k_dict = dict(k)
        zorunlular = [z.strip() for z in k_dict['zorunlu_evraklar'].split(',')] if k_dict['zorunlu_evraklar'] else []
        k_dict['zorunlular'] = zorunlular
        
        yuklenenler = conn.execute('SELECT evrak_tipi FROM evraklar WHERE klasor_id = ?', (k_dict['id'],)).fetchall()"""

new_get_auth = """def get_authorized_folders(user_id, rol, aktif_donem=None):
    if not aktif_donem:
        from flask import session
        aktif_donem = session.get('aktif_donem', '2026')
        
    conn = get_db_connection()
    if rol == 'admin':
        klasorler = conn.execute('SELECT * FROM klasorler WHERE is_deleted = 0 OR is_deleted IS NULL').fetchall()
    else:
        klasorler = conn.execute('''
            SELECT k.* FROM klasorler k
            JOIN klasor_yetkileri ky ON k.id = ky.klasor_id
            WHERE ky.kullanici_id = ? AND (k.is_deleted = 0 OR k.is_deleted IS NULL)
        ''', (user_id,)).fetchall()
        
    sonuc = []
    for k in klasorler:
        k_dict = dict(k)
        zorunlular = [z.strip() for z in k_dict['zorunlu_evraklar'].split(',')] if k_dict['zorunlu_evraklar'] else []
        k_dict['zorunlular'] = zorunlular
        
        yuklenenler = conn.execute('SELECT evrak_tipi FROM evraklar WHERE klasor_id = ? AND ait_oldugu_yil = ?', (k_dict['id'], aktif_donem)).fetchall()"""

content = content.replace(old_get_auth, new_get_auth)

# 3. Update dashboard to get aktif_donem and pass it to get_authorized_folders
old_dash = """def dashboard():
    klasorler = get_authorized_folders(session['kullanici_id'], session['rol'])
    toplam_klasor = len(klasorler)
    eksik_sayisi = sum(1 for k in klasorler if k['durum'] == 'Eksik Evrak')
    return render_template('dashboard.html', toplam_klasor=toplam_klasor, eksik_sayisi=eksik_sayisi, aktif_donem="2026")"""

new_dash = """def dashboard():
    aktif_donem = session.get('aktif_donem', '2026')
    klasorler = get_authorized_folders(session['kullanici_id'], session['rol'], aktif_donem)
    toplam_klasor = len(klasorler)
    eksik_sayisi = sum(1 for k in klasorler if k['durum'] == 'Eksik Evrak')
    return render_template('dashboard.html', toplam_klasor=toplam_klasor, eksik_sayisi=eksik_sayisi, aktif_donem=aktif_donem)"""

content = content.replace(old_dash, new_dash)

# 4. Update ana_sayfa
old_ana = """def ana_sayfa():
    klasorler = get_authorized_folders(session['kullanici_id'], session['rol'])
    return render_template('index.html', klasorler=klasorler, secili_klasor=None)"""

new_ana = """def ana_sayfa():
    aktif_donem = session.get('aktif_donem', '2026')
    klasorler = get_authorized_folders(session['kullanici_id'], session['rol'], aktif_donem)
    return render_template('index.html', klasorler=klasorler, secili_klasor=None, aktif_donem=aktif_donem)"""

content = content.replace(old_ana, new_ana)

# 5. Update klasor_detay
old_klasor = """def klasor_detay(klasor_id):
    klasorler = get_authorized_folders(session['kullanici_id'], session['rol'])
    secili_klasor = next((k for k in klasorler if k['id'] == klasor_id), None)
    if not secili_klasor:
        return redirect(url_for('ana_sayfa'))
    
    conn = get_db_connection()
    evraklar = conn.execute('''
        SELECT e.*, k.ad_soyad 
        FROM evraklar e 
        LEFT JOIN kullanicilar k ON e.kullanici_id = k.id 
        WHERE e.klasor_id = ?
        ORDER BY e.yukleme_tarihi DESC
    ''', (klasor_id,)).fetchall()
    conn.close()
    
    return render_template('index.html', klasorler=klasorler, secili_klasor=secili_klasor, evraklar=evraklar)"""

new_klasor = """def klasor_detay(klasor_id):
    aktif_donem = session.get('aktif_donem', '2026')
    klasorler = get_authorized_folders(session['kullanici_id'], session['rol'], aktif_donem)
    secili_klasor = next((k for k in klasorler if k['id'] == klasor_id), None)
    if not secili_klasor:
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

print("First batch of app.py changes done.")
