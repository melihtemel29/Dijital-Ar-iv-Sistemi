with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Change ana_sayfa route to /klasorler
old_ana_sayfa = '''@app.route('/')
@login_required
def ana_sayfa():'''

new_ana_sayfa = '''@app.route('/klasorler')
@login_required
def ana_sayfa():'''

if old_ana_sayfa in content:
    content = content.replace(old_ana_sayfa, new_ana_sayfa)

# Add new dashboard route
dashboard_code = '''
@app.route('/')
@login_required
def dashboard():
    klasorler = get_authorized_folders(session['kullanici_id'], session['rol'])
    toplam_klasor = len(klasorler)
    return render_template('dashboard.html', toplam_klasor=toplam_klasor, aktif_donem="2026")

'''

# Insert dashboard_code right before ana_sayfa
content = content.replace(new_ana_sayfa, dashboard_code + new_ana_sayfa)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("app.py updated with dashboard route.")
