import sqlite3

folders = [
    # Group 1
    ("934.01.02", "YANGIN ALARM SİSTEMLERİ, KESİNTİSİZ GÜÇ KAYNAĞI, JENERATÖR BAKIM SÖZLEŞMESİ", "1", "Sözleşme, Fatura, Bakım Formu"),
    ("949", "E-İMZA POSTA, KARGO, FATURA ve TUTANAKLAR", "1", "Fatura, Teslim Tutanağı"),
    ("950.01.01", "GELEN EVRAK", "1", "Üst Yazı, Ekler"),
    ("950.01.02", "GİDEN EVRAK", "1", "Üst Yazı, Dağıtım Listesi"),
    # Group 2
    ("841.01.01", "PART TIME ÖĞRENCİLER", "2", "Sözleşme, SGK İşe Giriş Bildirgesi, Puantaj"),
    ("841.02.01", "STAJYER ÖĞRENCİLER", "2", "Kabul Belgesi, SGK Bildirgesi, Değerlendirme Formu"),
    ("855.02.01.01", "SÜREKLİ İŞÇİ PUANTAJ", "2", "Puantaj Cetveli, İmzalı Liste"),
    ("855.02.01.03", "EK ÖZEL HİZMET TAZMİNATI", "2", "Onay Belgesi, Bordro"),
    ("869-1", "AYRILAN PERSONEL-1", "2", "İlişik Kesme Belgesi, SGK Çıkış Bildirgesi"),
    ("869-2", "AYRILAN PERSONEL-2", "2", "İlişik Kesme Belgesi, SGK Çıkış Bildirgesi"),
    # Group 3
    ("020", "BİDB YÖNETİM KLAVUZU", "3", "Kılavuz Belgesi, Onay Yazısı"),
    ("663.02", "İÇ KONTROL", "3", "Denetim Raporu, Eylem Planı"),
    ("811.01.01", "ÖDENEK TALEPLERİ", "3", "Talep Yazısı, Bütçe Fişi"),
    ("821.03", "MAL ve HİZMET ALIM FATURA, TUTANAKLAR", "3", "Fatura, Kabul Tutanağı"),
    # Group 4
    ("713.01", "BİLGİ GÜVENLİĞİ, GİZLİLİK SÖZLEŞMESİ, GÜVENLİK EYLEM PLANLARI", "4", "Sözleşme, Eylem Planı Raporu"),
    ("713.03", "ANTI SPAM AĞ GEÇİDİ", "4", "Lisans Belgesi, Konfigürasyon Raporu"),
    ("713.03-2", "SIZMA TESTİ", "4", "Test Raporu, Zafiyet Giderme Kanıtı"),
    ("713.05", "SSL WILDCARD ELEKTRONİK SUNUCU SERTİFİKASI", "4", "Sertifika Dosyası, Fatura"),
    ("713.06", "ZAMAN DAMGASI", "4", "Kullanım Raporu, Sözleşme"),
    ("714.01.02", "YAZILIM BİRİMİ FAALİYETLERİ", "4", "Faaliyet Raporu, Proje Onay Belgesi"),
    ("714.03", "EBYS TEKNİK DESTEK", "4", "Destek Formu, Talep Yazısı"),
    ("715.01", "VERİ TABANI BAKIM ve DESTEK HİZMETİ", "4", "Bakım Raporu, Performans Raporu"),
    ("715.02", "SANALLAŞTIRMA ve YEDEKLEME", "4", "Sistem Kayıtları, Yedekleme Raporu"),
    ("715.02.01", "DİSK TABANLI YEDEKLEME ÜNİTESİ", "4", "Kapasite Raporu, Donanım Faturası"),
    ("715.03", "SUNUCU ve DİSK DEPOLAMA TEKNİK BAKIM", "4", "Bakım Sözleşmesi, Arıza Raporu"),
    ("719", "MICROSOFT EĞİTİM ÇÖZÜMÜ SÖZLEŞMELERİ", "4", "Sözleşme Metni, Lisans Dosyası"),
    ("821.01.02", "HİZMET ALIM SÖZLEŞME, FATURA ve TUTANAKLAR", "4", "Hizmet Sözleşmesi, Hakediş Raporu, Fatura"),
    # Group 5
    ("641.03.01", "SORUŞTURMA EVRAKLARI", "5", "Soruşturma Emri, İfade Tutanağı, Soruşturma Raporu")
]

conn = sqlite3.connect('arsiv.db')
cursor = conn.cursor()

cursor.execute('DELETE FROM klasorler')
cursor.execute('DELETE FROM klasor_yetkileri')
cursor.execute('DELETE FROM evraklar')

for fid, ad, grup, zorunlu in folders:
    cursor.execute('INSERT INTO klasorler (id, ad, grup, zorunlu_evraklar, bitis_tarihi_var_mi) VALUES (?, ?, ?, ?, 0)', (fid, ad, grup, zorunlu))

cursor.execute("SELECT id FROM kullanicilar WHERE rol='admin'")
admin_id = cursor.fetchone()
if admin_id:
    admin_id = admin_id[0]
    for fid, ad, grup, zorunlu in folders:
        cursor.execute('INSERT INTO klasor_yetkileri (kullanici_id, klasor_id) VALUES (?, ?)', (admin_id, fid))

conn.commit()
conn.close()
print('Database migration successful.')
