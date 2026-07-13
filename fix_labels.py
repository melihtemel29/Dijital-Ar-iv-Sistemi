with open('templates/stok.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all <label class="form-label">
content = content.replace('<label class="form-label">', '<label class="form-label" style="color: var(--label-color) !important;">')

# Replace <small class="text-muted">
content = content.replace('<small class="text-muted">', '<small class="text-muted" style="color: var(--muted-color) !important;">')

with open('templates/stok.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected inline CSS variables to all form labels in stok.html")
