@echo off
echo ==========================================
echo ZNTKR Hesaplayici Derleme Araci
echo ==========================================
echo.

echo [1/2] Gerekli paketler kontrol ediliyor...
python -m pip install pyinstaller>=6.0.0

echo [2/2] .exe dosyasi olusturuluyor lutfen bekleyin...
python -m pyinstaller --noconfirm --onefile --windowed --icon "app_icon.ico" --name "Hesaplayici" "main.py"

echo.
echo Islem basarili! Uygulamaniz "dist" klasoru icerisinde hazir.
pause