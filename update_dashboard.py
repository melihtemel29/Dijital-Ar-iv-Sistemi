import re

with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace hardcoded 27 with {{ eksik_sayisi }}
content = re.sub(r'<div class="stat-value">27</div>\s*<div class="stat-label">Eksik Evraklı</div>', '<div class="stat-value">{{ eksik_sayisi }}</div>\n                            <div class="stat-label">Eksik Evraklı</div>', content)

with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('templates/dashboard.html updated')
