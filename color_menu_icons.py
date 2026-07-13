import glob
import re

files = glob.glob('templates/*.html')

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Ana Sayfa Icon
    content = re.sub(r'<i class="bi bi-grid-fill(?:\s+[^"]*)?"></i>', '<i class="bi bi-grid-fill" style="color: #3498db;"></i>', content)
    
    # Klasörler Icon
    content = re.sub(r'<i class="bi bi-folder2-open(?:\s+[^"]*)?"></i>', '<i class="bi bi-folder2-open" style="color: #f39c12;"></i>', content)
    # Also handle index.html specific folder icons if any that match the menu item
    # Wait, in index.html the sidebar has SDP codes. Those can stay as they are, but the main "Klasörler" link might be bi-folder2-open.
    
    # Stok & Sarf Malzeme Icon
    content = re.sub(r'<i class="bi bi-box-seam(?:\s+[^"]*)?"></i>', '<i class="bi bi-box-seam" style="color: #2ecc71;"></i>', content)
    
    # Admin Paneli Icon
    # Note: dashboard.html uses bi-shield-lock, others might use bi-shield-lock-fill
    content = re.sub(r'<i class="bi bi-shield-lock(?:-fill)?(?:\s+[^"]*)?"></i>', '<i class="bi bi-shield-lock-fill" style="color: #e74c3c;"></i>', content)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Icons colored in all templates.")
