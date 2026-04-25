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

def _fade_in(root: tk.Tk, alpha: float = 0.0) -> None:
    """Pencereyi yumuşak bir şekilde (fade-in) görünür yapar."""
    alpha += 0.06  # Sektör standardı akıcılık: ~16 adımda (150-160ms) tamamlar
    if alpha < 1.0:
        root.attributes("-alpha", alpha)
        root.after(10, lambda: _fade_in(root, alpha))
    else:
        root.attributes("-alpha", 1.0)

if __name__ == "__main__":
    # Yüksek çözünürlüklü ekranlarda (High-DPI) ikon ve arayüz bulanıklığını önler
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    root = tk.Tk()

    # 1. PERDEYİ ANINDA KAPAT: İşletim sisteminin pencereyi anlık çizmesini (zıplamayı) engellemek için,
    # ikon yükleme gibi disk işlemlerinden bile ÖNCE yazılmalıdır.
    root.withdraw()

    icon_path = get_resource_path("app_icon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)

    # 2. DEKORU KUR: Arayuzu olustur
    app = MainUI(root)

    # 3. GEOMETRİ HESABI: 400x560 (8-Point Grid - Fiziksel Defter Oranı) sabit boyutunu alıp ekran ortasını buluyoruz.
    genislik, yukseklik = 400, 560
    x = (root.winfo_screenwidth() // 2) - (genislik // 2)
    y = (root.winfo_screenheight() // 2) - (yukseklik // 2)
    root.geometry(f"{genislik}x{yukseklik}+{x}+{y}")

    # 4. ŞEFFAFLIK AYARI: Pencere ekrana yansımadan önce tamamen şeffaf yapılır
    root.attributes("-alpha", 0.0)

    # 5. PERDEYİ AÇ: Saydam (görünmez) olarak OS seviyesinde oluştur
    root.deiconify()
    
    # Windows Tkinter Bug Fix: Gizli pencerede resizable(False) yapılırsa iç alan (Client Area) 30-40px kırpılır.
    # Boyut kilitleme işlemini pencere görünür olduktan SONRA (ama henüz şeffafken) yapıyoruz.
    root.resizable(False, False)
    
    # 6. DWM & OS SYNC: Resizable işlemi pencere stilini değiştirir. 
    # Bu değişimin yaratacağı görsel titremeyi (glitch) şeffafken absorbe etmek için ekranı zorla güncelliyoruz.
    root.update()

    # 7. KÖŞE EFEKTİ: DWM tamamen oturduktan sonra köşeleri kesiyoruz
    _apply_square_corners(root)

    # 8. FADE-IN: İşletim sisteminin gölgeleri çizmesi için çok ufak bir avans (30ms) verip animasyonu başlatıyoruz
    root.after(30, lambda: _fade_in(root))

    root.mainloop()