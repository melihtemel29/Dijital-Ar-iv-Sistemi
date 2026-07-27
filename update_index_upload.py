import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

year_col = """                                      <div class="col-md-4">
                                          <label class="form-label small text-muted fw-bold">Yıl</label>
                                          <select class="form-select form-select-sm" name="ait_oldugu_yil" required>
                                              <option value="2026" {% if aktif_donem == '2026' %}selected{% endif %}>2026</option>
                                              <option value="2025" {% if aktif_donem == '2025' %}selected{% endif %}>2025</option>
                                              <option value="2024" {% if aktif_donem == '2024' %}selected{% endif %}>2024</option>
                                              <option value="2023" {% if aktif_donem == '2023' %}selected{% endif %}>2023</option>
                                          </select>
                                      </div>
"""

# Find the row g-2 inside the form
# We will change col-md-6 to col-md-4, and append the year column
content = content.replace('class="col-md-6"', 'class="col-md-4"')

# We will inject year_col before `<div class="col-md-4"> \n <label class="form-label small text-muted fw-bold">Dosya Seç</label>`
content = re.sub(r'(<div class="col-md-4">\s*<label class="form-label small text-muted fw-bold">Dosya)', year_col + r'\1', content)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("index.html year select updated.")
