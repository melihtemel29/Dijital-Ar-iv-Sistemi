import re

with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Change dashboard.html to make the stat-card clickable to show a dropdown, or just replace the stat-card with a dropdown.
# Or, even better, put a dropdown right in the stat-card that redirects on change.
dropdown_html = """<div class="stat-value">
                                <select class="form-select border-0 text-center fw-bold text-primary bg-transparent p-0" style="font-size: 32px; box-shadow: none; cursor: pointer;" onchange="window.location.href='/set_donem/' + this.value;">
                                    <option value="2026" {% if aktif_donem == '2026' %}selected{% endif %}>2026</option>
                                    <option value="2025" {% if aktif_donem == '2025' %}selected{% endif %}>2025</option>
                                    <option value="2024" {% if aktif_donem == '2024' %}selected{% endif %}>2024</option>
                                    <option value="2023" {% if aktif_donem == '2023' %}selected{% endif %}>2023</option>
                                </select>
                            </div>"""

content = re.sub(r'<div class="stat-value">\{\{\s*aktif_donem\s*\}\}</div>', dropdown_html, content)

with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("dashboard.html updated.")
