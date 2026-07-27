import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_yukle = """    conn.commit()
    conn.close()
    flash("Evrak başarıyla arşive eklendi.")
    
    kategori = ana_kod.split('.')[0] if '.' in ana_kod else ana_kod
    return redirect(url_for('sdp_arsiv', kategori=kategori, alt_kategori=ana_kod))"""

content = re.sub(r'    conn\.commit\(\)\n    conn\.close\(\)\n    flash\("Evrak ba.*?a eklendi\."\)\n    return redirect\(url_for\(\'sdp_arsiv\'\)\)', new_yukle, content, flags=re.DOTALL)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('app.py sdp_yukle updated')
