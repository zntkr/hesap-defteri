import tkinter as tk
from tkinter import ttk
from core.matematik_motoru import MatematikMotoru
from core.finans_motoru import FinansMotoru

class ToolsTab(tk.Frame):
    """Component class for the Tools (Araçlar) tab."""
    def __init__(self, parent, ui):
        super().__init__(parent, bg=ui.bg_color, padx=30, pady=20)
        self.ui = ui
        self.build_ui()

    def build_ui(self):
        # --- KDV CALCULATOR ---
        tk.Label(self, text="KDV HESAPLAYICI", font=self.ui.font_bold, fg=self.ui.fg_color, bg=self.ui.bg_color).pack(anchor="w", pady=(0, 10))
        
        tax_frame = tk.Frame(self, bg=self.ui.bg_color)
        tax_frame.pack(fill="x", pady=5)
        
        tk.Label(tax_frame, text="Tutar:", font=self.ui.font_main, fg=self.ui.fg_color, bg=self.ui.bg_color).grid(row=0, column=0, sticky="w", pady=5)
        self.tax_amount_entry = tk.Entry(tax_frame, font=self.ui.font_main, bg="#FFFFFF", fg=self.ui.fg_color, bd=2, relief="sunken", width=15)
        self.tax_amount_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(tax_frame, text="Oran (%):", font=self.ui.font_main, fg=self.ui.fg_color, bg=self.ui.bg_color).grid(row=1, column=0, sticky="w", pady=5)
        self.tax_rate_entry = tk.Entry(tax_frame, font=self.ui.font_main, bg="#FFFFFF", fg=self.ui.fg_color, bd=2, relief="sunken", width=15)
        self.tax_rate_entry.insert(0, "20")
        self.tax_rate_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tax_btn = tk.Button(tax_frame, text="HESAPLA", font=self.ui.font_bold, bg=self.ui.accent_color, fg="#FFFFFF", 
                            bd=2, relief="raised", activebackground=self.ui.accent_hover, activeforeground="#FFFFFF", cursor="hand2", command=self.calculate_tax)
        tax_btn.grid(row=0, column=2, rowspan=2, padx=10, sticky="ns", pady=5, ipadx=10)
        
        tax_res_frame = tk.Frame(self, bg=self.ui.bg_color)
        tax_res_frame.pack(fill="x", pady=(15, 0))
        
        self.tax_labels = {}
        tax_items = [("Ham Tutar:", "ham_tutar"), ("KDV Tutarı:", "kdv_tutari"), ("Toplam Tutar:", "toplam")]
        for i, (text, key) in enumerate(tax_items):
            tk.Label(tax_res_frame, text=text, fg="#888888", bg=self.ui.bg_color, font=self.ui.font_main).grid(row=i, column=0, sticky="w", pady=4)
            lbl = tk.Label(tax_res_frame, text="-", font=self.ui.font_bold, fg=self.ui.fg_color, bg=self.ui.bg_color)
            lbl.grid(row=i, column=1, sticky="w", padx=20)
            self.tax_labels[key] = lbl
            
        self.tax_info_lbl = tk.Label(self, text="KDV hesaplamak için tutarı girin", font=self.ui.font_main, fg="#888888", bg=self.ui.bg_color)
        self.tax_info_lbl.pack(pady=(5, 0))

        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=15)
        
        # --- DISCOUNT CALCULATOR ---
        tk.Label(self, text="İNDİRİM HESAPLAYICI", font=self.ui.font_bold, fg=self.ui.fg_color, bg=self.ui.bg_color).pack(anchor="w", pady=(0, 10))
        
        discount_frame = tk.Frame(self, bg=self.ui.bg_color)
        discount_frame.pack(fill="x", pady=5)
        
        tk.Label(discount_frame, text="Tutar:", font=self.ui.font_main, fg=self.ui.fg_color, bg=self.ui.bg_color).grid(row=0, column=0, sticky="w", pady=5)
        self.discount_amount_entry = tk.Entry(discount_frame, font=self.ui.font_main, bg="#FFFFFF", fg=self.ui.fg_color, bd=2, relief="sunken", width=15)
        self.discount_amount_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(discount_frame, text="İndirim (%):", font=self.ui.font_main, fg=self.ui.fg_color, bg=self.ui.bg_color).grid(row=1, column=0, sticky="w", pady=5)
        self.discount_rate_entry = tk.Entry(discount_frame, font=self.ui.font_main, bg="#FFFFFF", fg=self.ui.fg_color, bd=2, relief="sunken", width=15)
        self.discount_rate_entry.insert(0, "10")
        self.discount_rate_entry.grid(row=1, column=1, padx=10, pady=5)
        
        discount_btn = tk.Button(discount_frame, text="HESAPLA", font=self.ui.font_bold, bg=self.ui.accent_color, fg="#FFFFFF", 
                                 bd=2, relief="raised", activebackground=self.ui.accent_hover, activeforeground="#FFFFFF", cursor="hand2", command=self.calculate_discount)
        discount_btn.grid(row=0, column=2, rowspan=2, padx=10, sticky="ns", pady=5, ipadx=10)
        
        discount_res_frame = tk.Frame(self, bg=self.ui.bg_color)
        discount_res_frame.pack(fill="x", pady=(10, 0))
        
        self.discount_labels = {}
        discount_items = [("Ham Tutar:", "ham_tutar"), ("İndirim Tutarı:", "indirim_tutari"), ("Net Tutar:", "net_tutar")]
        for i, (text, key) in enumerate(discount_items):
            tk.Label(discount_res_frame, text=text, fg="#888888", bg=self.ui.bg_color, font=self.ui.font_main).grid(row=i, column=0, sticky="w", pady=4)
            lbl = tk.Label(discount_res_frame, text="-", font=self.ui.font_bold, fg=self.ui.fg_color, bg=self.ui.bg_color)
            lbl.grid(row=i, column=1, sticky="w", padx=20)
            self.discount_labels[key] = lbl
            
        self.discount_info_lbl = tk.Label(self, text="İndirim hesaplamak için tutarı girin", font=self.ui.font_main, fg="#888888", bg=self.ui.bg_color)
        self.discount_info_lbl.pack(pady=(5, 0))

        self.tax_amount_entry.bind('<Return>', self.calculate_tax)
        self.tax_rate_entry.bind('<Return>', self.calculate_tax)
        self.discount_amount_entry.bind('<Return>', self.calculate_discount)
        self.discount_rate_entry.bind('<Return>', self.calculate_discount)

    def calculate_tax(self, event=None):
        amount_str = self.tax_amount_entry.get().strip()
        rate_str = self.tax_rate_entry.get().strip()
        
        amount_numbers = MatematikMotoru.metinden_sayilari_ayikla(amount_str)
        rate_numbers = MatematikMotoru.metinden_sayilari_ayikla(rate_str)
        
        if not amount_numbers:
            self.tax_info_lbl.config(text="Geçersiz tutar!", fg="#D32F2F")
            return "break"
            
        amount = amount_numbers[0]
        rate = rate_numbers[0] if rate_numbers else 20.0
        result = FinansMotoru.kdv_hesapla(amount, rate)
        
        for key, lbl in self.tax_labels.items():
            lbl.config(text=str(result[key]))
        self.tax_info_lbl.config(text="KDV hesaplandı", fg=self.ui.accent_color)
        return "break"

    def calculate_discount(self, event=None):
        amount_str = self.discount_amount_entry.get().strip()
        rate_str = self.discount_rate_entry.get().strip()
        
        amount_numbers = MatematikMotoru.metinden_sayilari_ayikla(amount_str)
        rate_numbers = MatematikMotoru.metinden_sayilari_ayikla(rate_str)
        
        if not amount_numbers:
            self.discount_info_lbl.config(text="Geçersiz tutar!", fg="#D32F2F")
            return "break"
            
        amount = amount_numbers[0]
        rate = rate_numbers[0] if rate_numbers else 10.0
        result = FinansMotoru.indirim_hesapla(amount, rate)
        
        for key, lbl in self.discount_labels.items():
            lbl.config(text=str(result[key]))
        self.discount_info_lbl.config(text="İndirim hesaplandı", fg=self.ui.accent_color)
        return "break"

    def clear_data(self):
        self.tax_amount_entry.delete(0, tk.END)
        self.tax_rate_entry.delete(0, tk.END)
        self.tax_rate_entry.insert(0, "20")
        for lbl in self.tax_labels.values(): lbl.config(text="-")
        self.tax_info_lbl.config(text="KDV hesaplamak için tutarı girin", fg="#888888")
        
        self.discount_amount_entry.delete(0, tk.END)
        self.discount_rate_entry.delete(0, tk.END)
        self.discount_rate_entry.insert(0, "10")
        for lbl in self.discount_labels.values(): lbl.config(text="-")
        self.discount_info_lbl.config(text="İndirim hesaplamak için tutarı girin", fg="#888888")