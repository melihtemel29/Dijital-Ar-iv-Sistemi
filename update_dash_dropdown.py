import re

with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the bulky select tag with a Bootstrap dropdown
old_select = re.compile(r'<select class="form-select border-0 text-center fw-bold text-primary bg-transparent p-0".*?</select>', re.DOTALL)

new_dropdown = """<div class="dropdown">
                                      <button class="btn btn-sm btn-outline-primary dropdown-toggle fw-bold" type="button" data-bs-toggle="dropdown" aria-expanded="false" style="font-size: 18px; border-radius: 20px; padding: 2px 15px;">
                                          {{ aktif_donem }}
                                      </button>
                                      <ul class="dropdown-menu dropdown-menu-end shadow-sm border-0" style="min-width: 100px;">
                                          <li><a class="dropdown-item {% if aktif_donem == '2026' %}active{% endif %}" href="/set_donem/2026">2026</a></li>
                                          <li><a class="dropdown-item {% if aktif_donem == '2025' %}active{% endif %}" href="/set_donem/2025">2025</a></li>
                                          <li><a class="dropdown-item {% if aktif_donem == '2024' %}active{% endif %}" href="/set_donem/2024">2024</a></li>
                                          <li><a class="dropdown-item {% if aktif_donem == '2023' %}active{% endif %}" href="/set_donem/2023">2023</a></li>
                                      </ul>
                                  </div>"""

content = old_select.sub(new_dropdown, content)

with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("dashboard.html select replaced with dropdown")
