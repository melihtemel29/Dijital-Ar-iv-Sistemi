import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Update get_authorized_folders
# We'll use regex to find the k_dict['durum'] line
old_line = "k_dict['durum'] = 'Tamamlandı' if len(eksikler) == 0 else 'Eksik Evrak'"
new_line = "k_dict['durum'] = 'Boş Klasör' if len(yuklenen_tipler) == 0 else ('Tamamlandı' if len(eksikler) == 0 else 'Eksik Evrak')"

if old_line in content:
    content = content.replace(old_line, new_line)
else:
    print("Could not find old_line in app.py")


# Update dashboard route
old_dashboard = '''def dashboard():
    klasorler = get_authorized_folders(session['kullanici_id'], session['rol'])
    toplam_klasor = len(klasorler)
    return render_template('dashboard.html', toplam_klasor=toplam_klasor, aktif_donem="2026")'''

new_dashboard = '''def dashboard():
    klasorler = get_authorized_folders(session['kullanici_id'], session['rol'])
    toplam_klasor = len(klasorler)
    eksik_sayisi = sum(1 for k in klasorler if k['durum'] == 'Eksik Evrak')
    return render_template('dashboard.html', toplam_klasor=toplam_klasor, eksik_sayisi=eksik_sayisi, aktif_donem="2026")'''

content = content.replace(old_dashboard, new_dashboard)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('app.py updated')
