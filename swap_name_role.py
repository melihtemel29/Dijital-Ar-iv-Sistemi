import glob
import re

files = glob.glob('templates/*.html')

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Index.html, detay.html style
    if '<div class="profile-info text-white">' in content:
        # Swap the h6 and small
        # Currently:
        # <h6 class="m-0" style="font-size: 14px; font-weight: 600;">{{ session.get('ad_soyad', 'Personel') }}</h6>
        # <small class="text-muted" style="font-size: 12px;">{{ 'Sistem Yöneticisi' if session.get('rol') == 'admin' else 'Kullanıcı' }}</small>
        
        old_block = '''<h6 class="m-0" style="font-size: 14px; font-weight: 600;">{{ session.get('ad_soyad', 'Personel') }}</h6>
                <small class="text-muted" style="font-size: 12px;">{{ 'Sistem Yöneticisi' if session.get('rol') == 'admin' else 'Kullanıcı' }}</small>'''
        
        new_block = '''<h6 class="m-0" style="font-size: 14px; font-weight: 600;">{{ 'Sistem Yöneticisi' if session.get('rol') == 'admin' else 'Kullanıcı' }}</h6>
                <small class="text-muted" style="font-size: 12px;">{{ session.get('ad_soyad', 'Personel') }}</small>'''
                
        if old_block in content:
            content = content.replace(old_block, new_block)
            
    # stok.html style
    elif '<div class="profile-info">' in content:
        # Currently:
        # <h6>{{ session['ad_soyad'] }}</h6>
        # <small>{{ 'Sistem Yöneticisi' if session['rol'] == 'admin' else 'Personel' }}</small>
        
        old_block2 = '''<h6>{{ session['ad_soyad'] }}</h6>
                <small>{{ 'Sistem Yöneticisi' if session['rol'] == 'admin' else 'Personel' }}</small>'''
                
        new_block2 = '''<h6>{{ 'Sistem Yöneticisi' if session.get('rol') == 'admin' else 'Kullanıcı' }}</h6>
                <small>{{ session.get('ad_soyad', 'Personel') }}</small>'''
                
        if old_block2 in content:
            content = content.replace(old_block2, new_block2)
            
    # admin.html style
    elif '<h6>{{ session.get(\'ad_soyad\') }}</h6>' in content:
        old_block3 = '''<h6>{{ session.get('ad_soyad') }}</h6>
                <small>{{ 'Sistem Yöneticisi' if session.get('rol') == 'admin' else 'Kullanıcı' }}</small>'''
        new_block3 = '''<h6>{{ 'Sistem Yöneticisi' if session.get('rol') == 'admin' else 'Kullanıcı' }}</h6>
                <small>{{ session.get('ad_soyad', 'Personel') }}</small>'''
        if old_block3 in content:
            content = content.replace(old_block3, new_block3)
            

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Swapped name and role in all templates.")
