with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace redirect(url_for('ana_sayfa')) with redirect(url_for('dashboard')) in the login and decorator sections
# We'll just replace the specific occurrences.

# 1. Login success redirect
login_block = "session['rol'] = user['rol']\n            return redirect(url_for('ana_sayfa'))"
new_login_block = "session['rol'] = user['rol']\n            return redirect(url_for('dashboard'))"
content = content.replace(login_block, new_login_block)

# 2. admin_required redirect
admin_block = "flash(\"Bu sayfaya erişim yetkiniz yok.\")\n            return redirect(url_for('ana_sayfa'))"
new_admin_block = "flash(\"Bu sayfaya erişim yetkiniz yok.\")\n            return redirect(url_for('dashboard'))"
content = content.replace(admin_block, new_admin_block)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Redirects updated to point to the new dashboard.")
