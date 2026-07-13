import glob
import re

files = glob.glob('templates/*.html')

css_link = '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'theme.css\') }}?v=2.1">'
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

    # 1. Fix Logo Link
    content = content.replace(
        '<img src="{{ url_for(\'static\', filename=\'ktu_logo_new.png\') }}" alt="Kurum Logosu">',
        '<a href="{{ url_for(\'dashboard\') }}"><img src="{{ url_for(\'static\', filename=\'ktu_logo_new.png\') }}" alt="Kurum Logosu"></a>'
    )

    # 2. Fix Profile Card Link
    content = content.replace(
        '<a href="#" class="profile-card text-decoration-none">',
        '<a href="{{ url_for(\'dashboard\') }}" class="profile-card text-decoration-none">'
    )

    # 3. Add Ana Sayfa Link to sidebar if not present.
    # We will just inject it before the first nav-link if "Ana Sayfa" is not in the sidebar.
    if 'Ana Sayfa</a>' not in content:
        ana_sayfa_link = '\n        <a href="{{ url_for(\'dashboard\') }}" class="nav-link"><i class="bi bi-grid-fill" style="color: #27a2e2;"></i> Ana Sayfa</a>'
        # inject it right after the profile card </a>
        content = re.sub(r'(<a href="\{\{ url_for\(\'dashboard\'\) \}\}" class="profile-card.*?</small>\s*</div>\s*</a>)', r'\1' + ana_sayfa_link, content, flags=re.DOTALL)

    # 4. Inject Theme Switch and CSS/JS if missing
    if 'theme.css' not in content:
        content = content.replace('</head>', f'    {css_link}\n</head>')
        content = content.replace('</body>', f'    {js_link}\n</body>')

    # The logout button can be <a href="{{ url_for('logout') }}" OR <a href="/logout"
    # So we use a regex that matches either.
    if 'theme-switch-wrapper' not in content:
        logout_pattern = re.compile(r'(<a href="(?:/logout|\{\{ url_for\(\'logout\'\) \}\})".*?</a>)', re.DOTALL)
        if logout_pattern.search(content):
            content = logout_pattern.sub(r'\1' + switch_html, content)

    # Make sure we use the latest css version
    content = re.sub(r'theme\.css(\?v=[0-9\.]+)?', 'theme.css?v=2.1', content)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Links and Theme Switches fixed in all templates.")
