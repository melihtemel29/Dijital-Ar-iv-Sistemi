import glob
import re

# 1. Clean up stok.html
with open('templates/stok.html', 'r', encoding='utf-8') as f:
    stok_content = f.read()

# Remove inline variables
stok_content = stok_content.replace(' style="color: var(--label-color) !important;"', '')
stok_content = stok_content.replace(' style="color: var(--muted-color) !important;"', '')

# Remove root variables
vars_pattern = re.compile(r'--label-color: #212529;\s*--muted-color: #6c757d;')
stok_content = vars_pattern.sub('', stok_content)

with open('templates/stok.html', 'w', encoding='utf-8') as f:
    f.write(stok_content)

# 2. Inject Dark Mode Switch and CSS/JS into all HTMLs
files = glob.glob('templates/*.html')

css_link = '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'theme.css\') }}?v=2.0">'
js_link = '<script src="{{ url_for(\'static\', filename=\'theme.js\') }}"></script>'

switch_html = '''
                <!-- Tema Geçiş Düğmesi -->
                <div class="theme-switch-wrapper mt-3 text-center">
                    <label class="theme-switch" for="checkbox">
                        <input type="checkbox" id="checkbox" />
                        <div class="slider round">
                            <i class="bi bi-moon-fill ms-1" style="line-height:28px;"></i>
                            <i class="bi bi-sun-fill me-1" style="line-height:28px;"></i>
                        </div>
                    </label>
                </div>'''

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already injected
    if 'theme.css' in content:
        continue

    # Inject CSS before </head>
    content = content.replace('</head>', f'    {css_link}\n</head>')

    # Inject JS before </body>
    content = content.replace('</body>', f'    {js_link}\n</body>')

    # Inject Theme Switch after logout button
    logout_pattern = re.compile(r'(<a href="\{\{ url_for\(\'logout\'\) \}\}".*?</a>)', re.DOTALL)
    if logout_pattern.search(content):
        content = logout_pattern.sub(r'\1' + switch_html, content)
        
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Dark mode fully restored and cleaned up.")
