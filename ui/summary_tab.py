import tkinter as tk

class SummaryTab(tk.Frame):
    """Component class for the Summary (Özet) tab."""
    def __init__(self, parent, ui):
        super().__init__(parent, bg=ui.bg_color, padx=30, pady=20)
        self.ui = ui
        self.build_ui()

    def build_ui(self):
        self.result_lbl = tk.Label(self, text="0", font=self.ui.font_title, fg=self.ui.fg_color, bg=self.ui.bg_color, cursor="hand2")
        self.result_lbl.pack(pady=(15, 0)) 
        self.result_lbl.bind('<Button-1>', self.copy_to_clipboard)
        
        self.sum_lbl = tk.Label(self, text="Toplam: 0", font=self.ui.font_bold, fg="#888888", bg=self.ui.bg_color)
        self.sum_lbl.pack(pady=(0, 10))
        
        self.info_lbl = tk.Label(self, text="Sayıları yapıştırıp Enter'a basın", font=self.ui.font_main, fg="#888888", bg=self.ui.bg_color)
        self.info_lbl.pack()

    def copy_to_clipboard(self, event=None):
        result = self.result_lbl.cget("text")
        if result != "0":
            self.ui.root.clipboard_clear()
            self.ui.root.clipboard_append(result)
            self.ui.root.update() 
            self.info_lbl.config(text="Kopyalandı!", fg=self.ui.accent_color)
            self.ui.root.after(1500, lambda: self.info_lbl.config(text="Sayıları yapıştırıp Enter'a basın", fg="#888888"))

    def update_data(self, analysis):
        self.result_lbl.config(text=str(analysis["ortalama"]), fg=self.ui.fg_color)
        self.sum_lbl.config(text=f"Toplam: {analysis['toplam']}")
        self.info_lbl.config(text=f"{analysis['adet']} sayı işlendi • Kopyalamak için sonuca tıklayın", fg=self.ui.accent_color) 

    def clear_data(self):
        self.result_lbl.config(text="0")
        self.sum_lbl.config(text="Toplam: 0")
        self.info_lbl.config(text="Sayıları yapıştırıp Enter'a basın", fg="#888888")