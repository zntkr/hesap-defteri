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

REM Gereksiz kutuphaneleri dislayarak .exe boyutunu kucultme (Optimization)
set EXCLUDES=--exclude-module numpy --exclude-module pandas --exclude-module matplotlib --exclude-module PyQt5 --exclude-module PyQt6 --exclude-module PySide2 --exclude-module PySide6 --exclude-module unittest --exclude-module test --exclude-module pydoc --exclude-module lib2to3 --exclude-module xmlrpc --exclude-module http.server

python -m PyInstaller --noconfirm --onefile --windowed --icon "assets\app_icon.ico" --add-data "assets\app_icon.ico;assets" %EXCLUDES% --name "HesapDefteri" "main.py"
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