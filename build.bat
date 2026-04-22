@echo off
echo [Aritmetik Engine] Derleme Sureci Basliyor...
echo.

REM Eger sistemde pyinstaller yoksa kur, varsa en guncel surume yukselt:
pip install --upgrade pyinstaller

REM Eski hatali derleme artiklarini (DLL cakismalarini) oncesinde temizle:
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "AritmetikEngine.spec" del /q "AritmetikEngine.spec"

REM Sektore uygun, konsolsuz, tek dosya ve ikonlu derleme komutu:
REM --clean: PyInstaller onbellek (cache) hatalarini onler.
REM TAM KARANTİNA: İşletim sistemiyle çakışan tüm ağ, kripto ve veritabanı DLL'lerini kökünden reddediyoruz.
set EXCLUDES=--exclude-module sqlite3 --exclude-module ssl --exclude-module _ssl --exclude-module socket --exclude-module _socket --exclude-module hashlib --exclude-module _hashlib --exclude-module cryptography

pyinstaller --noconfirm --clean --onefile --windowed --icon="app_icon.ico" %EXCLUDES% --name "AritmetikEngine" main.py

echo.
echo [BASARILI] Derleme tamamlandi! 
echo "AritmetikEngine.exe" dosyasi "dist" klasoru icinde sizi bekliyor.
pause