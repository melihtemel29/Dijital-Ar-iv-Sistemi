import sqlite3

conn = sqlite3.connect('arsiv.db')
cursor = conn.cursor()

# Eklenmesi istenen evrak tipleri
yeni_evraklar = ['Gizlilik Sözleşmesi', 'Fatura', 'Tutanak', 'Teknik Şartname']

# 4. gruptaki tüm klasörleri al
cursor.execute("SELECT id, ad, zorunlu_evraklar FROM klasorler WHERE grup = '4'")
folders = cursor.fetchall()

for row in folders:
    f_id, ad, mevcut = row
    
    # Mevcut evrakları listeye çevir
    mevcut_liste = [x.strip() for x in mevcut.split(',')] if mevcut else []
    
    # Hangi klasöre ne eklenecek mantığını kuralım:
    eklenecekler = []
    
    # Tüm satın alma, bakım ve servis klasörlerine hepsini ekleyelim (yazılım faaliyetleri hariç)
    # Çoğu klasör dışarıdan hizmet/ürün alımı ile ilgili olduğu için hepsine Fatura, Tutanak, Teknik Şartname uyar.
    # Güvenlikle ilgili olanlara Gizlilik Sözleşmesi de uyar.
    for y in yeni_evraklar:
        if y not in mevcut_liste:
            eklenecekler.append(y)
            
    # Listeyi birleştir
    yeni_liste = mevcut_liste + eklenecekler
    yeni_deger = ", ".join(yeni_liste)
    
    # Veritabanını güncelle
    cursor.execute("UPDATE klasorler SET zorunlu_evraklar = ? WHERE id = ?", (yeni_deger, f_id))

conn.commit()
conn.close()
print("IT klasörlerinin zorunlu evrakları güncellendi.")
