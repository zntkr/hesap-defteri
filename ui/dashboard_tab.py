import tkinter as tk
from tkinter import ttk

class DashboardTab(tk.Frame):
    """Component class for the Unified Dashboard (Ana Ekran) tab."""
    def __init__(self, parent, ui):
        super().__init__(parent, bg=ui.bg_color, padx=30, pady=15)
        self.ui = ui
        self.has_data = False
        self.stats_labels = {}
        self.build_ui()

    def build_ui(self):
        # --- ÖZET BÖLÜMÜ (ÜST) ---
        summary_frame = tk.Frame(self, bg=self.ui.bg_color)
        summary_frame.pack(fill="x", pady=(0, 15))

        self.result_lbl = tk.Label(summary_frame, text="-", font=self.ui.font_title, fg=self.ui.fg_color, bg=self.ui.bg_color, cursor="hand2")
        self.result_lbl.pack(pady=(5, 0)) 
        self.result_lbl.bind('<Button-1>', self.copy_to_clipboard)
        
        self.sum_lbl = tk.Label(summary_frame, text="Toplam: -", font=self.ui.font_bold, fg=self.ui.text_secondary, bg=self.ui.bg_color)
        self.sum_lbl.pack(pady=(0, 10))
        
        self.info_lbl = tk.Label(summary_frame, text="Hesaplamak için Enter'a basın", font=self.ui.font_main, fg=self.ui.text_secondary, bg=self.ui.bg_color)
        self.info_lbl.pack()

        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=10)

        # --- İSTATİSTİK BÖLÜMÜ (ALT - 2 SÜTUNLU YAPI) ---
        stats_frame = tk.Frame(self, bg=self.ui.bg_color)
        stats_frame.pack(pady=(10, 0))
        
        items = [
            ("VERİ ADEDİ:", "adet"), ("MEDYAN:", "medyan"),
            ("EN BÜYÜK:", "en_buyuk"), ("AÇIKLIK (FARK):", "aciklik"),
            ("EN KÜÇÜK:", "en_kucuk"), ("STD. SAPMA:", "std_sapma")
        ]
        
        for i, (text, key) in enumerate(items):
            row = i // 2
            col = (i % 2) * 2
            pad_left = 30 if col == 2 else 0 # Sütunlar arası boşluk
            
            tk.Label(stats_frame, text=text, fg=self.ui.text_secondary, bg=self.ui.bg_color, font=self.ui.font_main).grid(row=row, column=col, sticky="w", pady=6, padx=(pad_left, 5))
            lbl = tk.Label(stats_frame, text="-", font=self.ui.font_bold, fg=self.ui.fg_color, bg=self.ui.bg_color)
            lbl.grid(row=row, column=col+1, sticky="w")
            self.stats_labels[key] = lbl

    def copy_to_clipboard(self, event=None):
        if self.has_data:
            result = self.result_lbl.cget("text")
            self.ui.root.clipboard_clear()
            self.ui.root.clipboard_append(result)
            self.ui.root.update() 
            self.info_lbl.config(text="Kopyalandı!", fg=self.ui.accent_color)
            self.ui.root.after(1500, lambda: self.info_lbl.config(text="Sayıları yapıştırıp Enter'a basın", fg=self.ui.text_secondary))

    def update_data(self, analysis):
        self.has_data = True
        self.result_lbl.config(text=str(analysis["ortalama"]), fg=self.ui.fg_color)
        self.sum_lbl.config(text=f"Toplam: {analysis['toplam']}")
        self.info_lbl.config(text=f"{analysis['adet']} sayı işlendi • Kopyalamak için rakama tıklayın", fg=self.ui.accent_color) 
        for key, lbl in self.stats_labels.items():
            lbl.config(text=str(analysis[key]))

    def clear_data(self):
        self.has_data = False
        self.result_lbl.config(text="-")
        self.sum_lbl.config(text="Toplam: -")
        self.info_lbl.config(text="Hesaplamak için Enter'a basın", fg=self.ui.text_secondary)
        for lbl in self.stats_labels.values(): lbl.config(text="-")