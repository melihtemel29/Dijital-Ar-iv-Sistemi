with open('templates/stok.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix Logo
old_logo = '''        <div class="logo-container">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div class="ktu-logo-emblem" style="width: 50px; height: 50px; border: 4px solid #fff; border-radius: 50%; position: relative;"></div>
                <div class="logo-text-wrapper">
                    <span class="logo-main-title">KTÜ</span>
                    <div class="logo-sub-info">
                        <span class="logo-year">1955</span>
                        <span class="logo-uni-name">KARADENİZ TEKNİK ÜNİVERSİTESİ</span>
                    </div>
                </div>
            </div>
        </div>
        <h5 class="system-title">Dijital Arşiv Sistemi</h5>'''

new_logo = '''        <div class="logo-container text-center">
            <img src="{{ url_for('static', filename='ktu_logo_new.png') }}" alt="Kurum Logosu">
        </div>
        <p class="system-title">Dijital Arşiv Sistemi</p>'''

if old_logo in content:
    content = content.replace(old_logo, new_logo)

# 2. Add Remaining Stock to table headers
if '<th>Çıkış Miktarı</th>' in content and '<th>Güncel Kalan</th>' not in content:
    content = content.replace('<th>Çıkış Miktarı</th>', '<th>Çıkış Miktarı</th>\n                                        <th>Güncel Kalan</th>')

# 3. Add Remaining Stock to table body
old_td = '<td><span class="badge bg-danger">{{ islem.adet }} {{ islem.birim_tipi }} Çıkış</span></td>'
new_td = '<td><span class="badge bg-danger">{{ islem.adet }} {{ islem.birim_tipi }} Çıkış</span></td>\n                                        <td><span class="badge bg-primary text-white">{{ islem.stok_adedi }} {{ islem.birim_tipi }} Kaldı</span></td>'
if old_td in content:
    content = content.replace(old_td, new_td)

with open('templates/stok.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("stok.html updated with logo and remaining stock column.")
