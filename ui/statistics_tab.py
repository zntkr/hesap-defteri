import tkinter as tk

class StatisticsTab(tk.Frame):
    """Component class for the Statistics (İstatistik) tab."""
    def __init__(self, parent, ui):
        super().__init__(parent, bg=ui.bg_color, padx=30, pady=20)
        self.ui = ui
        self.stats_labels = {}
        self.build_ui()

    def build_ui(self):
        items = [
            ("EN BÜYÜK:", "en_buyuk"), 
            ("EN KÜÇÜK:", "en_kucuk"), 
            ("MEDYAN:", "medyan"),
            ("VARYANS:", "varyans"),
            ("STD. SAPMA:", "std_sapma"),
            ("VERİ ADEDİ:", "adet")
        ]
        for i, (text, key) in enumerate(items):
            tk.Label(self, text=text, fg="#888888", bg=self.ui.bg_color, font=self.ui.font_main).grid(row=i, column=0, sticky="w", pady=6)
            lbl = tk.Label(self, text="-", font=self.ui.font_bold, fg=self.ui.fg_color, bg=self.ui.bg_color)
            lbl.grid(row=i, column=1, sticky="w", padx=30)
            self.stats_labels[key] = lbl

    def update_data(self, analysis):
        for key, lbl in self.stats_labels.items():
            lbl.config(text=str(analysis[key]))

    def clear_data(self):
        for lbl in self.stats_labels.values(): 
            lbl.config(text="-")