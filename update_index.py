import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add a button for "Boş Klasör"
if "sayac-bos" not in content:
    content = content.replace(
        '<button onclick="filtreleDurum(\'Eksik Evrak\')" class="status-filter-btn bg-danger text-white">Eksik (<span id="sayac-eksik">0</span>)</button>',
        '<button onclick="filtreleDurum(\'Eksik Evrak\')" class="status-filter-btn bg-danger text-white">Eksik (<span id="sayac-eksik">0</span>)</button>\n                              <button onclick="filtreleDurum(\'Boş Klasör\')" class="status-filter-btn bg-secondary text-white">Boş Klasör (<span id="sayac-bos">0</span>)</button>'
    )

# Add JS counter logic for Boş Klasör
if "let b = 0;" not in content:
    content = content.replace(
        "let e = 0;",
        "let e = 0;\n                let b = 0;"
    )
    content = content.replace(
        "if(durum === 'Eksik Evrak') e++;",
        "if(durum === 'Eksik Evrak') e++;\n                if(durum === 'Boş Klasör') b++;"
    )
    content = content.replace(
        "document.getElementById('sayac-eksik').innerText = e;",
        "document.getElementById('sayac-eksik').innerText = e;\n            if(document.getElementById('sayac-bos')) document.getElementById('sayac-bos').innerText = b;"
    )

# Visual for Boş Klasör
if "Boş Klasör" not in content.replace("Boş Klasör (", ""): # Check if we already added it in the loop
    # We want to add something for 'Boş Klasör'
    new_subtext = """{% if k.durum == 'Eksik Evrak' %}
                                                <div class="folder-subtext text-danger font-weight-bold">
                                                    <i class="bi bi-exclamation-triangle-fill"></i> Eksik: {% for e in k.eksikler %}{{ e }}{% if not loop.last %}, {% endif %}{% endfor %}
                                                </div>
                                            {% elif k.durum == 'Boş Klasör' %}
                                                <div class="folder-subtext text-muted">
                                                    <i class="bi bi-folder-x"></i> Evrak yok
                                                </div>
                                            {% endif %}"""
    content = re.sub(r'\{%\s*if k\.durum == \'Eksik Evrak\'\s*%\}.*?\{%\s*endif\s*%\}', new_subtext, content, flags=re.DOTALL)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('templates/index.html updated')
