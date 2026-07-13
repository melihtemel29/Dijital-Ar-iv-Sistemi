import glob
import re

files = glob.glob('templates/*.html')

new_profile_block = '''        <a href="{{ url_for('dashboard') }}" class="profile-card text-decoration-none">
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
        </a>'''

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # The profile card might start with <a href="{{ url_for('dashboard') }}" class="profile-card... or <a href="#" class="profile-card... or <div class="profile-card">
    
    # regex to match from the opening <div class="profile-card"> or <a ... class="profile-card..."> to the closing </div> or </a> that matches the end of profile-info
    # A robust regex for this specific block:
    # It starts with either <div class="profile-card"> or <a[^>]*class="profile-card[^>]*>
    # It ends with </div> or </a> immediately after the profile-info block
    
    pattern = re.compile(r'<(div|a)[^>]*class="profile-card[^>]*>.*?<div class="profile-info.*?</small>\s*</div>\s*</\1>', re.DOTALL)
    
    content = pattern.sub(new_profile_block, content)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Synchronized profile cards across all templates.")
