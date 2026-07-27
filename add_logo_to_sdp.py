import re

with open('templates/sdp_arsiv.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add CSS rules
css_to_add = """
        .system-title { font-size: 13px; color: #fff; opacity: 0.9; font-weight: 500; padding: 10px 0 15px 0px; border-bottom: 1px solid rgba(255,255,255,0.08); margin: 0; text-align: center; }
        .logo-container { padding: 25px 20px 20px 20px; display: flex; justify-content: center; align-items: center; }
        .logo-container img { max-width: 140px; height: auto; }
"""

if '.logo-container' not in content:
    content = content.replace("        .sidebar .brand {", css_to_add + "\n        .sidebar .brand {")

# Replace the HTML part
old_html = """        <div class="brand">
            <i class="bi bi-shield-check text-primary"></i> SDP Arşivi
        </div>"""

new_html = """        <div class="logo-container text-center">
            <a href="{{ url_for('dashboard') }}"><img src="{{ url_for('static', filename='ktu_logo_new.png') }}" alt="Kurum Logosu"></a>
        </div>
        <p class="system-title">Dijital Arşiv Sistemi</p>"""

if 'class="brand"' in content:
    content = content.replace(old_html, new_html)
    # Also handle possible regex match if exactly spacing is different
    content = re.sub(r'<div class="brand">.*?</div>', new_html, content, flags=re.DOTALL)

with open('templates/sdp_arsiv.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Logo added to sdp_arsiv.html")
