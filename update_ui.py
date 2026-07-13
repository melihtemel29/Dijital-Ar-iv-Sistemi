import os
import glob

html_files = glob.glob('templates/*.html')
media_query = """
        @media (max-width: 768px) {
            .sidebar { width: 100%; position: relative; min-height: auto; padding-bottom: 20px; }
            .main-content { margin-left: 0; }
            .top-navbar { flex-direction: column; text-align: center; gap: 10px; }
            .folder-list-panel, .file-list-panel { width: 100% !important; margin-bottom: 20px; }
            .row { flex-direction: column; }
            .col-md-3, .col-md-9, .col-md-4, .col-md-8 { width: 100% !important; }
        }
    </style>"""

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '@media (max-width: 768px)' not in content:
        # replace the first occurrence of </style>
        content = content.replace('</style>', media_query, 1)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file}")
