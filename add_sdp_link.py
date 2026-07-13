import glob

files = glob.glob('templates/*.html')
link_html = '            <a class="nav-link" href="{{ url_for(\'sdp_arsiv\') }}"><i class="bi bi-file-earmark-medical-fill" style="color: #9b59b6;"></i> SDP Arşivi</a>\n'

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find where Ana Sayfa or Klasörler is and insert the SDP link.
    if "{{ url_for('sdp_arsiv') }}" not in content:
        if "Klasörler</a>" in content:
            parts = content.split("Klasörler</a>")
            new_content = parts[0] + "Klasörler</a>\n" + link_html + parts[1]
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_content)
        elif "Arşive Dön</a>" in content:
            parts = content.split("Arşive Dön</a>")
            new_content = parts[0] + "Arşive Dön</a>\n" + link_html + parts[1]
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_content)
