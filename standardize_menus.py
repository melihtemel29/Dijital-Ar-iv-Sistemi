import re

templates = {
    'dashboard.html': 'dashboard',
    'sdp_arsiv.html': 'sdp',
    'stok.html': 'stok',
    'admin.html': 'admin'
}

for filename, active_key in templates.items():
    filepath = f"templates/{filename}"
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Build the exact menu block
        menu_block = f"""        <p class="nav-heading">Menü</p>
        <a class="nav-link {'active' if active_key == 'dashboard' else ''}" href="{{{{ url_for('dashboard') }}}}"><i class="bi bi-grid-fill" style="color: #3498db;"></i> Ana Sayfa</a>
        <a class="nav-link {'active' if active_key == 'klasorler' else ''}" href="{{{{ url_for('ana_sayfa') }}}}"><i class="bi bi-folder2-open" style="color: #f39c12;"></i> Klasörler</a>
        <a class="nav-link {'active' if active_key == 'sdp' else ''}" href="{{{{ url_for('sdp_arsiv') }}}}"><i class="bi bi-file-earmark-medical-fill" style="color: #9b59b6;"></i> SDP Arşivi</a>
        
        {{% if session.get('rol') == 'admin' %}}
        <a class="nav-link {'active' if active_key == 'stok' else ''}" href="{{{{ url_for('stok_sayfasi') }}}}"><i class="bi bi-box-seam" style="color: #2ecc71;"></i> Stok & Sarf Malzeme</a>
        <a class="nav-link {'active' if active_key == 'admin' else ''}" href="{{{{ url_for('admin_panel') }}}}"><i class="bi bi-shield-lock-fill" style="color: #e74c3c;"></i> Admin Paneli</a>
        {{% endif %}}"""

        # Replace everything between <p class="nav-heading"> and <div style="margin-top
        # Wait, not all use EXACTLY <p class="nav-heading">Menü</p>. Some might have MENÜ.
        # Let's use regex.
        pattern = re.compile(r'<p class="nav-heading">.*?(?=<div style="margin-top: [23]0px;)', re.DOTALL | re.IGNORECASE)
        
        if pattern.search(content):
            new_content = pattern.sub(menu_block + '\n        ', content)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filename}")
        else:
            print(f"Pattern not found in {filename}")
            
    except Exception as e:
        print(f"Error processing {filename}: {e}")

# index.html (Folders) might have a different structure, let's check it separately.
try:
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    # It currently has something like <a href="/" class="nav-link text-white... 
    # Let's not touch index.html if it's too different, but user mainly complained about SDP.
except:
    pass
