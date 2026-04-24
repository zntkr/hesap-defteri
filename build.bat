@echo off
echo =======================================================
echo   HESAP DEFTERI - DERLEME VE INSA ARACI (BUILD TOOL)
echo =======================================================
echo.
echo [*] Sistem gereksinimleri denetleniyor...
echo.

echo [1/2] Bagimliliklar (PyInstaller) kontrol ediliyor...
python -m pip install "pyinstaller>=6.0.0" --quiet
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] KRITIK HATA: PyInstaller yuklenemedi. 
    echo     Lutfen Python'un sisteme kurulu oldugundan ve 
    echo     internet baglantinizdan emin olun.
    pause
    exit /b %ERRORLEVEL%
)
echo [+] Bagimliliklar saglandi.
echo.

echo [2/2] Calistirilabilir dosya (.exe) derleniyor...
echo     Bu islem bilgisayarinizin hizina bagli olarak 1-2 dakika surebilir.
python -m PyInstaller --noconfirm --onefile --windowed --icon "app_icon.ico" --name "HesapDefteri" "main.py"
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] KRITIK HATA: Derleme islemi (Build) basarisiz oldu!
    echo     Lutfen kaynak dosyalarin eksiksiz oldugundan emin olun.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo =======================================================
echo [+] ISLEM BASARILI! 
echo     HesapDefteri.exe dosyasi "dist" klasoru icerisinde 
echo     kullanima hazir sekilde olusturuldu.
echo =======================================================
echo.
pause