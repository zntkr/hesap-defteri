import tkinter as tk
import os
import sys
from ui.arayuz_tasarimi import MainUI

def get_resource_path(relative_path: str) -> str:
    """PyInstaller --onefile ile derlendiğinde geçici klasördeki dosyaları bulur."""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    root = tk.Tk()
    
    # 1. PERDEYİ ANINDA KAPAT: İşletim sisteminin pencereyi anlık çizmesini (zıplamayı) engellemek için,
    # ikon yükleme gibi disk işlemlerinden bile ÖNCE yazılmalıdır.
    root.withdraw()

    icon_path = get_resource_path("app_icon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)

    # 2. DEKORU KUR: Arayuzu olustur
    app = MainUI(root)
    
    # 3. HESAPLAMA YAP: Arka planda boyutları algıla ve ortayı bul
    root.update_idletasks()
    
    # Gizli pencerenin boyutunu winfo_width() yanlış (örneğin 200px) verebilir.
    # Arayüz tasarımında belirlediğimiz 440x540 boyutunu statik olarak alıp ekranın tam ortasını buluyoruz:
    genislik, yukseklik = 450, 540
    x = (root.winfo_screenwidth() // 2) - (genislik // 2)
    y = (root.winfo_screenheight() // 2) - (yukseklik // 2)
    root.geometry(f"{genislik}x{yukseklik}+{x}+{y}")
    
    # 4. PERDEYİ AÇ: Her şey hazır, pencereyi doğrudan hedeflenen yerde göster
    root.deiconify()
    
    root.mainloop()