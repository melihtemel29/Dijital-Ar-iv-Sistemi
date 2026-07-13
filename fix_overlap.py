import glob

files = glob.glob('templates/*.html')

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the overlap by changing absolute position to margin-top
    old_div = '<div style="position: absolute; bottom: 20px; width: 100%; padding: 0 15px;">'
    new_div = '<div style="margin-top: 30px; margin-bottom: 20px; width: 100%; padding: 0 15px;">'
    
    if old_div in content:
        content = content.replace(old_div, new_div)
        
    # Also make sure the sidebar is scrollable if needed
    if '.sidebar { background-color: #2c303b; min-height: 100vh; color: #fff; width: 260px; position: fixed;' in content:
        content = content.replace(
            '.sidebar { background-color: #2c303b; min-height: 100vh; color: #fff; width: 260px; position: fixed;',
            '.sidebar { background-color: #2c303b; height: 100vh; overflow-y: auto; color: #fff; width: 260px; position: fixed;'
        )

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Overlap fixed in templates.")
