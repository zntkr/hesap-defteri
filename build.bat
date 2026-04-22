@echo off
echo ==========================================
echo ZNTKR Hesaplayici Derleme Araci
echo ==========================================
echo.

echo [1/2] Gerekli paketler kontrol ediliyor...
python -m pip install "pyinstaller>=6.0.0"
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo [HATA] PyInstaller yuklenirken bir sorun olustu. Python'un yuklu oldugundan emin olun.
    pause
    exit /b %ERRORLEVEL%
)

echo [2/2] .exe dosyasi olusturuluyor lutfen bekleyin...
python -m PyInstaller --noconfirm --onefile --windowed --icon "app_icon.ico" --name "Hesaplayici" "main.py"
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo [HATA] Derleme basarisiz oldu! Lutfen yukaridaki hatalari inceleyin. Ornegin main.py eksik olabilir.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Islem basarili! Uygulamaniz "dist" klasoru icerisinde hazir.
pause