import glob
import re

files = glob.glob('templates/*.html')

css_link = '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'theme.css\') }}">'
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

    # Inject Theme Switch after logout button (if exists)
    # The logout block looks like:
    # <a href="{{ url_for('logout') }}" ...>...</a>
    # </div>
    logout_pattern = re.compile(r'(<a href="\{\{ url_for\(\'logout\'\) \}\}".*?</a>)', re.DOTALL)
    
    if logout_pattern.search(content):
        # We append the switch right after the </a> tag
        content = logout_pattern.sub(r'\1' + switch_html, content)
        
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Theme CSS/JS and switch injected into all templates.")
