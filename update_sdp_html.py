import re

with open('templates/sdp_arsiv.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the tree generation part
old_tree = '''<div class="tree-container">
                    <div class="tree-item active" onclick="filterDocs('ALL', this)">
                        <span class="tree-code"><i class="bi bi-collection"></i></span>
                        <span>Tüm Belgeler</span>
                    </div>
                    
                    {% for group_id, group in categories.items() %}
                    <div class="tree-group mt-3">
                        <div class="tree-group-title">
                            <i class="bi bi-diagram-3-fill text-primary"></i> 
                            {{ group_id }} - {{ group.name }}
                        </div>
                        <div class="tree-group-items">
                            {% for code, name in group.codes.items() %}
                            <div class="tree-item" data-sdp="{{ code }}" onclick="filterDocs('{{ code }}', this)">
                                <span class="tree-code">{{ code }}</span>
                                <span>{{ name }}</span>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                    {% endfor %}
                </div>'''

new_tree = '''<div class="tree-container">
                    <a href="{{ url_for('sdp_arsiv') }}" class="tree-item {% if not kategori %}active{% endif %} text-decoration-none">
                        <span class="tree-code"><i class="bi bi-collection"></i></span>
                        <span>Ana Sayfa</span>
                    </a>
                    
                    {% for group_id, group in categories.items() %}
                    <div class="tree-group mt-3">
                        <div class="tree-group-title">
                            <i class="bi bi-diagram-3-fill text-primary"></i> 
                            {{ group_id }} - {{ group.name }}
                        </div>
                        <div class="tree-group-items">
                            {% for code, data in group.codes.items() %}
                            <a href="{{ url_for('sdp_arsiv', kategori=code) }}" class="tree-item {% if kategori == code %}active{% endif %} text-decoration-none" data-sdp="{{ code }}">
                                <span class="tree-code">{{ code }}</span>
                                <span>{{ data.title }}</span>
                            </a>
                            {% endfor %}
                        </div>
                    </div>
                    {% endfor %}
                </div>'''

content = content.replace(old_tree, new_tree)
content = content.replace('TǬm Belgeler', 'Tüm Belgeler')

# Replace Right Pane Content
old_right_pane = content[content.find('<div class="top-bar">') : content.find('<!-- Upload Modal -->')]

new_right_pane = '''
                {% if not kategori %}
                <div class="d-flex flex-column align-items-center justify-content-center h-100">
                    <i class="bi bi-folder-check text-muted mb-3" style="font-size: 4rem; opacity: 0.3;"></i>
                    <h5 class="text-secondary fw-bold">SDP Arşivi'ne Hoş Geldiniz</h5>
                    <p class="text-muted">Dosyalara ve kırılımlara erişmek için lütfen sol menüden bir kategori seçin.</p>
                </div>
                {% elif kategori and not alt_kategori %}
                <div class="top-bar">
                    <div>
                        <h4 class="fw-bold mb-1">{{ kategori }} - {{ secili_kategori_data.title }}</h4>
                        <p class="text-muted small mb-0">Lütfen işlem yapmak istediğiniz alt kırılımı seçin</p>
                    </div>
                </div>
                <div class="row g-3">
                    {% for sub_code, sub_title in secili_kategori_data.subcodes.items() %}
                    <div class="col-md-6 col-lg-4">
                        <a href="{{ url_for('sdp_arsiv', kategori=kategori, alt_kategori=sub_code) }}" class="card border-0 shadow-sm text-decoration-none h-100" style="transition: all 0.2s;">
                            <div class="card-body d-flex align-items-center">
                                <i class="bi bi-folder-fill text-warning fs-3 me-3"></i>
                                <div>
                                    <h6 class="mb-0 fw-bold text-dark">{{ sub_code }}</h6>
                                    <small class="text-muted">{{ sub_title }}</small>
                                </div>
                            </div>
                        </a>
                    </div>
                    {% endfor %}
                </div>
                {% else %}
                <div class="top-bar">
                    <div>
                        <h4 class="fw-bold mb-1">{{ alt_kategori }} - {{ secili_kategori_data.subcodes[alt_kategori] }}</h4>
                        <p class="text-muted small mb-0"><a href="{{ url_for('sdp_arsiv', kategori=kategori) }}" class="text-decoration-none"><i class="bi bi-arrow-left"></i> Geri Dön</a></p>
                    </div>
                    <div class="d-flex gap-3">
                        <div class="input-group" style="width: 250px;">
                            <span class="input-group-text bg-white border-end-0"><i class="bi bi-search text-muted"></i></span>
                            <input type="text" class="form-control border-start-0 ps-0" id="searchInput" placeholder="Belgelerde ara..." onkeyup="searchDocs()">
                        </div>
                        <button class="btn btn-primary fw-bold" data-bs-toggle="modal" data-bs-target="#uploadModal">
                            <i class="bi bi-cloud-arrow-up-fill me-1"></i> Yeni Evrak
                        </button>
                    </div>
                </div>
                
                <div class="data-card">
                    <div class="table-responsive">
                        <table class="table table-custom table-hover" id="docsTable">
                            <thead>
                                <tr>
                                    <th width="80">SDP</th>
                                    <th>Belge Başlığı</th>
                                    <th>Yükleyen</th>
                                    <th>Tarih</th>
                                    <th>Etiketler</th>
                                    <th width="100" class="text-end">İşlem</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for evrak in evraklar %}
                                <tr class="doc-row" data-sdp="{{ evrak.ana_sdp_kodu }}">
                                    <td>
                                        <span class="badge-sdp">{{ evrak.ana_sdp_kodu }}</span>
                                    </td>
                                    <td>
                                        <div class="fw-bold text-primary">{{ evrak.baslik }}</div>
                                        {% if evrak.aciklama %}
                                        <div class="small text-muted mt-1">{{ evrak.aciklama }}</div>
                                        {% endif %}
                                    </td>
                                    <td>
                                        <div class="fw-semibold">{{ evrak.ad_soyad }}</div>
                                        <div class="small text-muted">{{ evrak.departman }}</div>
                                    </td>
                                    <td>
                                        <div class="fw-medium">{{ evrak.yukleme_tarihi.split(' ')[0] if evrak.yukleme_tarihi else '-' }}</div>
                                    </td>
                                    <td>
                                        {% if evrak.etiketler %}
                                            {% set tags = evrak.etiketler.split(',') %}
                                            {% for tag in tags %}
                                                <span class="badge-tag">{{ tag.strip() }}</span>
                                            {% endfor %}
                                        {% else %}
                                            -
                                        {% endif %}
                                    </td>
                                    <td class="text-end">
                                        <a href="/sdp/goruntule{{ '/' + evrak.dosya_adi }}" class="btn btn-sm btn-light border text-success" title="Görüntüle" target="_blank">
                                            <i class="bi bi-eye"></i>
                                        </a>
                                        <a href="/sdp/indir{{ '/' + evrak.dosya_adi }}" class="btn btn-sm btn-light border text-primary" title="İndir">
                                            <i class="bi bi-download"></i>
                                        </a>
                                        {% if session.get('rol') == 'admin' or session.get('kullanici_id') == evrak.kullanici_id %}
                                        <a href="/sdp/sil/{{ evrak.id }}" class="btn btn-sm btn-light border text-danger" title="Sil" onclick="return confirm('Bu evrakı silmek istediğinize emin misiniz?')">
                                            <i class="bi bi-trash"></i>
                                        </a>
                                        {% endif %}
                                    </td>
                                </tr>
                                {% else %}
                                <tr id="noDataRow">
                                    <td colspan="6">
                                        <div class="empty-state">
                                            <i class="bi bi-folder-x"></i>
                                            <h5>Bu klasörde henüz belge yok</h5>
                                            <p>Yeni bir belge yüklemek için sağ üstteki "Yeni Evrak" butonunu kullanın.</p>
                                        </div>
                                    </td>
                                </tr>
                                {% endfor %}
                                
                                <tr id="noSearchRow" style="display: none;">
                                    <td colspan="6">
                                        <div class="empty-state">
                                            <i class="bi bi-search"></i>
                                            <h5>Sonuç Bulunamadı</h5>
                                            <p>Arama kriterlerinize uyan belge bulunmuyor.</p>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                {% endif %}
                
'''

content = content.replace(old_right_pane, new_right_pane)

# Update Modal
old_modal_body = content[content.find('<div class="modal-body p-4">') : content.find('<div class="modal-footer bg-light border-top-0">')]

new_modal_body = '''<div class="modal-body p-4">
                        {% if alt_kategori %}
                        <input type="hidden" name="ana_sdp_kodu" value="{{ alt_kategori }}">
                        
                        <div class="alert alert-info border-0 shadow-sm mb-4">
                            <strong><i class="bi bi-info-circle-fill me-2"></i>Seçili Klasör:</strong> 
                            {{ alt_kategori }} - {{ secili_kategori_data.subcodes[alt_kategori] }}
                        </div>
                        {% endif %}

                        <div class="mb-4">
                            <label class="form-label fw-bold small text-muted uppercase">Belge Başlığı / Konusu *</label>
                            <input type="text" name="baslik" class="form-control form-control-lg" placeholder="Belgenin kısa özetini yazın" required>
                        </div>
                        
                        <div class="mb-4">
                            <label class="form-label fw-bold small text-muted uppercase">Anahtar Kelimeler / Etiketler</label>
                            <input type="text" name="etiketler" class="form-control" placeholder="Virgülle ayırarak yazın (Örn: ihale, 2026, teknik şartname)">
                        </div>
                        
                        <div class="mb-4">
                            <label class="form-label fw-bold small text-muted uppercase">Detaylı Açıklama</label>
                            <textarea name="aciklama" class="form-control" rows="2" placeholder="Belge hakkında eklemek istediğiniz notlar..."></textarea>
                        </div>
                        
                        <div class="mb-2">
                            <label class="form-label fw-bold small text-muted uppercase">Dosya Yükle *</label>
                            <input type="file" name="dosya" class="form-control form-control-lg" required>
                            <div class="form-text">PDF, DOCX, XLSX veya Resim dosyaları desteklenir.</div>
                        </div>
                        
                    </div>
                    '''
content = content.replace(old_modal_body, new_modal_body)

# Fix Javascript filterDocs to just client-side filtering of existing rows
content = re.sub(r'function filterDocs\(sdpCode, element\) \{.*?\}', '', content, flags=re.DOTALL)
content = content.replace('onkeyup="searchDocs()"', 'onkeyup="searchDocsNew()"')

new_js = '''
        function searchDocsNew() {
            const query = document.getElementById('searchInput').value.toLowerCase();
            const rows = document.querySelectorAll('.doc-row');
            let visibleCount = 0;
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(query)) {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            });
            
            checkEmptyStates(visibleCount, query.length > 0);
        }
'''
content = content.replace('function searchDocs() {', new_js + '\n        function searchDocsOld() {')


with open('templates/sdp_arsiv.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('templates/sdp_arsiv.html updated')
