import re
import os

# 1. Update app.py to add goruntule and sil routes, and update sdp_yukle
with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

# Add goruntule and sil routes if they don't exist
if "@app.route('/sdp/goruntule/" not in app_content:
    routes_to_add = """
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
"""
    app_content = app_content + routes_to_add

# Modify sdp_yukle to sync with klasorler and evraklar
yukle_sync_code = """
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
        
    conn.execute('INSERT INTO evraklar (klasor_id, evrak_tipi, dosya_adi) VALUES (?, ?, ?)', (ana_kod, baslik, filename))
"""

if "# SDP Klasör Senkronizasyonu" not in app_content:
    app_content = app_content.replace(
        "    conn.commit()\n    conn.close()\n    \n    flash(\"Evrak başarıyla SDP sistemine eklendi.\")",
        yukle_sync_code + "\n    conn.commit()\n    conn.close()\n    \n    flash(\"Evrak başarıyla SDP sistemine ve Klasörlere eklendi.\")"
    )

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)

# 2. Update sdp_arsiv.html to add View and Delete buttons
with open('templates/sdp_arsiv.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

buttons_html = """                                        <a href="/sdp/goruntule{{ '/' + evrak.dosya_adi }}" class="btn btn-sm btn-light border text-success" title="Görüntüle" target="_blank">
                                            <i class="bi bi-eye"></i>
                                        </a>
                                        <a href="/sdp/indir{{ '/' + evrak.dosya_adi }}" class="btn btn-sm btn-light border text-primary" title="İndir">
                                            <i class="bi bi-download"></i>
                                        </a>
                                        {% if session.get('rol') == 'admin' or session.get('kullanici_id') == evrak.kullanici_id %}
                                        <a href="/sdp/sil/{{ evrak.id }}" class="btn btn-sm btn-light border text-danger" title="Sil" onclick="return confirm('Bu evrakı silmek istediğinize emin misiniz?')">
                                            <i class="bi bi-trash"></i>
                                        </a>
                                        {% endif %}"""

old_buttons = """                                        <a href="/sdp/indir{{ '/' + evrak.dosya_adi }}" class="btn btn-sm btn-light border" title="İndir">
                                            <i class="bi bi-download text-primary"></i>
                                        </a>"""

html_content = html_content.replace(old_buttons, buttons_html)

with open('templates/sdp_arsiv.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Features added successfully.")
