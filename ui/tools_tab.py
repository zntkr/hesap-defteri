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
        # --- ARAÇ SEÇİCİ HEADER ---
        header_frame = tk.Frame(self, bg=self.ui.bg_color)
        header_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(header_frame, text="İŞLEM TİPİ SEÇİN:", font=self.ui.font_bold, fg=self.ui.fg_color, bg=self.ui.bg_color).pack(side="left")
        
        self.tool_var = tk.StringVar()
        self.tool_selector = ttk.Combobox(header_frame, textvariable=self.tool_var, state="readonly", font=self.ui.font_main, width=20)
        self.tool_selector['values'] = ("Değişim Oranı", "KDV Hesaplayıcı", "İndirim Hesaplayıcı")
        self.tool_selector.current(0)
        self.tool_selector.pack(side="right", fill="x", expand=True, padx=(15, 0))
        self.tool_selector.bind("<<ComboboxSelected>>", self.on_tool_change)
        
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=(0, 15))

        # --- DİNAMİK KONTEYNER ---
        self.container = tk.Frame(self, bg=self.ui.bg_color)
        self.container.pack(fill="both", expand=True)
        
        # Alt araç frameleri
        self.frames = {}
        self.frames["KDV Hesaplayıcı"] = self.build_tax_tool()
        self.frames["İndirim Hesaplayıcı"] = self.build_discount_tool()
        self.frames["Değişim Oranı"] = self.build_change_tool()
        
        # Başlangıçta Değişim Oranı göster (En sık kullanılan araç)
        self.current_frame = self.frames["Değişim Oranı"]
        self.current_frame.pack(fill="both", expand=True)

    def on_tool_change(self, event=None):
        selected_tool = self.tool_var.get()
        self.current_frame.pack_forget()
        self.current_frame = self.frames[selected_tool]
        self.current_frame.pack(fill="both", expand=True)

    def build_tax_tool(self):
        frame = tk.Frame(self.container, bg=self.ui.bg_color)
        
        tax_frame = tk.Frame(frame, bg=self.ui.bg_color)
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
        tax_btn.grid(row=0, column=2, padx=10, sticky="nsew", pady=(5, 2), ipadx=10)
        
        tax_clear_btn = tk.Button(tax_frame, text="Temizle", font=(self.ui.font_main[0], 8), bg="#EFEBE6", fg="#888888", 
                                  bd=1, relief="raised", activebackground="#E0DCE3", cursor="hand2", command=self.clear_data)
        tax_clear_btn.grid(row=1, column=2, padx=10, sticky="nsew", pady=(2, 5))
        
        tax_res_frame = tk.Frame(frame, bg=self.ui.bg_color)
        tax_res_frame.pack(fill="x", pady=(15, 0))
        
        self.tax_labels = {}
        tax_items = [("Ham Tutar:", "ham_tutar"), ("KDV Tutarı:", "kdv_tutari"), ("Toplam Tutar:", "toplam")]
        for i, (text, key) in enumerate(tax_items):
            tk.Label(tax_res_frame, text=text, fg="#888888", bg=self.ui.bg_color, font=self.ui.font_main).grid(row=i, column=0, sticky="w", pady=4)
            lbl = tk.Label(tax_res_frame, text="-", font=self.ui.font_bold, fg=self.ui.fg_color, bg=self.ui.bg_color)
            lbl.grid(row=i, column=1, sticky="w", padx=20)
            self.tax_labels[key] = lbl
            
        self.tax_info_lbl = tk.Label(frame, text="KDV hesaplamak için tutarı girin", font=self.ui.font_main, fg="#888888", bg=self.ui.bg_color)
        self.tax_info_lbl.pack(pady=(5, 0))
        
        self.tax_amount_entry.bind('<Return>', self.calculate_tax)
        self.tax_rate_entry.bind('<Return>', self.calculate_tax)
        
        return frame

    def build_discount_tool(self):
        frame = tk.Frame(self.container, bg=self.ui.bg_color)
        
        discount_frame = tk.Frame(frame, bg=self.ui.bg_color)
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
        discount_btn.grid(row=0, column=2, padx=10, sticky="nsew", pady=(5, 2), ipadx=10)
        
        discount_clear_btn = tk.Button(discount_frame, text="Temizle", font=(self.ui.font_main[0], 8), bg="#EFEBE6", fg="#888888", 
                                       bd=1, relief="raised", activebackground="#E0DCE3", cursor="hand2", command=self.clear_data)
        discount_clear_btn.grid(row=1, column=2, padx=10, sticky="nsew", pady=(2, 5))
        
        discount_res_frame = tk.Frame(frame, bg=self.ui.bg_color)
        discount_res_frame.pack(fill="x", pady=(10, 0))
        
        self.discount_labels = {}
        discount_items = [("Ham Tutar:", "ham_tutar"), ("İndirim Tutarı:", "indirim_tutari"), ("Net Tutar:", "net_tutar")]
        for i, (text, key) in enumerate(discount_items):
            tk.Label(discount_res_frame, text=text, fg="#888888", bg=self.ui.bg_color, font=self.ui.font_main).grid(row=i, column=0, sticky="w", pady=4)
            lbl = tk.Label(discount_res_frame, text="-", font=self.ui.font_bold, fg=self.ui.fg_color, bg=self.ui.bg_color)
            lbl.grid(row=i, column=1, sticky="w", padx=20)
            self.discount_labels[key] = lbl
            
        self.discount_info_lbl = tk.Label(frame, text="İndirim hesaplamak için tutarı girin", font=self.ui.font_main, fg="#888888", bg=self.ui.bg_color)
        self.discount_info_lbl.pack(pady=(5, 0))
        
        self.discount_amount_entry.bind('<Return>', self.calculate_discount)
        self.discount_rate_entry.bind('<Return>', self.calculate_discount)
        
        return frame

    def build_change_tool(self):
        frame = tk.Frame(self.container, bg=self.ui.bg_color)
        
        change_frame = tk.Frame(frame, bg=self.ui.bg_color)
        change_frame.pack(fill="x", pady=5)
        
        tk.Label(change_frame, text="Eski Değer:", font=self.ui.font_main, fg=self.ui.fg_color, bg=self.ui.bg_color).grid(row=0, column=0, sticky="w", pady=5)
        self.old_val_entry = tk.Entry(change_frame, font=self.ui.font_main, bg="#FFFFFF", fg=self.ui.fg_color, bd=2, relief="sunken", width=15)
        self.old_val_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(change_frame, text="Yeni Değer:", font=self.ui.font_main, fg=self.ui.fg_color, bg=self.ui.bg_color).grid(row=1, column=0, sticky="w", pady=5)
        self.new_val_entry = tk.Entry(change_frame, font=self.ui.font_main, bg="#FFFFFF", fg=self.ui.fg_color, bd=2, relief="sunken", width=15)
        self.new_val_entry.grid(row=1, column=1, padx=10, pady=5)
        
        change_btn = tk.Button(change_frame, text="HESAPLA", font=self.ui.font_bold, bg=self.ui.accent_color, fg="#FFFFFF", 
                                 bd=2, relief="raised", activebackground=self.ui.accent_hover, activeforeground="#FFFFFF", cursor="hand2", command=self.calculate_change)
        change_btn.grid(row=0, column=2, padx=10, sticky="nsew", pady=(5, 2), ipadx=10)
        
        change_clear_btn = tk.Button(change_frame, text="Temizle", font=(self.ui.font_main[0], 8), bg="#EFEBE6", fg="#888888", 
                                     bd=1, relief="raised", activebackground="#E0DCE3", cursor="hand2", command=self.clear_data)
        change_clear_btn.grid(row=1, column=2, padx=10, sticky="nsew", pady=(2, 5))
        
        change_res_frame = tk.Frame(frame, bg=self.ui.bg_color)
        change_res_frame.pack(fill="x", pady=(10, 0))
        
        tk.Label(change_res_frame, text="Değişim Oranı:", fg="#888888", bg=self.ui.bg_color, font=self.ui.font_main).grid(row=0, column=0, sticky="w", pady=4)
        self.change_res_lbl = tk.Label(change_res_frame, text="-", font=self.ui.font_title, fg=self.ui.fg_color, bg=self.ui.bg_color, cursor="hand2")
        self.change_res_lbl.grid(row=0, column=1, sticky="w", padx=20)
        self.change_res_lbl.bind('<Button-1>', self.copy_change_rate)
            
        self.change_info_lbl = tk.Label(frame, text="Artış veya azalışı görmek için değerleri girin", font=self.ui.font_main, fg="#888888", bg=self.ui.bg_color)
        self.change_info_lbl.pack(pady=(15, 0))
        
        self.old_val_entry.bind('<Return>', self.calculate_change)
        self.new_val_entry.bind('<Return>', self.calculate_change)
        
        return frame

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

    def calculate_change(self, event=None):
        old_str = self.old_val_entry.get().strip()
        new_str = self.new_val_entry.get().strip()
        
        old_nums = MatematikMotoru.metinden_sayilari_ayikla(old_str)
        new_nums = MatematikMotoru.metinden_sayilari_ayikla(new_str)
        
        if not old_nums or not new_nums:
            self.change_info_lbl.config(text="Eski ve yeni değer eksik!", fg="#D32F2F")
            return "break"
            
        old_val = old_nums[0]
        new_val = new_nums[0]
        
        result = FinansMotoru.degisim_orani_hesapla(old_val, new_val)
        oran = result["degisim_orani"]
        
        sembol = "+" if oran > 0 else ""
        self.change_res_lbl.config(text=f"%{sembol}{oran}")
        self.change_info_lbl.config(text="Hesaplandı • Kopyalamak için sonuca tıklayın", fg=self.ui.accent_color)
        return "break"

    def copy_change_rate(self, event=None):
        result = self.change_res_lbl.cget("text")
        if result != "-":
            self.ui.root.clipboard_clear()
            self.ui.root.clipboard_append(result)
            self.ui.root.update()
            self.change_info_lbl.config(text="Kopyalandı!", fg=self.ui.accent_color)
            self.ui.root.after(1500, lambda: self.change_info_lbl.config(text="Hesaplandı • Kopyalamak için sonuca tıklayın", fg=self.ui.accent_color))

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
        
        self.old_val_entry.delete(0, tk.END)
        self.new_val_entry.delete(0, tk.END)
        self.change_res_lbl.config(text="-")
        self.change_info_lbl.config(text="Artış veya azalışı görmek için değerleri girin", fg="#888888")