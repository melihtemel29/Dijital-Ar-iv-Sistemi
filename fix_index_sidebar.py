import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to replace the sidebar navigation section.
# It starts from: <p class="nav-heading mt-4">ARŞİV BÖLÜMLERİ (SDP)</p>
# It ends at the theme toggle or logout button.
# Let's find the exact block.

# Find the start of nav-heading
start_idx = content.find('<p class="nav-heading mt-4">ARŞİV BÖLÜMLERİ (SDP)</p>')
if start_idx == -1:
    start_idx = content.find('<p class="nav-heading">')

# Find the logout button
logout_idx = content.find('<a href="/logout" class="btn btn-danger')
if logout_idx == -1:
    logout_idx = content.find('<a href="/logout"')

# We will replace everything from start_idx to the div containing logout_idx.
# Actually, let's just use regex to replace the old ARŞİV BÖLÜMLERİ logic with the new one.
# It's safer to find exactly what to replace.

old_sidebar_pattern = re.compile(r'<p class="nav-heading mt-4">ARŞİV BÖLÜMLERİ \(SDP\)</p>.*?<div style="margin-top: 30px; margin-bottom: 20px; width: 100%; padding: 0 15px;">', re.DOTALL)

new_sidebar_html = """<p class="nav-heading">Menü</p>
            <a class="nav-link" href="{{ url_for('dashboard') }}"><i class="bi bi-grid-fill" style="color: #3498db;"></i> Ana Sayfa</a>
            
            <a class="nav-link active" href="{{ url_for('ana_sayfa') }}"><i class="bi bi-folder2-open" style="color: #f39c12;"></i> Klasörler</a>
            
            <div style="padding-left: 20px; border-left: 2px solid rgba(255,255,255,0.05); margin-left: 28px; margin-bottom: 10px;">
                <a href="#" class="nav-link" style="font-size: 13px; padding: 6px 10px; min-height: auto;" onclick="filtreleGrup('HEPSİ', this)"><i class="bi bi-grid-3x3-gap-fill" style="color: #3498db; font-size: 14px;"></i> Tümünü Gör</a>
                <a href="#" class="nav-link" style="font-size: 13px; padding: 6px 10px; min-height: auto;" onclick="filtreleGrup('1', this)"><i class="bi bi-building" style="color: #bdc3c7; font-size: 14px;"></i> 1. Bölüm: Genel ve İdari</a>
                <a href="#" class="nav-link" style="font-size: 13px; padding: 6px 10px; min-height: auto;" onclick="filtreleGrup('2', this)"><i class="bi bi-people-fill" style="color: #bdc3c7; font-size: 14px;"></i> 2. Bölüm: Personel ve Özlük</a>
                <a href="#" class="nav-link" style="font-size: 13px; padding: 6px 10px; min-height: auto;" onclick="filtreleGrup('3', this)"><i class="bi bi-cash-stack" style="color: #bdc3c7; font-size: 14px;"></i> 3. Bölüm: Mali İşler</a>
                <a href="#" class="nav-link" style="font-size: 13px; padding: 6px 10px; min-height: auto;" onclick="filtreleGrup('4', this)"><i class="bi bi-cpu" style="color: #bdc3c7; font-size: 14px;"></i> 4. Bölüm: Bilgi Teknoloji.</a>
                <a href="#" class="nav-link" style="font-size: 13px; padding: 6px 10px; min-height: auto;" onclick="filtreleGrup('5', this)"><i class="bi bi-shield-check" style="color: #bdc3c7; font-size: 14px;"></i> 5. Bölüm: Hukuk</a>
            </div>

            <a class="nav-link" href="{{ url_for('sdp_arsiv') }}"><i class="bi bi-file-earmark-medical-fill" style="color: #9b59b6;"></i> SDP Arşivi</a>
            
            {% if session.get('rol') == 'admin' %}
            <a class="nav-link" href="{{ url_for('stok_sayfasi') }}"><i class="bi bi-box-seam" style="color: #2ecc71;"></i> Stok & Sarf Malzeme</a>
            <a class="nav-link" href="{{ url_for('admin_panel') }}"><i class="bi bi-shield-lock-fill" style="color: #e74c3c;"></i> Admin Paneli</a>
            {% endif %}

            <div style="margin-top: 30px; margin-bottom: 20px; width: 100%; padding: 0 15px;">"""

if old_sidebar_pattern.search(content):
    new_content = old_sidebar_pattern.sub(new_sidebar_html, content)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully updated index.html")
else:
    print("Could not find the target HTML block in index.html")
    # Let's write the file content out to inspect if it failed
    with open('debug_index.html', 'w', encoding='utf-8') as f:
        f.write(content)
