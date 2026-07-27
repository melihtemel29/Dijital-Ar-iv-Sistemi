import re

# Update index.html
with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

index_pattern = re.compile(r'(<select class="form-select form-select-sm" name="ait_oldugu_yil" required>).*?(</select>)', re.DOTALL)
new_index = r"""\1
                                              {% for yil in range(2030, 2014, -1) %}
                                              <option value="{{ yil }}" {% if aktif_donem == yil|string %}selected{% endif %}>{{ yil }}</option>
                                              {% endfor %}
                                          \2"""
content = index_pattern.sub(new_index, content)
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Update sdp_arsiv.html
with open('templates/sdp_arsiv.html', 'r', encoding='utf-8') as f:
    content = f.read()

sdp_pattern = re.compile(r'(<select class="form-select form-select-lg" name="ait_oldugu_yil" required>).*?(</select>)', re.DOTALL)
new_sdp = r"""\1
                                  {% for yil in range(2030, 2014, -1) %}
                                  <option value="{{ yil }}" {% if aktif_donem == yil|string %}selected{% endif %}>{{ yil }}</option>
                                  {% endfor %}
                              \2"""
content = sdp_pattern.sub(new_sdp, content)
with open('templates/sdp_arsiv.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Update dashboard.html
with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

dash_pattern = re.compile(r'(<ul class="dropdown-menu dropdown-menu-end shadow-sm border-0" style="min-width: 100px;">).*?(</ul>)', re.DOTALL)
new_dash = r"""\1
                                          {% for yil in range(2030, 2014, -1) %}
                                          <li><a class="dropdown-item {% if aktif_donem == yil|string %}active{% endif %}" href="/set_donem/{{ yil }}">{{ yil }}</a></li>
                                          {% endfor %}
                                      \2"""
content = dash_pattern.sub(new_dash, content)
with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Dynamic year loops added")
