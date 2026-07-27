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



def get_authorized_folders(user_id, rol, aktif_donem=None):
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

        

        yuklenenler = conn.execute('SELECT evrak_tipi FROM evraklar WHERE klasor_id = ? AND ait_oldugu_yil = ?', (k_dict['id'], aktif_donem)).fetchall()

        yuklenen_tipler = [y['evrak_tipi'] for y in yuklenenler]

        

        eksikler = [z for z in zorunlular if z not in yuklenen_tipler]

        k_dict['eksikler'] = eksikler

        k_dict['durum'] = 'Boş Klasör' if len(yuklenen_tipler) == 0 else ('Tamamlandı' if len(eksikler) == 0 else 'Eksik Evrak')

        sonuc.append(k_dict)

        

    conn.close()

    return sonuc





@app.route('/set_donem/<yil>')
@login_required
def set_donem(yil):
    session['aktif_donem'] = yil
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/')

@login_required

def dashboard():
    aktif_donem = session.get('aktif_donem', '2026')
    klasorler = get_authorized_folders(session['kullanici_id'], session['rol'], aktif_donem)
    toplam_klasor = len(klasorler)
    eksik_sayisi = sum(1 for k in klasorler if k['durum'] == 'Eksik Evrak')
    return render_template('dashboard.html', toplam_klasor=toplam_klasor, eksik_sayisi=eksik_sayisi, aktif_donem=aktif_donem)



@app.route('/klasorler')

@login_required

def ana_sayfa():
    aktif_donem = session.get('aktif_donem', '2026')
    klasorler = get_authorized_folders(session['kullanici_id'], session['rol'], aktif_donem)
    return render_template('index.html', klasorler=klasorler, secili_klasor=None, aktif_donem=aktif_donem)



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






def auto_migrate_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check evraklar table
    cursor.execute("PRAGMA table_info(evraklar)")
    columns = [info['name'] for info in cursor.fetchall()]
    if 'ait_oldugu_yil' not in columns:
        cursor.execute('ALTER TABLE evraklar ADD COLUMN ait_oldugu_yil TEXT DEFAULT "2026"')
        # Migrate old records
        cursor.execute("SELECT id, yukleme_tarihi FROM evraklar WHERE ait_oldugu_yil IS NULL OR ait_oldugu_yil = '2026'")
        for row in cursor.fetchall():
            if row['yukleme_tarihi']:
                year = str(row['yukleme_tarihi'])[:4]
                conn.execute("UPDATE evraklar SET ait_oldugu_yil = ? WHERE id = ?", (year, row['id']))
    
    # Check sdp_evraklar table
    cursor.execute("PRAGMA table_info(sdp_evraklar)")
    columns = [info['name'] for info in cursor.fetchall()]
    if 'ait_oldugu_yil' not in columns:
        cursor.execute('ALTER TABLE sdp_evraklar ADD COLUMN ait_oldugu_yil TEXT DEFAULT "2026"')
        # Migrate old records
        cursor.execute("SELECT id, yukleme_tarihi FROM sdp_evraklar WHERE ait_oldugu_yil IS NULL OR ait_oldugu_yil = '2026'")
        for row in cursor.fetchall():
            if row['yukleme_tarihi']:
                year = str(row['yukleme_tarihi'])[:4]
                conn.execute("UPDATE sdp_evraklar SET ait_oldugu_yil = ? WHERE id = ?", (year, row['id']))
                
    conn.commit()
    conn.close()

# Run migrations at startup
try:
    auto_migrate_db()
except Exception as e:
    print("Auto migration error:", e)

if __name__ == '__main__':

    # host='0.0.0.0' ayarı, yerel ağdaki herkesin bağlanmasını sağlar

    app.run(debug=True, host='0.0.0.0', port=5000)





# --- SDP (Standart Dosya Planı) Modülü ---



SDP_KODLARI = {
    "000-099": {
        "name": "Ortak Kodlar",
        "departman_adi": "Tüm Birimler",
        "codes": {
            "010": {
                "title": "Kurullar ve Komisyonlar",
                "subcodes": {
                    "010.01": "Senato",
                    "010.02": "Yönetim Kurulu",
                    "010.03": "İhtisas Komisyonları",
                    "010.04": "Çalışma Grubu / Komisyonlar"
                }
            },
            "030": {
                "title": "Mevzuat İşleri",
                "subcodes": {
                    "030.01": "Kanun, Kanun Hükmünde Kararname",
                    "030.02": "Tüzük, Yönetmelik",
                    "030.03": "Yönerge, Usul ve Esaslar",
                    "030.04": "Genelge, Talimat, Senato Kararı"
                }
            },
            "040": {
                "title": "Faaliyet Raporları ve Brifingler",
                "subcodes": {
                    "040.01": "Faaliyet Raporları (Birim/Kurum)",
                    "040.02": "Brifingler"
                }
            },
            "050": {
                "title": "Genel Yazışmalar",
                "subcodes": {
                    "050.01": "Genel İşler ve Duyurular",
                    "050.02": "Görüş Talepleri ve Cevapları",
                    "050.06": "Bilgi Edinme İstekleri",
                    "050.99": "Diğer İşler"
                }
            }
        }
    },
    "300-399": {
        "name": "Akademik ve Eğitim Birimleri",
        "departman_adi": "Öğrenci İşleri Daire Başkanlığı",
        "codes": {
            "300": {
                "title": "Eğitim ve Öğretim İşleri (Genel)",
                "subcodes": {
                    "300.01": "Akademik Takvim",
                    "300.02": "Öğretim Yılı Hazırlıkları"
                }
            },
            "301": {
                "title": "Öğrenci Kontenjanları ve Kabul İşlemleri",
                "subcodes": {
                    "301.01": "Kontenjan Belirleme",
                    "301.02": "Özel Yetenek Sınavı ile Kabul",
                    "301.03": "Yabancı Uyruklu Öğrenci Kabulü"
                }
            },
            "302": {
                "title": "Öğrenci Kayıt İşleri ve Dosyaları",
                "subcodes": {
                    "302.01": "Yeni Kayıt İşlemleri",
                    "302.02": "Kayıt Yenileme / Ders Kaydı",
                    "302.03": "Kayıt Dondurma / Silme"
                }
            },
            "304": {
                "title": "Sınav ve Değerlendirme İşlemleri",
                "subcodes": {
                    "304.01": "Sınav Programları",
                    "304.02": "Mazeret / Tek Ders Sınavları",
                    "304.03": "Sınav Sonuçları ve İtirazlar"
                }
            },
            "308": {
                "title": "Mezuniyet ve Diploma İşlemleri",
                "subcodes": {
                    "308.01": "Mezuniyet Kararları / Dereceler",
                    "308.02": "Diploma ve Sertifika Basımı",
                    "308.03": "Diploma Eki ve Geçici Mezuniyet Belgesi"
                }
            },
            "310": {
                "title": "Yatay / Dikey Geçiş İşlemleri",
                "subcodes": {
                    "310.01": "Kurum İçi / Kurumlar Arası Yatay Geçiş",
                    "310.02": "Dikey Geçiş İşlemleri",
                    "310.03": "İntibak ve Muafiyet İşlemleri"
                }
            },
            "320": {
                "title": "Burs ve Sosyal Yardım İşlemleri",
                "subcodes": {
                    "320.01": "YKY / KYK Burs/Kredi İşlemleri",
                    "320.02": "Özel / Kurum Bursları",
                    "320.03": "Yemek, Barınma ve Destek Yardımları"
                }
            },
            "340": {
                "title": "Ders Programları ve Müfredat İşlemleri",
                "subcodes": {
                    "340.01": "Müfredat Düzenleme ve Güncelleme",
                    "340.02": "Haftalık Ders Programları",
                    "340.03": "Ders Görevlendirmeleri"
                }
            }
        }
    },
    "400-599": {
        "name": "Sağlık, Kültür ve Spor",
        "departman_adi": "Sağlık, Kültür ve Spor Daire Başkanlığı",
        "codes": {
            "410": {
                "title": "Kültürel Faaliyetler",
                "subcodes": {
                    "410.01": "Konser, Tiyatro, Sergi vb.",
                    "410.02": "Öğrenci Kulüpleri ve Toplulukları"
                }
            },
            "420": {
                "title": "Spor Faaliyetleri",
                "subcodes": {
                    "420.01": "Spor Turnuvaları ve Yarışmalar",
                    "420.02": "Tesis Kullanımı ve Takımlar"
                }
            },
            "430": {
                "title": "Beslenme ve Yemek Hizmetleri",
                "subcodes": {
                    "430.01": "Yemekhane İşletimi ve Menü",
                    "430.02": "Gıda Hijyen ve Denetimleri"
                }
            },
            "440": {
                "title": "Barınma Hizmetleri",
                "subcodes": {
                    "440.01": "Yurt / Konukevi Kayıt ve Tahsis",
                    "440.02": "Yurt İşletim İşlemleri"
                }
            },
            "450": {
                "title": "Sağlık Hizmetleri",
                "subcodes": {
                    "450.01": "Muayene ve Tedavi Hizmetleri",
                    "450.02": "Psikolojik Danışmanlık ve Rehberlik"
                }
            }
        }
    },
    "600-619": {
        "name": "Strateji ve Planlama",
        "departman_adi": "Strateji Geliştirme Daire Başkanlığı",
        "codes": {
            "020": {
                "title": "Kurumsal İstatistikler ve Veri Analizleri",
                "subcodes": {
                    "020.01": "Periyodik İstatistikler",
                    "020.02": "Anket ve Veri Toplama"
                }
            },
            "601": {
                "title": "Stratejik Planlama İşlemleri",
                "subcodes": {
                    "601.01": "Stratejik Plan Hazırlama",
                    "601.02": "İzleme ve Değerlendirme"
                }
            },
            "602": {
                "title": "Performans Programı ve Faaliyet Raporları",
                "subcodes": {
                    "602.01": "Performans Programı",
                    "602.02": "Kurumsal Faaliyet Raporu"
                }
            },
            "610": {
                "title": "İç Kontrol Sistemi Geliştirme Çalışmaları",
                "subcodes": {
                    "610.01": "Risk Yönetimi",
                    "610.02": "İş Süreçleri ve Görev Tanımları"
                }
            }
        }
    },
    "620-639": {
        "name": "Kütüphane",
        "departman_adi": "Kütüphane ve Dokümantasyon Daire Başkanlığı",
        "codes": {
            "622": {
                "title": "Kitap, Süreli Yayın ve Materyal Alımı",
                "subcodes": {
                    "622.01": "Yayın İstekleri ve Seçimi",
                    "622.02": "Bağış ve Değişim Yayınlar"
                }
            },
            "624": {
                "title": "Kataloglama ve Sınıflandırma İşlemleri",
                "subcodes": {
                    "624.01": "Kataloglama",
                    "624.02": "Etiketleme ve Ciltleme"
                }
            },
            "626": {
                "title": "Kütüphane Kullanım ve Ödünç Verme İşleri",
                "subcodes": {
                    "626.01": "Üye İşlemleri",
                    "626.02": "Ödünç Verme / İade / İkaz"
                }
            },
            "632": {
                "title": "Elektronik Veri Tabanı Abonelikleri",
                "subcodes": {
                    "632.01": "Veri Tabanı Talepleri",
                    "632.02": "Abonelik ve Kullanım İstatistikleri"
                }
            }
        }
    },
    "640-659": {
        "name": "Hukuk Müşavirliği",
        "departman_adi": "Hukuk Müşavirliği",
        "codes": {
            "641": {
                "title": "Adli ve İdari Davalar",
                "subcodes": {
                    "641.01": "İdari Davalar",
                    "641.02": "Adli Davalar"
                }
            },
            "645": {
                "title": "İcra Takipleri",
                "subcodes": {
                    "645.01": "Kurum Alacakları",
                    "645.02": "Borç Takibi"
                }
            },
            "651": {
                "title": "Hukuki Mütalaalar",
                "subcodes": {
                    "651.01": "Birimlerden Gelen Hukuki Görüş Talepleri",
                    "651.02": "Dış Kurumlara Verilen Görüşler"
                }
            }
        }
    },
    "700-719": {
        "name": "Bilgi İşlem",
        "departman_adi": "Bilgi İşlem Daire Başkanlığı",
        "codes": {
            "700": {
                "title": "Bilgi İşlem İşleri (Genel)",
                "subcodes": {
                    "700.01": "Bilgi İşlem Politikaları ve Standartları"
                }
            },
            "702": {
                "title": "Yazılım Geliştirme ve Proje İşlemleri",
                "subcodes": {
                    "702.01": "Yazılım Talepleri ve Analiz",
                    "702.02": "Proje Kodlama ve Test Süreçleri"
                }
            },
            "704": {
                "title": "Veri Tabanı ve Sunucu Yönetimi",
                "subcodes": {
                    "704.01": "Veri Tabanı Kurulum ve Yedekleme",
                    "704.02": "Sunucu Sanallaştırma ve Bakım"
                }
            },
            "708": {
                "title": "Donanım, Altyapı ve Ağ Yönetimi",
                "subcodes": {
                    "708.01": "Ağ (Network) Yapılandırması",
                    "708.02": "Donanım Envanter ve Dağıtım"
                }
            },
            "710": {
                "title": "Bilgi ve Siber Güvenlik İşlemleri",
                "subcodes": {
                    "710.01": "Güvenlik Duvarı (Firewall) ve Log Yönetimi",
                    "710.02": "Siber Olaylara Müdahale (SOME)"
                }
            },
            "713": {
                "title": "Teknik Servis ve Bakım Onarım İşlemleri",
                "subcodes": {
                    "713.01": "Arıza Bildirimleri",
                    "713.02": "Periyodik Donanım Bakımları"
                }
            }
        }
    },
    "750-769": {
        "name": "Yapı İşleri",
        "departman_adi": "Yapı İşleri ve Teknik Daire Başkanlığı",
        "codes": {
            "751": {
                "title": "Etüt-Proje ve Kamulaştırma İşleri",
                "subcodes": {
                    "751.01": "Mimari ve Mühendislik Projeleri",
                    "751.02": "Kamulaştırma İşlemleri"
                }
            },
            "755": {
                "title": "Yapım (İnşaat) İhaleleri ve Dosyaları",
                "subcodes": {
                    "755.01": "İnşaat İhale Dosyaları",
                    "755.02": "Hakediş ve Geçici/Kabul İşlemleri"
                }
            },
            "757": {
                "title": "Büyük Onarım ve Tadilat İşleri",
                "subcodes": {
                    "757.01": "Onarım Keşif ve Şartnameleri",
                    "757.02": "Tadilat Uygulamaları"
                }
            },
            "764": {
                "title": "Enerji, Isıtma ve Tesisat İşleri",
                "subcodes": {
                    "764.01": "Elektrik, Su, Doğalgaz Abonelikleri",
                    "764.02": "Tesisat Periyodik Bakımları"
                }
            }
        }
    },
    "840-869": {
        "name": "Mali İşler",
        "departman_adi": "İdari ve Mali İşler Daire Başkanlığı",
        "codes": {
            "841": {
                "title": "Bütçe Hazırlama ve Uygulama",
                "subcodes": {
                    "841.01": "Bütçe Çağrısı ve Hazırlıklar",
                    "841.02": "Bütçe Aktarma ve Revize İşlemleri"
                }
            },
            "843": {
                "title": "Ödenek İşlemleri",
                "subcodes": {
                    "843.01": "Ödenek Gönderme",
                    "843.02": "Tenkis İşlemleri"
                }
            },
            "851": {
                "title": "Muhasebe İşlemleri",
                "subcodes": {
                    "851.01": "Yıl Sonu Hesap Kapama",
                    "851.02": "Mutabakat Belgeleri"
                }
            },
            "855": {
                "title": "Ödeme İşlemleri",
                "subcodes": {
                    "855.01": "Maaş, Ücret ve Yolluk Ödemeleri",
                    "855.02": "Fatura Ödeme Evrakı (Mevzuat/Mal/Hizmet)"
                }
            },
            "869": {
                "title": "Taşınır Mal İşlemleri",
                "subcodes": {
                    "869.01": "Taşınır Giriş / Çıkış (TİF)",
                    "869.02": "Sayım, Düşüm ve Hurda İşlemleri"
                }
            }
        }
    },
    "900-929": {
        "name": "Personel İşleri",
        "departman_adi": "Personel Daire Başkanlığı",
        "codes": {
            "900": {
                "title": "Personel İşleri (Genel)",
                "subcodes": {
                    "900.01": "Personel Politikaları ve İstatistikleri"
                }
            },
            "901": {
                "title": "Kadro İşlemleri",
                "subcodes": {
                    "901.01": "Kadro İhdası ve İptali",
                    "901.02": "Kadro Dağılımı ve Kullanımı"
                }
            },
            "902": {
                "title": "Atama ve Görevlendirme İşleri",
                "subcodes": {
                    "902.01": "Açıktan / Naklen Atamalar",
                    "902.02": "Vekalet ve İkinci Görev"
                }
            },
            "903": {
                "title": "Personel Özlük İşleri",
                "subcodes": {
                    "903.01": "İşe Giriş Belgeleri",
                    "903.02": "Atama İşleri",
                    "903.03": "Terfi ve İntibak İşleri",
                    "903.04": "Hizmet Cetveli ve Hizmet Belgesi",
                    "903.05": "Personel İzin İşlemleri",
                    "903.06": "Görevden Ayrılma",
                    "903.07": "Görevlendirme"
                }
            },
            "907": {
                "title": "Disiplin ve Cezai İşlemler",
                "subcodes": {
                    "907.01": "Disiplin Soruşturmaları",
                    "907.02": "Disiplin Cezaları ve İtirazlar"
                }
            },
            "915": {
                "title": "Sendikal Faaliyetler",
                "subcodes": {
                    "915.01": "Sendika Üyelik / İstifa",
                    "915.02": "Toplu Sözleşme İşlemleri"
                }
            },
            "918": {
                "title": "Emeklilik İşlemleri",
                "subcodes": {
                    "918.01": "Yaş Haddi / İsteğe Bağlı Emeklilik",
                    "918.02": "Malulen Emeklilik"
                }
            }
        }
    },
    "930-949": {
        "name": "Satın Alma ve İhale",
        "departman_adi": "İdari ve Mali İşler Daire Başkanlığı",
        "codes": {
            "930": {
                "title": "Satın Alma ve İhale İşleri (Genel)",
                "subcodes": {
                    "930.01": "Satın Alma Talepleri"
                }
            },
            "934": {
                "title": "İhale İşlemleri",
                "subcodes": {
                    "934.01": "Açık İhale Usulü Dosyaları",
                    "934.02": "Pazarlık Usulü İhale Dosyaları",
                    "934.03": "İhale Komisyon Kararları"
                }
            },
            "942": {
                "title": "Piyasa Fiyat Araştırması",
                "subcodes": {
                    "942.01": "Fiyat Teklif Formları",
                    "942.02": "Yaklaşık Maliyet Cetvelleri"
                }
            },
            "944": {
                "title": "Doğrudan Temin İşlemleri",
                "subcodes": {
                    "944.01": "Doğrudan Temin Onay Belgeleri",
                    "944.02": "Fatura ve Alım Belgeleri"
                }
            }
        }
    }
}





@app.route('/sdp')
@login_required
def sdp_arsiv():
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
                           aktif_donem=aktif_donem)



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
    ait_oldugu_yil = request.form.get('ait_oldugu_yil', session.get('aktif_donem', '2026'))

    

    if dosya.filename == '':

        flash("Geçerli bir dosya seçin.")

        return redirect(url_for('sdp_arsiv'))

        

    filename = secure_filename(dosya.filename)

    dosya.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    

    conn = get_db_connection()

    conn.execute('''

        INSERT INTO sdp_evraklar (kullanici_id, departman, ana_sdp_kodu, alt_sdp_kodu, baslik, etiketler, aciklama, dosya_adi, ait_oldugu_yil)

        VALUES (?, ?, ?, ?, ?, ?, ?, ?), ?)

    ''', (session['kullanici_id'], departman, ana_kod, alt_kod, baslik, etiketler, aciklama, filename, ait_oldugu_yil))



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
    return redirect(url_for('sdp_arsiv'))


@app.route('/klasor/sil/<path:klasor_id>', methods=['POST'])
@login_required
def klasor_sil(klasor_id):
    if session.get('rol') != 'admin':
        flash("Klasör silme yetkiniz yok.")
        return redirect(url_for('ana_sayfa'))
    
    conn = get_db_connection()
    conn.execute('UPDATE klasorler SET is_deleted = 1 WHERE id = ?', (klasor_id,))
    conn.commit()
    conn.close()
    flash("Klasör çöp kutusuna taşındı.")
    return redirect(url_for('ana_sayfa'))

@app.route('/cop_kutusu')
@login_required
def cop_kutusu():
    if session.get('rol') != 'admin':
        flash("Çöp kutusunu görüntüleme yetkiniz yok.")
        return redirect(url_for('ana_sayfa'))
        
    conn = get_db_connection()
    silinmis_klasorler = conn.execute('SELECT * FROM klasorler WHERE is_deleted = 1').fetchall()
    conn.close()
    
    return render_template('cop_kutusu.html', klasorler=silinmis_klasorler)

@app.route('/klasor/kurtar/<path:klasor_id>', methods=['POST'])
@login_required
def klasor_kurtar(klasor_id):
    if session.get('rol') != 'admin':
        flash("Klasör kurtarma yetkiniz yok.")
        return redirect(url_for('ana_sayfa'))
    
    conn = get_db_connection()
    conn.execute('UPDATE klasorler SET is_deleted = 0 WHERE id = ?', (klasor_id,))
    conn.commit()
    conn.close()
    flash("Klasör başarıyla geri yüklendi.")
    return redirect(url_for('cop_kutusu'))

@app.route('/klasor/kalici_sil/<path:klasor_id>', methods=['POST'])
@login_required
def klasor_kalici_sil(klasor_id):
    if session.get('rol') != 'admin':
        flash("Kalıcı silme yetkiniz yok.")
        return redirect(url_for('ana_sayfa'))
    
    conn = get_db_connection()
    # 1. Get associated evraklar
    evraklar = conn.execute('SELECT dosya_adi FROM evraklar WHERE klasor_id = ?', (klasor_id,)).fetchall()
    for evrak in evraklar:
        dosya_yolu = os.path.join(app.config['UPLOAD_FOLDER'], evrak['dosya_adi'])
        if os.path.exists(dosya_yolu):
            try:
                os.remove(dosya_yolu)
            except:
                pass
                
    # 2. Delete from tables
    conn.execute('DELETE FROM evraklar WHERE klasor_id = ?', (klasor_id,))
    conn.execute('DELETE FROM sdp_evraklar WHERE ana_sdp_kodu = ?', (klasor_id,))
    conn.execute('DELETE FROM klasor_yetkileri WHERE klasor_id = ?', (klasor_id,))
    conn.execute('DELETE FROM klasorler WHERE id = ?', (klasor_id,))
    
    conn.commit()
    conn.close()
    
    flash("Klasör ve içindeki tüm evraklar kalıcı olarak silindi.")
    return redirect(url_for('cop_kutusu'))


