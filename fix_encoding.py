import codecs
import re

with open('app.py', 'rb') as f:
    content = f.read()

# Let's decode properly.
# The original file is UTF-8. The part appended at the end is probably Windows-1254 (Turkish).
# We can find the exact point where it was appended.
separator = b'@app.route(\'/klasor/sil/<path:klasor_id>\', methods=[\'POST\'])'

if separator in content:
    parts = content.split(separator)
    # The first part is UTF-8
    part1 = parts[0].decode('utf-8')
    # The second part is Windows-1254
    part2 = separator.decode('utf-8') + parts[1].decode('cp1254')
    
    final_content = part1 + part2
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(final_content)
    print("app.py encoding fixed")
else:
    print("Separator not found, decoding the whole file as utf-8 replacing errors")
    final_content = content.decode('utf-8', errors='replace')
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(final_content)

