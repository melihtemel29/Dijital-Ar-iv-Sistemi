import re

with open('templates/sdp_arsiv.html', 'r', encoding='utf-8') as f:
    content = f.read()

year_block = """
                          <div class="mb-3">
                              <label class="form-label fw-bold small text-muted uppercase">Evrakın Ait Olduğu Yıl *</label>
                              <select class="form-select form-select-lg" name="ait_oldugu_yil" required>
                                  <option value="2026" {% if aktif_donem == '2026' %}selected{% endif %}>2026</option>
                                  <option value="2025" {% if aktif_donem == '2025' %}selected{% endif %}>2025</option>
                                  <option value="2024" {% if aktif_donem == '2024' %}selected{% endif %}>2024</option>
                                  <option value="2023" {% if aktif_donem == '2023' %}selected{% endif %}>2023</option>
                              </select>
                          </div>
"""

# Find the Dosya Yükle div and insert year_block before it
target = r'(<div class="mb-2">\s*<label class="form-label fw-bold small text-muted uppercase">Dosya)'
content = re.sub(target, year_block + r'\n                          \1', content)

with open('templates/sdp_arsiv.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("sdp_arsiv.html form updated")
