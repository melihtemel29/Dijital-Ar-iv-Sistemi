import re

with open('templates/sdp_arsiv.html', 'r', encoding='utf-8') as f:
    content = f.read()

year_select = """
                            <div class="mb-3">
                                <label class="form-label text-dark fw-bold">Evrakın Ait Olduğu Yıl</label>
                                <select class="form-select" name="ait_oldugu_yil" required>
                                    <option value="2026" {% if aktif_donem == '2026' %}selected{% endif %}>2026</option>
                                    <option value="2025" {% if aktif_donem == '2025' %}selected{% endif %}>2025</option>
                                    <option value="2024" {% if aktif_donem == '2024' %}selected{% endif %}>2024</option>
                                    <option value="2023" {% if aktif_donem == '2023' %}selected{% endif %}>2023</option>
                                </select>
                            </div>
"""

# Insert year_select in the modal form, before file input
content = re.sub(r'(<div class="mb-3">\s*<label class="form-label text-dark fw-bold">Dosya Seçin</label>)', year_select + r'\1', content)

# Add "Yıl" to table headers
content = re.sub(r'<th>Tarih</th>', r'<th>Yıl</th>\n                                      <th>Tarih</th>', content)

# Add e.ait_oldugu_yil to table body
content = re.sub(r'<td>\{\{\s*e\.yukleme_tarihi.*?\}\}</td>', r'<td><span class="badge bg-secondary">{{ e.ait_oldugu_yil }}</span></td>\n                                          <td>{{ e.yukleme_tarihi.split()[0] if e.yukleme_tarihi else "" }}</td>', content)

with open('templates/sdp_arsiv.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("sdp_arsiv.html updated.")
