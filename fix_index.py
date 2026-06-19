import os, re

filepath = r'c:\Users\MELİH TEMEL\Desktop\BİDB_ARSİV\templates\index.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace profile card
old_profile = """        <div class="profile-card">
            <div class="profile-img"><i class="bi bi-person-fill"></i></div>
            <div class="profile-info">
                <h6>Melih Temel</h6>
                <small>Birim Sorumlusu</small>
            </div>
        </div>"""
new_profile = """        <div class="profile-card">
            <div class="profile-img"><i class="bi bi-person-fill"></i></div>
            <div class="profile-info text-white">
                <h6 class="m-0" style="font-size: 14px; font-weight: 600;">{{ session.get('ad_soyad', 'Personel') }}</h6>
                <small style="color: #a2a5b9; font-size: 11px;">
                    {% if session.get('rol') == 'admin' %}Sistem Yöneticisi{% else %}Personel{% endif %}
                </small>
            </div>
        </div>"""

if old_profile in content:
    content = content.replace(old_profile, new_profile)
else:
    print('Warning: old_profile not found')

# 2. Add admin/logout
old_sidebar_end = """C Grubu: Hizmet alımı</a>
    </div>"""
new_sidebar_end = """C Grubu: Hizmet alımı</a>
        
        <div style="position: absolute; bottom: 20px; width: 100%;">
            {% if session.get('rol') == 'admin' %}
            <a href="/admin" class="nav-link text-primary"><i class="bi bi-shield-lock-fill"></i> Admin Paneli</a>
            {% endif %}
            <a href="/logout" class="nav-link text-danger"><i class="bi bi-box-arrow-left"></i> Çıkış Yap</a>
        </div>
    </div>"""

# Try matching with alımı
if old_sidebar_end in content:
    content = content.replace(old_sidebar_end, new_sidebar_end)
else:
    # Try Alımı
    old_sidebar_end2 = """C Grubu: Hizmet Alımı</a>
    </div>"""
    new_sidebar_end2 = """C Grubu: Hizmet Alımı</a>
        
        <div style="position: absolute; bottom: 20px; width: 100%;">
            {% if session.get('rol') == 'admin' %}
            <a href="/admin" class="nav-link text-primary"><i class="bi bi-shield-lock-fill"></i> Admin Paneli</a>
            {% endif %}
            <a href="/logout" class="nav-link text-danger"><i class="bi bi-box-arrow-left"></i> Çıkış Yap</a>
        </div>
    </div>"""
    if old_sidebar_end2 in content:
        content = content.replace(old_sidebar_end2, new_sidebar_end2)
    else:
        print('Warning: old_sidebar_end not found')

# 3. Replace folder loop
pattern = re.compile(r'{%\s*for k in klasorler\s*%}.*?{%\s*endfor\s*%}', re.DOTALL)
new_loop = """{% for k in klasorler %}
                                <a href="/klasor/{{ k.id }}" class="folder-row {% if secili_klasor and secili_klasor.id == k.id %}active-folder{% endif %}" data-grup="{{ k.grup }}" data-durum="{{ k.durum }}">
                                    <div class="d-flex align-items-center">
                                        <div class="folder-num">{{ loop.index }})</div>
                                        <div>
                                            <div class="folder-title">({{ k.id }}) {{ k.ad }}</div>
                                            {% if k.durum == 'Eksik Evrak' %}
                                                <div class="folder-subtext text-danger font-weight-bold">
                                                    <i class="bi bi-exclamation-triangle-fill"></i> Eksik: {% for e in k.eksikler %}{{ e }}{% if not loop.last %}, {% endif %}{% endfor %}
                                                </div>
                                            {% endif %}
                                        </div>
                                    </div>
                                    {% if k.durum == 'Tamamlandı' %}
                                        <span class="badge bg-primary rounded-pill"><i class="bi bi-check-lg"></i></span>
                                    {% else %}
                                        <span class="badge bg-danger rounded-pill"><i class="bi bi-x-lg"></i></span>
                                    {% endif %}
                                </a>
                            {% endfor %}"""

content = pattern.sub(new_loop, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated index.html successfully')
