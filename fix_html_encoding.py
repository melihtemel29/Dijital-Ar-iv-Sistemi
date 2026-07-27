import os

file_path = os.path.join('templates', 'cop_kutusu.html')
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

try:
    # Try to decode the double-encoded UTF-8
    fixed_content = content.encode('latin1').decode('utf-8')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    print("Fixed successfully with latin1->utf8.")
except Exception as e:
    print("Failed latin1 decoding:", e)
    # Manual fallback if latin1 fails due to some weird char
    replacements = {
        'KTÃœ': 'KTÜ',
        'Ä°': 'İ',
        'ÅŸ': 'ş',
        'Ä±': 'ı',
        'Ã¶': 'ö',
        'Ã‡': 'Ç',
        'Ã¼': 'ü',
        'ÄŸ': 'ğ',
        'Ã§': 'ç',
        'Ã–': 'Ö',
        'Åž': 'Ş',
        'Äž': 'Ğ',
        'Ã¢': 'â'
    }
    for bad, good in replacements.items():
        content = content.replace(bad, good)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed via manual replacements.")
