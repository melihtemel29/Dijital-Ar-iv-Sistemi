import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update get_authorized_folders
def_get = r"def get_authorized_folders\(user_id, rol\):"
new_def_get = r"def get_authorized_folders(user_id, rol, aktif_donem=None):\n    if not aktif_donem:\n        from flask import session\n        aktif_donem = session.get('aktif_donem', '2026')"
content = re.sub(def_get, new_def_get, content)

yuklenenler_q = r"yuklenenler = conn\.execute\('SELECT evrak_tipi FROM evraklar WHERE klasor_id = \?', \(k_dict\['id'\],\)\)\.fetchall\(\)"
new_yuklenenler_q = r"yuklenenler = conn.execute('SELECT evrak_tipi FROM evraklar WHERE klasor_id = ? AND ait_oldugu_yil = ?', (k_dict['id'], aktif_donem)).fetchall()"
content = re.sub(yuklenenler_q, new_yuklenenler_q, content)

# 2. Update dashboard
old_dash = r"def dashboard\(\):\n    klasorler = get_authorized_folders\(session\['kullanici_id'\], session\['rol'\]\)\n    toplam_klasor = len\(klasorler\)\n    return render_template\('dashboard\.html', toplam_klasor=toplam_klasor, aktif_donem=\"2026\"\)"
new_dash = r"""def dashboard():
    aktif_donem = session.get('aktif_donem', '2026')
    klasorler = get_authorized_folders(session['kullanici_id'], session['rol'], aktif_donem)
    toplam_klasor = len(klasorler)
    eksik_sayisi = sum(1 for k in klasorler if k['durum'] == 'Eksik Evrak')
    return render_template('dashboard.html', toplam_klasor=toplam_klasor, eksik_sayisi=eksik_sayisi, aktif_donem=aktif_donem)"""
content = re.sub(old_dash, new_dash, content)

# 3. Add set_donem route before dashboard
if "@app.route('/set_donem/<yil>')" not in content:
    set_donem_route = """@app.route('/set_donem/<yil>')
@login_required
def set_donem(yil):
    session['aktif_donem'] = yil
    return redirect(request.referrer or url_for('dashboard'))\n\n"""
    # Find @app.route('/')
    content = re.sub(r'(@app\.route\(\'/\'\)\s*@login_required\s*def dashboard\(\):)', set_donem_route + r'\1', content)

# 4. Update ana_sayfa
old_ana = r"def ana_sayfa\(\):\n    klasorler = get_authorized_folders\(session\['kullanici_id'\], session\['rol'\]\)\n    return render_template\('index\.html', klasorler=klasorler, secili_klasor=None\)"
new_ana = r"""def ana_sayfa():
    aktif_donem = session.get('aktif_donem', '2026')
    klasorler = get_authorized_folders(session['kullanici_id'], session['rol'], aktif_donem)
    return render_template('index.html', klasorler=klasorler, secili_klasor=None, aktif_donem=aktif_donem)"""
content = re.sub(old_ana, new_ana, content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("app.py thoroughly updated")
