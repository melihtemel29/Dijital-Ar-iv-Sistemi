import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the dictionary assignment in sdp_yukle
target = r"kategori_adi = group_val\['codes'\]\[ana_kod\]\s+break"
replacement = r"kategori_adi = group_val['codes'][ana_kod]['title']\n            break"

content = re.sub(target, replacement, content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed TypeError in sdp_yukle")
