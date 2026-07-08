import os
import glob

files = glob.glob('templates/*.html')

for file in files:
    if file.endswith('stok.html'):
        continue
    
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check for index.html bottom style
    if '<a href="/admin" class="nav-link text-white mb-2"' in content:
        if '<a href="/stok"' not in content:
            new_link = '<a href="/stok" class="nav-link text-white mb-2" style="background: rgba(255,255,255,0.08); border-radius: 6px;"><i class="bi bi-box-seam text-info"></i> Stok Takip</a>\n            '
            content = content.replace('<a href="/admin" class="nav-link text-white mb-2"', new_link + '<a href="/admin" class="nav-link text-white mb-2"')
            
    # Check for admin.html normal style
    elif '<a class="nav-link" href="/admin"' in content or '<a href="/admin" class="nav-link' in content:
        if '/stok' not in content:
            # find the line with /admin
            lines = content.split('\n')
            new_lines = []
            for line in lines:
                if 'href="/admin"' in line or "href=\"{{ url_for('admin_panel') }}\"" in line:
                    indent = len(line) - len(line.lstrip())
                    new_lines.append(' ' * indent + '<a class="nav-link" href="/stok"><i class="bi bi-box-seam"></i> Stok & Sarf Malzeme</a>')
                new_lines.append(line)
            content = '\n'.join(new_lines)
            
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Links added.")
