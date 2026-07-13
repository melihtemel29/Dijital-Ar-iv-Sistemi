@echo off
color 0A
echo ====================================================
echo      DIJITAL ARSIV SISTEMI - INTERNET BAGLANTISI
echo ====================================================
echo.
echo Bu islem projenizi "https://....ngrok.app" seklinde gecici bir
echo genel link uzerinden internete acar.
echo.
echo UYARI: Arka planda Flask uygulamanizin (python app.py) 
echo calisiyor (5000 portunda) oldugundan emin olun!
echo.
set /p TOKEN="Ngrok Authtoken'inizi girin (Eger daha once girdiyseniz bos birakip ENTER'a basin): "

if not "%TOKEN%"=="" (
    ngrok.exe config add-authtoken %TOKEN%
    echo Token basariyla kaydedildi!
)

echo.
echo Baglanti baslatiliyor... Lutfen bekleyin...
echo (Acilan siyah ekrandaki "Forwarding" karsisinda yazan link sizin adresinizdir!)
echo.
ngrok.exe http 5000
pause
