import tkinter as tk
import os
from ui.arayuz_tasarimi import MainUI

if __name__ == "__main__":
    root = tk.Tk()
    
    # 1. PERDEYİ ANINDA KAPAT: İşletim sisteminin pencereyi anlık çizmesini (zıplamayı) engellemek için,
    # ikon yükleme gibi disk işlemlerinden bile ÖNCE yazılmalıdır.
    root.withdraw()

    # Sektör Standardı: İkon ataması (Eğer dosya dizinde mevcutsa uygula, yoksa çökmeyi engelle)
    if os.path.exists("app_icon.ico"):
        root.iconbitmap("app_icon.ico")

    # 2. DEKORU KUR: Arayuzu olustur
    app = MainUI(root)
    
    # 3. HESAPLAMA YAP: Arka planda boyutları algıla ve ortayı bul
    root.update_idletasks()
    
    # Gizli pencerenin boyutunu winfo_width() yanlış (örneğin 200px) verebilir.
    # Arayüz tasarımında belirlediğimiz 440x620 boyutunu statik olarak alıp ekranın tam ortasını buluyoruz:
    genislik, yukseklik = 440, 520
    x = (root.winfo_screenwidth() // 2) - (genislik // 2)
    y = (root.winfo_screenheight() // 2) - (yukseklik // 2)
    root.geometry(f"{genislik}x{yukseklik}+{x}+{y}")
    
    # 4. PERDEYİ AÇ: Her şey hazır, pencereyi doğrudan hedeflenen yerde göster
    root.deiconify()
    
    root.mainloop()