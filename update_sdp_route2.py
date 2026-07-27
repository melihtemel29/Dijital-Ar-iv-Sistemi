import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_route = """@app.route('/sdp')
@login_required
def sdp_arsiv():
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
            WHERE s.ana_sdp_kodu = ?
            ORDER BY s.yukleme_tarihi DESC
        ''', (alt_kategori,)).fetchall()
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
                           secili_kategori_data=secili_kategori_data)"""

# Find the old route
pattern = re.compile(r'@app\.route\(\'/sdp\'\)\s*@login_required\s*def sdp_arsiv\(\):.*?return render_template\(\'sdp_arsiv\.html\', categories=allowed_categories, evraklar=evraklar\)', re.DOTALL)
content = pattern.sub(new_route, content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('app.py sdp_arsiv route updated')
