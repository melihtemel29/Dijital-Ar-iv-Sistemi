import glob

files = glob.glob('templates/*.html')

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add version to theme.css to bust cache
    if "filename='theme.css') }}\"" in content:
        content = content.replace("filename='theme.css') }}\"", "filename='theme.css') }}?v=1.1\"")
        
    # Or if already has v=... we can just update it
    # For now, replacing the exact match.

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Added version string to theme.css in all templates to bust browser cache.")
