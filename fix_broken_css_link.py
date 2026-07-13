import glob
import re

files = glob.glob('templates/*.html')

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the broken url_for and fix it.
    # It might look like: <link rel="stylesheet" href="{{ url_for('static', filename='theme.css?v=2.1') }}?v=2.0">
    # We want it to be exactly: <link rel="stylesheet" href="{{ url_for('static', filename='theme.css') }}?v=2.2">
    
    # Let's just blindly replace any href containing theme.css with the correct one
    # The whole tag is: <link rel="stylesheet" href="{{ url_for('static', filename='theme.css...
    
    pattern = re.compile(r'<link rel="stylesheet" href="\{\{ url_for\(\'static\', filename=\'theme\.css[^>]*>')
    correct_tag = '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'theme.css\') }}?v=2.2">'
    
    content = pattern.sub(correct_tag, content)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fixed broken CSS links.")
