import tkinter as tk
import os
import sys
from ui.arayuz_tasarimi import MainUI

def get_resource_path(relative_path: str) -> str:
    """PyInstaller --onefile ile derlendiğinde geçici klasördeki dosyaları bulur."""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

def _fade_in(root: tk.Tk, duration_ms: int = 200, steps: int = 10) -> None:
    try:
        step_ms = max(1, duration_ms // steps)
        delta = 1.0 / steps

        def _tick(alpha: float) -> None:
            nxt = min(alpha + delta, 1.0)
            root.attributes('-alpha', nxt)
            if nxt < 1.0:
                root.after(step_ms, lambda: _tick(nxt))

        root.after(step_ms, lambda: _tick(0.0))
    except Exception:
        pass

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

    icon_path = get_resource_path(os.path.join("assets", "app_icon.ico"))
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)

    # 2. DEKORU KUR: Arayüzü oluştur
    app = MainUI(root)

    # 3. PENCERE AYARLARI: Boyutlandırmayı kilitle ve işletim sisteminin çizimleri bitirmesini bekle
    root.resizable(False, False)
    root.update_idletasks()

    # 4. GEOMETRİ HESABI: Uygulamayı ekranın tam ortasına hizala
    sf = root.winfo_fpixels('1i') / 96.0
    genislik = int(376 * sf)
    yukseklik = int(544 * sf)
    x = (root.winfo_screenwidth() // 2) - (genislik // 2)
    y = (root.winfo_screenheight() // 2) - (yukseklik // 2)
    root.geometry(f"{genislik}x{yukseklik}+{x}+{y}")

    # Windows 11'in varsayılan yuvarlak köşelerine izin vermek için iptal edildi
    # _apply_square_corners(root)

    # 5. PERDEYİ AÇ: Şeffaf başlat, fade-in ile tam opaklığa getir
    root.attributes('-alpha', 0.0)
    root.deiconify()
    _fade_in(root)

    root.mainloop()