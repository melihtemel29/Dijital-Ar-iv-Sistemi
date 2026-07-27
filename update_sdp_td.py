import re

with open('templates/sdp_arsiv.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add the <td> for Yıl after Yükleyen column and before Tarih column
target_td = r"(<div class=\"fw-semibold\">\{\{\s*evrak\.ad_soyad\s*\}\}</div>\s*<div class=\"small text-muted\">\{\{\s*evrak\.departman\s*\}\}</div>\s*</td>)"
replacement = r"\1\n                                      <td>\n                                          <span class=\"badge bg-secondary\">{{ evrak.ait_oldugu_yil }}</span>\n                                      </td>"

content = re.sub(target_td, replacement, content)

with open('templates/sdp_arsiv.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("sdp_arsiv.html table updated")
