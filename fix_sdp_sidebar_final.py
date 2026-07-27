import re

with open('templates/sdp_arsiv.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Profile Card
old_profile_card = """        <a href="{{ url_for('dashboard') }}" class="profile-card text-decoration-none">
            <div class="profile-img" style="overflow: hidden;">
                {% if session.get('rol') == 'admin' %}
                    <img src="{{ url_for('static', filename='profile.jpg') }}" alt="Profil" style="width: 100%; height: 100%; object-fit: cover; object-position: top;">
                {% else %}
                    <i class="bi bi-person-fill"></i>
                {% endif %}
            </div>
            <div class="profile-info text-white">
                <h6 class="m-0" style="font-size: 14px; font-weight: 600; color: #a2a5b9;">{{ session.get('ad_soyad', 'Personel') }}</h6>
                <small style="color: #6c757d; font-size: 11px;">{{ session.get('departman', 'Genel') }}</small>
            </div>
        </a>"""

new_profile_card = """        <a href="{{ url_for('dashboard') }}" class="profile-card text-decoration-none">
            <div class="profile-img" style="overflow: hidden;">
                {% if session.get('rol') == 'admin' %}
                    <img src="{{ url_for('static', filename='profile.jpg') }}" alt="Profil" style="width: 100%; height: 100%; object-fit: cover; object-position: top;">
                {% else %}
                    <i class="bi bi-person-fill"></i>
                {% endif %}
            </div>
            <div class="profile-info text-white">
                <h6 class="m-0" style="font-size: 14px; font-weight: 600;">{{ 'Sistem Yöneticisi' if session.get('rol') == 'admin' else 'Kullanıcı' }}</h6>
                <small style="color: #a2a5b9; font-size: 12px;">{{ session.get('ad_soyad', 'Personel') }}</small>
            </div>
        </a>"""

content = content.replace(old_profile_card, new_profile_card)

# If it didn't match perfectly, use regex
if new_profile_card not in content:
    content = re.sub(r'<a href="\{\{ url_for\(\'dashboard\'\) \}\}" class="profile-card text-decoration-none">.*?</a>', new_profile_card, content, flags=re.DOTALL)


# 2. Update bottom section (Logout and Theme switch)
# Use regex to find the section starting from <div style="margin-top: 20px (or similar) to the end of sidebar </div>
old_bottom_pattern = re.compile(r'<div style="margin-top: 20px; width: 100%; padding: 0 15px;">\s*<a href="/logout".*?</div>\s*</div>', re.DOTALL)
old_bottom_pattern_2 = re.compile(r'<div style="margin-top: 30px; margin-bottom: 20px; width: 100%; padding: 0 15px;">\s*<a href="/logout".*?</div>\s*</div>', re.DOTALL)


new_bottom = """        <div style="margin-top: 30px; margin-bottom: 20px; width: 100%; padding: 0 15px;">
            <a href="/logout" class="btn btn-danger btn-sm w-100 fw-bold d-flex align-items-center justify-content-center py-2"><i class="bi bi-box-arrow-left me-2"></i> Çıkış Yap</a>
                <!-- Tema Geçiş Düğmesi -->
                <div class="theme-switch-wrapper mt-3 text-center">
                    <label class="theme-switch" for="checkbox">
                        <input type="checkbox" id="checkbox" />
                        <div class="slider round">
                            <i class="bi bi-moon-fill ms-1" style="line-height:28px;"></i>
                            <i class="bi bi-sun-fill me-1" style="line-height:28px;"></i>
                        </div>
                    </label>
                </div>
        </div>
    </div>"""

# Wait, in sdp_arsiv.html, it's currently:
# <div style="margin-top: 20px; width: 100%; padding: 0 15px;">
#             <a href="/logout" ...>
#                 <i class="bi bi-box-arrow-left me-2"></i> Çıkış Yap
#             </a>
#         </div>
#
#         <div class="theme-switch-wrapper mt-auto">
#             <div class="form-check form-switch d-flex align-items-center gap-2">
# ...
#         </div>
#     </div>

old_bottom_pattern_3 = re.compile(r'<div style="margin-top: 20px; width: 100%; padding: 0 15px;">\s*<a href="/logout".*?</div>\s*<div class="theme-switch-wrapper mt-auto">.*?</div>\s*</div>', re.DOTALL)
old_bottom_pattern_4 = re.compile(r'<div style="margin-top: 30px; margin-bottom: 20px; width: 100%; padding: 0 15px;">\s*<a href="/logout".*?</div>\s*<div class="theme-switch-wrapper mt-auto">.*?</div>\s*</div>', re.DOTALL)
old_bottom_pattern_5 = re.compile(r'<div style="margin-top: 30px; margin-bottom: 20px; width: 100%; padding: 0 15px;">\s*<a href="/logout" class="btn btn-outline-danger.*?</div>\s*</div>', re.DOTALL)


# Let's try replacing them.
if old_bottom_pattern_3.search(content):
    content = old_bottom_pattern_3.sub(new_bottom, content)
elif old_bottom_pattern_4.search(content):
    content = old_bottom_pattern_4.sub(new_bottom, content)
elif old_bottom_pattern_5.search(content):
    content = old_bottom_pattern_5.sub(new_bottom, content)
elif '<a href="/logout" class="btn btn-outline-danger' in content:
    # Just do a rough replace
    start_idx = content.find('<div style="margin-top: 30px; margin-bottom: 20px; width: 100%; padding: 0 15px;">')
    if start_idx == -1:
        start_idx = content.find('<div style="margin-top: 20px;')
    
    end_idx = content.find('<!-- Main Content -->')
    if start_idx != -1 and end_idx != -1:
        content = content[:start_idx] + new_bottom + "\n\n    " + content[end_idx:]


# 3. Update CSS styles for the profile card and active links.
content = content.replace(
    ".profile-card { background: rgba(255,255,255,0.05); border-radius: 8px; padding: 15px; margin: 0 15px 20px 15px; display: flex; align-items: center; gap: 12px; transition: all 0.2s; border: 1px solid rgba(255,255,255,0.1); }",
    ".profile-card { padding: 15px 20px; display: flex; align-items: center; gap: 12px; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 20px;}"
)
content = content.replace(
    ".profile-card:hover { background: rgba(255,255,255,0.1); border-color: rgba(255,255,255,0.2); }",
    ".profile-card:hover { background: rgba(255,255,255,0.02); }"
)
content = content.replace(
    ".sidebar .nav-link:hover, .sidebar .nav-link.active { background-color: rgba(255,255,255,0.05); color: #fff; border-left-color: #27a2e2; }",
    ".sidebar .nav-link:hover, .sidebar .nav-link.active { background-color: rgba(255,255,255,0.05); color: #fff; border-left-color: #102d5c; }"
)


with open('templates/sdp_arsiv.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated sdp_arsiv.html perfectly.")
