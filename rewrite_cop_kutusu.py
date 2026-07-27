import os
import re

file_path = os.path.join(os.path.dirname(__file__), 'templates', 'cop_kutusu.html')
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace breadcrumb
content = content.replace(
    '<p class="breadcrumb-text">KTÜ Rektörlüğü / Bilgi İşlem Daire Başkanlığı (Kurum Kodu: 93431525) / <strong id="grup-baslik">Tüm Klasörler</strong></p>',
    '<p class="breadcrumb-text">KTÜ Rektörlüğü / Bilgi İşlem Daire Başkanlığı / <strong id="grup-baslik">Çöp Kutusu</strong></p>'
)

# Change title
content = content.replace('KTÜ | Dijital Arşiv Sistemi', 'Çöp Kutusu | Dijital Arşiv Sistemi')
content = content.replace('<h5 class="m-0 fw-bold text-dark">Klasör listesi</h5>', '<h5 class="m-0 fw-bold text-danger"><i class="bi bi-trash-fill"></i> Çöp Kutusu (Silinmiş Klasörler)</h5>')

# The folder loop in cop_kutusu
loop_start = content.find('{% for k in klasorler %}')
loop_end = content.find('{% endfor %}', loop_start) + len('{% endfor %}')

new_loop = """{% for k in klasorler %}
<div class="folder-row d-flex justify-content-between align-items-center" data-grup="{{ k.grup }}" data-durum="{{ k.durum }}">
    <div class="d-flex align-items-center flex-grow-1">
        <div class="folder-num">{{ loop.index }})</div>
        <div>
            <div class="folder-title text-muted">({{ k.id }}) {{ k.ad }}</div>
            <div class="folder-subtext text-secondary">
                <i class="bi bi-clock-history"></i> Çöp Kutusunda
            </div>
        </div>
    </div>
    <div class="d-flex align-items-center gap-2">
        {% if session.get('rol') == 'admin' %}
        <form action="{{ url_for('klasor_kurtar', klasor_id=k.id) }}" method="post" class="m-0 p-0">
            <button type="submit" class="btn btn-sm btn-success p-1 px-2 text-white fw-bold shadow-sm" title="Kurtar">
                <i class="bi bi-arrow-counterclockwise"></i> Kurtar
            </button>
        </form>
        <form action="{{ url_for('klasor_kalici_sil', klasor_id=k.id) }}" method="post" class="m-0 p-0" onsubmit="return confirm('Bu klasörü ve içindeki TÜM EVRAKLARI kalıcı olarak silmek istiyor musunuz? Bu işlem GERİ ALINAMAZ!');">
            <button type="submit" class="btn btn-sm btn-danger p-1 px-2 text-white fw-bold shadow-sm" title="Kalıcı Sil">
                <i class="bi bi-trash-fill"></i> Kalıcı Sil
            </button>
        </form>
        {% endif %}
    </div>
</div>
{% else %}
<div class="text-center py-5">
    <i class="bi bi-emoji-smile text-muted" style="font-size: 3rem;"></i>
    <h5 class="text-muted mt-3">Çöp kutusu boş</h5>
</div>
{% endfor %}"""

content = content[:loop_start] + new_loop + content[loop_end:]

# Remove the right column completely (col-md-6)
# It starts with `<div class="col-md-6">` and ends before `</div> <!-- end of row -->`
# Wait, it's safer to just regex it
content = re.sub(r'<div class="col-md-6">.*?<!-- Modal: Evrak', '<!-- Modal: Evrak', content, flags=re.DOTALL)

# Adjust col-md-6 to col-md-12 for the left column
content = content.replace('<div class="col-md-6">', '<div class="col-md-12">', 1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("cop_kutusu.html updated.")
