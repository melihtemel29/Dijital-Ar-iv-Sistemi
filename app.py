import os
import sqlite3
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.secret_key = 'cok_gizli_anahtar_arsiv'
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def get_db_connection():
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'arsiv.db'))
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
            return redirect(url_for('dashboard'))
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
            session['departman'] = user['departman']
            return redirect(url_for('dashboard'))
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
def dashboard():
    klasorler = get_authorized_folders(session['kullanici_id'], session['rol'])
    toplam_klasor = len(klasorler)
    return render_template('dashboard.html', toplam_klasor=toplam_klasor, aktif_donem="2026")

@app.route('/klasorler')
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
    departman = request.form.get('departman', 'Genel')
    
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO kullanicilar (ad_soyad, kullanici_adi, sifre, rol, departman) VALUES (?, ?, ?, ?, ?)', (ad_soyad, kullanici_adi, sifre, rol, departman))
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


# --- STOK VE SARF MALZEME MODÜLÜ ---
@app.route('/stok')
@login_required
def stok_sayfasi():
    conn = get_db_connection()
    malzemeler = conn.execute('SELECT * FROM malzemeler ORDER BY malzeme_adi').fetchall()
    birimler = conn.execute('SELECT * FROM birimler ORDER BY birim_adi').fetchall()
    
    gecmis = conn.execute('''
        SELECT h.id, m.malzeme_adi, b.birim_adi, h.adet, h.tarih, m.birim_tipi, m.stok_adedi 
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
        SELECT m.malzeme_adi, m.stok_adedi, SUM(h.adet) as toplam
        FROM harcamalar h
        JOIN malzemeler m ON h.malzeme_id = m.id
        GROUP BY h.malzeme_id
        ORDER BY toplam DESC LIMIT 5
    ''').fetchall()
    conn.close()
    
    labels = [row['malzeme_adi'] for row in veri]
    tuketilen = [row['toplam'] for row in veri]
    kalan = [row['stok_adedi'] for row in veri]
    
    from flask import jsonify
    return jsonify({'labels': labels, 'tuketilen': tuketilen, 'kalan': kalan})


if __name__ == '__main__':
    # host='0.0.0.0' ayarı, yerel ağdaki herkesin bağlanmasını sağlar
    app.run(debug=True, host='0.0.0.0', port=5000)


# --- SDP (Standart Dosya Planı) Modülü ---

SDP_KODLARI = {
    "300-399": {
        "name": "Akademik ve Eğitim Birimleri",
        "departman_adi": "Öğrenci İşleri Daire Başkanlığı",
        "codes": {
            "300": "Eğitim ve Öğretim İşleri (Genel)",
            "301": "Öğrenci Kontenjanları ve Kabul İşlemleri",
            "302": "Öğrenci Kayıt İşleri ve Dosyaları",
            "304": "Sınav ve Değerlendirme İşlemleri",
            "308": "Mezuniyet ve Diploma İşlemleri",
            "310": "Yatay/Dikey Geçiş İşlemleri",
            "320": "Burs ve Sosyal Yardım İşlemleri",
            "340": "Ders Programları ve Müfredat İşlemleri"
        }
    },
    "900-929": {
        "name": "Personel İşleri",
        "departman_adi": "Personel Daire Başkanlığı",
        "codes": {
            "900": "Personel İşleri (Genel)",
            "901": "Kadro İşlemleri",
            "902": "Atama ve Görevlendirme İşleri",
            "903": "Personel Özlük İşleri",
            "907": "Disiplin ve Cezai İşlemler",
            "915": "Sendikal Faaliyetler",
            "918": "Emeklilik İşlemleri"
        }
    },
    "840-869": {
        "name": "Mali İşler",
        "departman_adi": "İdari ve Mali İşler Daire Başkanlığı",
        "codes": {
            "841": "Bütçe Hazırlama ve Uygulama",
            "843": "Ödenek İşlemleri",
            "851": "Muhasebe İşlemleri",
            "855": "Ödeme İşlemleri",
            "869": "Taşınır Mal İşlemleri"
        }
    },
    "930-949": {
        "name": "Satın Alma ve İhale",
        "departman_adi": "İdari ve Mali İşler Daire Başkanlığı",
        "codes": {
            "930": "Satın Alma ve İhale İşleri (Genel)",
            "934": "İhale İşlemleri",
            "942": "Piyasa Fiyat Araştırması",
            "944": "Doğrudan Temin İşlemleri"
        }
    },
    "700-719": {
        "name": "Bilgi İşlem",
        "departman_adi": "Bilgi İşlem Daire Başkanlığı",
        "codes": {
            "700": "Bilgi İşlem İşleri (Genel)",
            "702": "Yazılım Geliştirme ve Proje İşlemleri",
            "704": "Veri Tabanı ve Sunucu Yönetimi",
            "708": "Donanım, Altyapı ve Ağ Yönetimi",
            "710": "Bilgi ve Siber Güvenlik İşlemleri",
            "713": "Teknik Servis ve Bakım Onarım İşlemleri"
        }
    },
    "400-599": {
        "name": "Sağlık, Kültür ve Spor",
        "departman_adi": "Sağlık, Kültür ve Spor Daire Başkanlığı",
        "codes": {
            "410": "Kültürel Faaliyetler",
            "420": "Spor Faaliyetleri",
            "430": "Beslenme ve Yemek Hizmetleri",
            "440": "Barınma Hizmetleri",
            "450": "Sağlık Hizmetleri"
        }
    },
    "620-639": {
        "name": "Kütüphane",
        "departman_adi": "Kütüphane ve Dokümantasyon Daire Başkanlığı",
        "codes": {
            "622": "Kitap, Süreli Yayın ve Materyal Alımı",
            "624": "Kataloglama ve Sınıflandırma İşlemleri",
            "626": "Kütüphane Kullanım ve Ödünç Verme İşleri",
            "632": "Elektronik Veri Tabanı Abonelikleri"
        }
    },
    "600-619": {
        "name": "Strateji ve Planlama",
        "departman_adi": "Strateji Geliştirme Daire Başkanlığı",
        "codes": {
            "601": "Stratejik Planlama İşlemleri",
            "602": "Performans Programı ve Faaliyet Raporları",
            "610": "İç Kontrol Sistemi Geliştirme Çalışmaları",
            "020": "Kurumsal İstatistikler ve Veri Analizleri"
        }
    },
    "750-769": {
        "name": "Yapı İşleri",
        "departman_adi": "Yapı İşleri ve Teknik Daire Başkanlığı",
        "codes": {
            "751": "Etüt-Proje ve Kamulaştırma İşleri",
            "755": "Yapım (İnşaat) İhaleleri ve Dosyaları",
            "757": "Büyük Onarım ve Tadilat İşleri",
            "764": "Enerji, Isıtma ve Tesisat İşleri"
        }
    },
    "640-659": {
        "name": "Hukuk Müşavirliği",
        "departman_adi": "Hukuk Müşavirliği",
        "codes": {
            "641": "Adli ve İdari Davalar",
            "645": "İcra Takipleri",
            "651": "Hukuki Mütalaalar"
        }
    },
    "000-099": {
        "name": "Ortak Kodlar",
        "departman_adi": "Tüm Birimler",
        "codes": {
            "010": "Kurullar ve Komisyonlar",
            "030": "Mevzuat İşleri",
            "040": "Faaliyet Raporları ve Brifingler",
            "050": "Genel Yazışmalar"
        }
    }
}

@app.route('/sdp')
@login_required
def sdp_arsiv():
    user_dept = session.get('departman', 'Genel')
    # Ortak kodlar herkes için görünür, diğerleri sadece ilgili departman için.
    allowed_categories = {}
    
    # Tüm grupları kontrol et
    for group_key, group_val in SDP_KODLARI.items():
        if group_key == "000-099" or group_val["departman_adi"] == user_dept or user_dept == "Sistem Yöneticisi" or user_dept == "Genel":
            allowed_categories[group_key] = group_val
            
    conn = get_db_connection()
    evraklar = conn.execute('''
        SELECT s.*, k.ad_soyad 
        FROM sdp_evraklar s 
        LEFT JOIN kullanicilar k ON s.kullanici_id = k.id 
        ORDER BY s.yukleme_tarihi DESC
    ''').fetchall()
    conn.close()
    
    return render_template('sdp_arsiv.html', categories=allowed_categories, evraklar=evraklar)

from werkzeug.utils import secure_filename
import json

@app.route('/sdp/yukle', methods=['POST'])
@login_required
def sdp_yukle():
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

    # SDP Klasör Senkronizasyonu
    kategori_adi = ""
    for group_key, group_val in SDP_KODLARI.items():
        if ana_kod in group_val['codes']:
            kategori_adi = group_val['codes'][ana_kod]
            break
            
    klasor = conn.execute('SELECT * FROM klasorler WHERE id = ?', (ana_kod,)).fetchone()
    if not klasor:
        conn.execute('INSERT INTO klasorler (id, ad, grup) VALUES (?, ?, ?)', (ana_kod, ana_kod + " - " + kategori_adi, "SDP Arşivi"))
        
    yetki = conn.execute('SELECT * FROM klasor_yetkileri WHERE kullanici_id = ? AND klasor_id = ?', (session['kullanici_id'], ana_kod)).fetchone()
    if not yetki:
        conn.execute('INSERT INTO klasor_yetkileri (kullanici_id, klasor_id) VALUES (?, ?)', (session['kullanici_id'], ana_kod))
        
    evrak_gorunum_ismi = f"{baslik} ({ana_kod} - {kategori_adi})"
    conn.execute('INSERT INTO evraklar (klasor_id, evrak_tipi, dosya_adi) VALUES (?, ?, ?)', (ana_kod, evrak_gorunum_ismi, filename))

    conn.commit()
    conn.close()
    
    flash("Evrak başarıyla SDP sistemine ve Klasörlere eklendi.")
    return redirect(url_for('sdp_arsiv'))

@app.route('/sdp/indir/<path:dosya_adi>')
@login_required
def sdp_indir(dosya_adi):
    return send_from_directory(app.config['UPLOAD_FOLDER'], dosya_adi, as_attachment=True)

@app.route('/sdp/goruntule/<path:dosya_adi>')
@login_required
def sdp_goruntule(dosya_adi):
    return send_from_directory(app.config['UPLOAD_FOLDER'], dosya_adi)

@app.route('/sdp/sil/<int:evrak_id>')
@login_required
def sdp_sil(evrak_id):
    conn = get_db_connection()
    evrak = conn.execute('SELECT * FROM sdp_evraklar WHERE id = ?', (evrak_id,)).fetchone()
    if evrak:
        if session.get('rol') == 'admin' or session.get('kullanici_id') == evrak['kullanici_id']:
            dosya_yolu = os.path.join(app.config['UPLOAD_FOLDER'], evrak['dosya_adi'])
            if os.path.exists(dosya_yolu):
                try:
                    os.remove(dosya_yolu)
                except:
                    pass
            conn.execute('DELETE FROM sdp_evraklar WHERE id = ?', (evrak_id,))
            conn.execute('DELETE FROM evraklar WHERE dosya_adi = ?', (evrak['dosya_adi'],))
            conn.commit()
            flash("Evrak başarıyla silindi.")
        else:
            flash("Bu evrakı silme yetkiniz yok.")
    conn.close()
    return redirect(url_for('sdp_arsiv'))
