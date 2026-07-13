with open('static/theme.css', 'a', encoding='utf-8') as f:
    f.write("""
/* Genel Metin Renkleri Dark Mode Fix */
[data-theme="dark"] label,
[data-theme="dark"] .form-label { color: #e9ecef !important; }
[data-theme="dark"] .text-muted, [data-theme="dark"] small.text-muted { color: #a2a5b9 !important; }
[data-theme="dark"] .text-primary { color: #27a2e2 !important; }
[data-theme="dark"] .text-dark { color: #e9ecef !important; }
[data-theme="dark"] h1, [data-theme="dark"] h2, [data-theme="dark"] h3, [data-theme="dark"] h4, [data-theme="dark"] h5, [data-theme="dark"] h6 { color: #fff !important; }
[data-theme="dark"] strong, [data-theme="dark"] b { color: #fff !important; }

/* Select2 Dark Mode Fixes */
[data-theme="dark"] .select2-container--default .select2-selection--single { background-color: #121418 !important; border-color: #2c303b !important; }
[data-theme="dark"] .select2-container--default .select2-selection--single .select2-selection__rendered { color: #e9ecef !important; }
[data-theme="dark"] .select2-dropdown { background-color: #1a1d24 !important; border-color: #2c303b !important; color: #e9ecef !important; }
[data-theme="dark"] .select2-search--dropdown .select2-search__field { background-color: #121418 !important; border-color: #2c303b !important; color: #e9ecef !important; }
[data-theme="dark"] .select2-container--default .select2-results__option--selected { background-color: #2c303b !important; color: #fff !important; }
[data-theme="dark"] .select2-container--default .select2-results__option--highlighted.select2-results__option--selectable { background-color: #27a2e2 !important; color: #fff !important; }
[data-theme="dark"] .select2-results__option { color: #e9ecef; }
""")

print("theme.css updated with lighter text colors and Select2 support for dark mode.")
