import tkinter as tk
import os
import sys
from ui.arayuz_tasarimi import MainUI

def get_resource_path(relative_path: str) -> str:
    """PyInstaller --onefile ile derlendiğinde geçici klasördeki dosyaları bulur."""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

def _apply_square_corners(root: tk.Tk) -> None:
    """
    Windows 11'in DWM yuvarlak köşe efektini devre dışı bırakır.
    Eski Windows sürümlerinde sessizce başarısız olur.
    """
    try:
        import ctypes
        DWMWA_WINDOW_CORNER_PREFERENCE = 33
        DONOTROUND = ctypes.c_int(1)
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_WINDOW_CORNER_PREFERENCE,
            ctypes.byref(DONOTROUND),
            ctypes.sizeof(DONOTROUND),
        )
    except Exception:
        pass

if __name__ == "__main__":
    # Yüksek çözünürlüklü ekranlarda (High-DPI) ikon ve arayüz bulanıklığını önler
    try:
        import ctypes
        # Temel DPI Farkındalığı (Aşırı mühendislikten arındırılmış, en stabil Tkinter standardı)
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    root = tk.Tk()

    # 1. PERDEYİ KAPAT: Arayüz çizilirken ekranda titreme (flicker) olmaması için pencereyi gizle
    root.withdraw()

    icon_path = get_resource_path("app_icon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)

    # 2. DEKORU KUR: Arayüzü oluştur
    app = MainUI(root)

    # 3. PENCERE AYARLARI: Boyutlandırmayı kilitle ve işletim sisteminin çizimleri bitirmesini bekle
    root.resizable(False, False)
    root.update_idletasks()

    # 4. GEOMETRİ HESABI: Uygulamayı ekranın tam ortasına hizala
    sf = root.winfo_fpixels('1i') / 96.0
    genislik = int(400 * sf)
    yukseklik = int(560 * sf)
    x = (root.winfo_screenwidth() // 2) - (genislik // 2)
    y = (root.winfo_screenheight() // 2) - (yukseklik // 2)
    root.geometry(f"{genislik}x{yukseklik}+{x}+{y}")

    _apply_square_corners(root)

    # 5. PERDEYİ AÇ: Kusursuz bir şekilde ekranda göster
    root.deiconify()

    root.mainloop()