import os

sdp_code = """

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
    conn.commit()
    conn.close()
    
    flash("Evrak başarıyla SDP sistemine eklendi.")
    return redirect(url_for('sdp_arsiv'))

@app.route('/sdp/indir/<path:dosya_adi>')
@login_required
def sdp_indir(dosya_adi):
    return send_from_directory(app.config['UPLOAD_FOLDER'], dosya_adi, as_attachment=True)
"""

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Make sure we don't add it twice
if "SDP_KODLARI" not in content:
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content + "\n" + sdp_code)
    print("SDP routes and variables appended to app.py")
else:
    print("SDP code already exists in app.py")
