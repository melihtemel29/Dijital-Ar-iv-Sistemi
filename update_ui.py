import os

filepath = r'c:\Users\MELİH TEMEL\Desktop\BİDB_ARSİV\templates\index.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Breadcrumb
old_breadcrumb = '<p class="breadcrumb-text">Bilgi İşlem Daire Başkanlığı / <strong id="grup-baslik">Tüm Klasörler</strong></p>'
new_breadcrumb = '<p class="breadcrumb-text">KTÜ Rektörlüğü / Bilgi İşlem Daire Başkanlığı (Kurum Kodu: 93431525) / <strong id="grup-baslik">Tüm Klasörler</strong></p>'
content = content.replace(old_breadcrumb, new_breadcrumb)

# 2. Badges
old_badges = '<div><span class="badge bg-light text-dark border"><i class="bi bi-clock-history"></i> Aktif Dönem: 2026</span></div>'
new_badges = '''<div class="d-flex gap-2">
                <a href="#" class="badge bg-info text-dark text-decoration-none border shadow-sm px-3 py-2"><i class="bi bi-journal-bookmark-fill me-1"></i> SDP Kılavuzu Gör</a>
                <a href="#" class="badge bg-danger text-white text-decoration-none border shadow-sm px-3 py-2"><i class="bi bi-calendar-x-fill me-1"></i> İmha Dönemi Takvimi</a>
                <span class="badge bg-light text-dark border shadow-sm px-3 py-2"><i class="bi bi-clock-history me-1"></i> Aktif Dönem: 2026</span>
            </div>'''
content = content.replace(old_badges, new_badges)

# 3. Old search bar remove
old_search = '''<div class="input-group input-group-sm" style="max-width: 200px;">
                                <input type="text" id="arama-kutusu" class="form-control" placeholder="Ara...">
                                <span class="input-group-text bg-white"><i class="bi bi-search text-muted"></i></span>
                            </div>'''
new_search = '<!-- Arama çubuğu üste taşındı -->'
content = content.replace(old_search, new_search)

# 4. New search bar insert
old_container = '<div class="container-fluid p-4">\n            <div class="row">'
new_container = '''<div class="container-fluid p-4">
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card bg-white border-0 shadow-sm" style="border-radius: 12px;">
                        <div class="card-body p-2 d-flex align-items-center">
                            <i class="bi bi-search text-muted fs-5 px-3"></i>
                            <input type="text" id="arama-kutusu" class="form-control border-0 shadow-none fs-6" style="box-shadow: none;" placeholder="SDP koduna, klasör ismine veya yıla göre arama yapın...">
                            <button class="btn btn-light text-primary border-0 px-4 fw-bold" style="border-radius: 8px;"><i class="bi bi-sliders me-2"></i>Filtrele</button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">'''
content = content.replace(old_container, new_container)

# 5. Statistic cards
old_empty = '''<div class="card p-5 text-center bg-white d-flex flex-column align-items-center justify-content-center" style="min-height: 400px; border: 2px dashed #dee2e6;">
                            <i class="bi bi-folder2-open text-muted" style="font-size: 4rem;"></i>
                            <h5 class="text-secondary mt-3 fw-bold">Detay görüntüleme paneli</h5>
                            <p class="text-muted small px-4">Evrak yüklemek, mevcut belgeleri incelemek veya silmek için sol taraftaki listeden herhangi bir klasörün üzerine tıklayın.</p>
                        </div>'''
new_empty = '''<div class="row g-4">
                            <div class="col-12">
                                <div class="card border-0 shadow-sm p-4" style="border-radius: 12px; background: linear-gradient(135deg, #102d5c 0%, #1a458a 100%); color: white;">
                                    <div class="d-flex align-items-center">
                                        <div class="display-4 me-4"><i class="bi bi-folder-fill"></i></div>
                                        <div>
                                            <h6 class="text-uppercase mb-1 opacity-75" style="letter-spacing: 1px; font-size: 12px;">Toplam Klasör Sayısı</h6>
                                            <h2 class="fw-bold m-0">{{ klasorler|length }} Aktif Klasör</h2>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-12">
                                <div class="card border-0 shadow-sm p-4" style="border-radius: 12px; background: linear-gradient(135deg, #8a1538 0%, #b21c49 100%); color: white;">
                                    <div class="d-flex align-items-center">
                                        <div class="display-4 me-4"><i class="bi bi-exclamation-triangle-fill"></i></div>
                                        <div>
                                            <h6 class="text-uppercase mb-1 opacity-75" style="letter-spacing: 1px; font-size: 12px;">Eksik Belgeli Klasörler</h6>
                                            <h2 class="fw-bold m-0">{% set e = namespace(val=0) %}{% for k in klasorler %}{% if k.durum == 'Eksik Evrak' %}{% set e.val = e.val + 1 %}{% endif %}{% endfor %}{{ e.val }} Klasörde Eksik Var</h2>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-12">
                                <div class="card border-0 shadow-sm p-4" style="border-radius: 12px; background: linear-gradient(135deg, #d35400 0%, #e67e22 100%); color: white;">
                                    <div class="d-flex align-items-center">
                                        <div class="display-4 me-4"><i class="bi bi-clock-history"></i></div>
                                        <div>
                                            <h6 class="text-uppercase mb-1 opacity-75" style="letter-spacing: 1px; font-size: 12px;">Saklama Süresi Dolanlar</h6>
                                            <h2 class="fw-bold m-0">0 Klasör İşlem Bekliyor</h2>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>'''
content = content.replace(old_empty, new_empty)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("UI updated successfully.")
