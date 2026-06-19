import os
import sqlite3
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory

app = Flask(__name__)
app.secret_key = 'cok_gizli_anahtar_arsiv'
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def get_db_connection():
    conn = sqlite3.connect('arsiv.db')
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'kullanici_id' not in session:
            flash("Lütfen önce giriş yapın.")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'kullanici_id' not in session or session.get('rol') != 'admin':
            flash("Bu sayfaya erişim yetkiniz yok.")
            return redirect(url_for('ana_sayfa'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM kullanicilar WHERE kullanici_adi = ? AND sifre = ?', (username, password)).fetchone()
        conn.close()
        
        if user:
            session['kullanici_id'] = user['id']
            session['kullanici_adi'] = user['kullanici_adi']
            session['ad_soyad'] = user['ad_soyad']
            session['rol'] = user['rol']
            return redirect(url_for('ana_sayfa'))
        else:
            flash("Hatalı kullanıcı adı veya şifre.")
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

def get_authorized_folders(user_id, rol):
    conn = get_db_connection()
    if rol == 'admin':
        klasorler = conn.execute('SELECT * FROM klasorler').fetchall()
    else:
        klasorler = conn.execute('''
            SELECT k.* FROM klasorler k
            JOIN klasor_yetkileri ky ON k.id = ky.klasor_id
            WHERE ky.kullanici_id = ?
        ''', (user_id,)).fetchall()
        
    sonuc = []
    for k in klasorler:
        k_dict = dict(k)
        zorunlular = [z.strip() for z in k_dict['zorunlu_evraklar'].split(',')] if k_dict['zorunlu_evraklar'] else []
        k_dict['zorunlular'] = zorunlular
        
        yuklenenler = conn.execute('SELECT evrak_tipi FROM evraklar WHERE klasor_id = ?', (k_dict['id'],)).fetchall()
        yuklenen_tipler = [y['evrak_tipi'] for y in yuklenenler]
        
        eksikler = [z for z in zorunlular if z not in yuklenen_tipler]
        k_dict['eksikler'] = eksikler
        k_dict['durum'] = 'Tamamlandı' if len(eksikler) == 0 else 'Eksik Evrak'
        sonuc.append(k_dict)
        
    conn.close()
    return sonuc

@app.route('/')
@login_required
def ana_sayfa():
    klasorler = get_authorized_folders(session['kullanici_id'], session['rol'])
    return render_template('index.html', klasorler=klasorler, secili_klasor=None)

@app.route('/klasor/<path:klasor_id>')
@login_required
def klasor_detay(klasor_id):
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
    
    return render_template('index.html', klasorler=klasorler, secili_klasor=secili_klasor, yuklenenler=yuklenenler)

@app.route('/yukle/<path:klasor_id>', methods=['POST'])
@login_required
def evrak_yukle(klasor_id):
    if 'dosya' not in request.files:
        flash("Dosya seçilmedi.")
        return redirect(url_for('klasor_detay', klasor_id=klasor_id))
        
    dosya = request.files['dosya']
    evrak_tipi = request.form.get('evrak_tipi')
    
    if dosya.filename == '':
        flash("Dosya seçilmedi.")
        return redirect(url_for('klasor_detay', klasor_id=klasor_id))
        
    dosya_adi = dosya.filename
    dosya.save(os.path.join(app.config['UPLOAD_FOLDER'], dosya_adi))
    
    conn = get_db_connection()
    conn.execute('INSERT INTO evraklar (klasor_id, evrak_tipi, dosya_adi) VALUES (?, ?, ?)', (klasor_id, evrak_tipi, dosya_adi))
    conn.commit()
    conn.close()
    
    return redirect(url_for('klasor_detay', klasor_id=klasor_id))

@app.route('/sil/<path:klasor_id>/<int:evrak_id>')
@login_required
def evrak_sil(klasor_id, evrak_id):
    conn = get_db_connection()
    evrak = conn.execute('SELECT dosya_adi FROM evraklar WHERE id = ? AND klasor_id = ?', (evrak_id, klasor_id)).fetchone()
    if evrak:
        dosya_yolu = os.path.join(app.config['UPLOAD_FOLDER'], evrak['dosya_adi'])
        if os.path.exists(dosya_yolu):
            os.remove(dosya_yolu)
        conn.execute('DELETE FROM evraklar WHERE id = ?', (evrak_id,))
        conn.commit()
    conn.close()
    return redirect(url_for('klasor_detay', klasor_id=klasor_id))

@app.route('/indir/<path:dosya_adi>')
@login_required
def evrak_indir(dosya_adi):
    return send_from_directory(app.config['UPLOAD_FOLDER'], dosya_adi)

# --- ADMIN PANELİ ---
@app.route('/admin')
@admin_required
def admin_panel():
    conn = get_db_connection()
    kullanicilar = conn.execute('SELECT * FROM kullanicilar').fetchall()
    klasorler = conn.execute('SELECT id, ad FROM klasorler').fetchall()
    
    yetkiler = {}
    yetkiler_db = conn.execute('SELECT kullanici_id, klasor_id FROM klasor_yetkileri').fetchall()
    for row in yetkiler_db:
        uid = row['kullanici_id']
        if uid not in yetkiler:
            yetkiler[uid] = []
        yetkiler[uid].append(row['klasor_id'])
        
    conn.close()
    return render_template('admin.html', kullanicilar=kullanicilar, klasorler=klasorler, yetkiler=yetkiler)

@app.route('/admin/kullanici_ekle', methods=['POST'])
@admin_required
def kullanici_ekle():
    ad_soyad = request.form.get('ad_soyad')
    kullanici_adi = request.form.get('kullanici_adi')
    sifre = request.form.get('sifre')
    rol = request.form.get('rol')
    
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO kullanicilar (ad_soyad, kullanici_adi, sifre, rol) VALUES (?, ?, ?, ?)', (ad_soyad, kullanici_adi, sifre, rol))
        conn.commit()
    except sqlite3.IntegrityError:
        flash("Bu kullanıcı adı zaten mevcut.")
    conn.close()
    return redirect(url_for('admin_panel'))

@app.route('/admin/kullanici_sil/<int:user_id>')
@admin_required
def kullanici_sil(user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM kullanicilar WHERE id = ?', (user_id,))
    conn.execute('DELETE FROM klasor_yetkileri WHERE kullanici_id = ?', (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel'))

@app.route('/admin/yetki_kaydet', methods=['POST'])
@admin_required
def yetki_kaydet():
    conn = get_db_connection()
    kullanici_id = request.form.get('kullanici_id')
    klasorler = request.form.getlist('klasorler')
    
    conn.execute('DELETE FROM klasor_yetkileri WHERE kullanici_id = ?', (kullanici_id,))
    for kl in klasorler:
        conn.execute('INSERT INTO klasor_yetkileri (kullanici_id, klasor_id) VALUES (?, ?)', (kullanici_id, kl))
        
    conn.commit()
    conn.close()
    flash("Yetkiler güncellendi.")
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)