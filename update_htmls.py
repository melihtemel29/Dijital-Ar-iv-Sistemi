import glob

files = glob.glob('templates/*.html')

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Change object-fit: cover; to object-fit: cover; object-position: top;
    old_img = 'style="width: 100%; height: 100%; object-fit: cover;"'
    new_img = 'style="width: 100%; height: 100%; object-fit: cover; object-position: top;"'
    
    if old_img in content:
        content = content.replace(old_img, new_img)
        
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("HTML files updated.")
