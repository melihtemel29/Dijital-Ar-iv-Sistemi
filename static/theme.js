// Sayfa yüklendiğinde temayı kontrol et
document.addEventListener('DOMContentLoaded', function() {
    const toggleSwitch = document.querySelector('#checkbox');
    const currentTheme = localStorage.getItem('theme');

    // Varsayılan tema Karanlık (Dark) olacak
    if (currentTheme) {
        document.documentElement.setAttribute('data-theme', currentTheme);
        if (currentTheme === 'light') {
            if(toggleSwitch) toggleSwitch.checked = false;
        } else {
            if(toggleSwitch) toggleSwitch.checked = true;
        }
    } else {
        // İlk giriş, karanlık yap
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
        if(toggleSwitch) toggleSwitch.checked = true;
    }

    // Toggle düğmesi değiştiğinde
    if(toggleSwitch) {
        toggleSwitch.addEventListener('change', function(e) {
            if (e.target.checked) {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
            } else {
                document.documentElement.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
            }    
        });
    }
});
