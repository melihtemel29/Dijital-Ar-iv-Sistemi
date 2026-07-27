import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix dashboard
# Replace the entire dashboard function
dash_pattern = re.compile(r'def dashboard\(\):.*?return render_template\([^\)]+\)', re.DOTALL)
new_dash = """def dashboard():
    aktif_donem = session.get('aktif_donem', '2026')
    klasorler = get_authorized_folders(session['kullanici_id'], session['rol'], aktif_donem)
    toplam_klasor = len(klasorler)
    eksik_sayisi = sum(1 for k in klasorler if k['durum'] == 'Eksik Evrak')
    return render_template('dashboard.html', toplam_klasor=toplam_klasor, eksik_sayisi=eksik_sayisi, aktif_donem=aktif_donem)"""
content = dash_pattern.sub(new_dash, content)

# Fix ana_sayfa
ana_pattern = re.compile(r'def ana_sayfa\(\):.*?return render_template\(\'index\.html\'[^\)]+\)', re.DOTALL)
new_ana = """def ana_sayfa():
    aktif_donem = session.get('aktif_donem', '2026')
    klasorler = get_authorized_folders(session['kullanici_id'], session['rol'], aktif_donem)
    return render_template('index.html', klasorler=klasorler, secili_klasor=None, aktif_donem=aktif_donem)"""
content = ana_pattern.sub(new_ana, content)

# Fix sdp_yukle
sdp_yukle_pattern = re.compile(r'(def sdp_yukle\(\):.*?departman = session\.get\(\'departman\', \'Genel\'\))', re.DOTALL)
new_sdp_yukle = r"""\1
    ait_oldugu_yil = request.form.get('ait_oldugu_yil', session.get('aktif_donem', '2026'))"""
content = sdp_yukle_pattern.sub(new_sdp_yukle, content)

sdp_insert_pattern = re.compile(r'(INSERT INTO sdp_evraklar.*?dosya_adi)\)(.*?VALUES \(\?, \?, \?, \?, \?, \?, \?, \?\))', re.DOTALL)
new_sdp_insert = r"\1, ait_oldugu_yil)\2, ?)"
content = sdp_insert_pattern.sub(new_sdp_insert, content)

sdp_execute_pattern = re.compile(r'(aciklama, filename)\)\)', re.DOTALL)
new_sdp_execute = r"\1, ait_oldugu_yil))"
content = sdp_execute_pattern.sub(new_sdp_execute, content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("app.py successfully replaced")
