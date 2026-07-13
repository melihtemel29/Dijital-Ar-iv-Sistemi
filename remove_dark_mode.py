import glob
import re

files = glob.glob('templates/*.html')

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove theme switch HTML block
    theme_switch_pattern = re.compile(r'<!-- Tema Geçiş Düğmesi -->.*?</div>\s*</div>', re.DOTALL)
    
    # Wait, the </div> matching might be tricky. Let's just match the exact string or a safe regex.
    # The block ends with </label>\n                </div>
    theme_switch_pattern = re.compile(r'\s*<!-- Tema Geçiş Düğmesi -->.*?<div class="theme-switch-wrapper.*?</label>\s*</div>', re.DOTALL)
    content = theme_switch_pattern.sub('', content)

    # Remove CSS link
    css_pattern = re.compile(r'<link rel="stylesheet" href="\{\{ url_for\(\'static\', filename=\'theme.css\'\) \}\}[^>]*>')
    content = css_pattern.sub('', content)

    # Remove JS link
    js_pattern = re.compile(r'<script src="\{\{ url_for\(\'static\', filename=\'theme.js\'\) \}\}[^>]*></script>')
    content = js_pattern.sub('', content)
    
    # Optional: clean up stok.html specific inline dark mode css
    stok_dark_css = re.compile(r'/\* Dark Mode Direct Overrides to Bypass Cache \*/.*?</style>', re.DOTALL)
    content = stok_dark_css.sub('</style>', content)

    # Remove CSS vars block
    stok_css_vars = re.compile(r'\[data-theme="dark"\]\s*\{[^\}]+\}', re.DOTALL)
    content = stok_css_vars.sub('', content)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Dark mode features removed from all templates.")
