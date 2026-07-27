import os
import glob

def add_trash_link():
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    html_files = glob.glob(os.path.join(template_dir, '*.html'))
    
    # We want to add the Çöp Kutusu link right after SDP Arşivi
    # But only if user is admin. So we wrap it in {% if session.get('rol') == 'admin' %}
    
    trash_link_template = """
          {{% if session.get('rol') == 'admin' %}}
          <a class="nav-link {active_class}" href="{{{{ url_for('cop_kutusu') }}}}"><i class="bi bi-trash-fill" style="color: #e74c3c;"></i> Çöp Kutusu</a>
          {{% endif %}}"""

    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'Çöp Kutusu' in content and 'cop_kutusu' in content:
            continue # Already added
            
        # Find where SDP Arşivi is
        sdp_search_active = 'href="{{ url_for(\'sdp_arsiv\') }}"><i class="bi bi-file-earmark-medical-fill" style="color: #9b59b6;"></i> SDP Arşivi</a>'
        
        if sdp_search_active in content:
            is_cop_kutusu = "cop_kutusu" in file_path
            active = "active" if is_cop_kutusu else ""
            replacement = sdp_search_active + trash_link_template.format(active_class=active)
            content = content.replace(sdp_search_active, replacement)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {os.path.basename(file_path)}")

if __name__ == '__main__':
    add_trash_link()
