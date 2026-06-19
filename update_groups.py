import os, re

filepath = r'c:\Users\MELİH TEMEL\Desktop\BİDB_ARSİV\templates\index.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r'<p class="nav-heading">Arşiv Grupları</p>.*?<a onclick="filtreleGrup\(\'C\', this\)" class="nav-link"><i class="bi bi-cpu"></i> C Grubu:.*?</a>', re.DOTALL | re.IGNORECASE)

new_html = """<p class="nav-heading">Arşiv Bölümleri (SDP)</p>
        <a onclick="filtreleGrup('HEPSİ', this)" class="nav-link active"><i class="bi bi-grid-fill"></i> Tüm Klasörler</a>
        <a onclick="filtreleGrup('1', this)" class="nav-link"><i class="bi bi-building"></i> 1. Bölüm: Genel ve İdari</a>
        <a onclick="filtreleGrup('2', this)" class="nav-link"><i class="bi bi-person-lines-fill"></i> 2. Bölüm: Personel ve Özlük</a>
        <a onclick="filtreleGrup('3', this)" class="nav-link"><i class="bi bi-cash-coin"></i> 3. Bölüm: Mali İşler</a>
        <a onclick="filtreleGrup('4', this)" class="nav-link"><i class="bi bi-cpu"></i> 4. Bölüm: Bilgi Teknolojileri</a>
        <a onclick="filtreleGrup('5', this)" class="nav-link"><i class="bi bi-shield-check"></i> 5. Bölüm: Hukuk ve Soruşturma</a>"""

content = pattern.sub(new_html, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('UI Groups updated.')
