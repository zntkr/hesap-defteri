import tkinter as tk
from tkinter import ttk
import sys
import os

# Proje kök dizinini Python yoluna ekle (Pylance import hatalarını önlemek için)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
        self.tool_selector['values'] = ("Değişim Oranı", "KDV Hesaplayıcı", "İndirim Hesaplayıcı", "Orantı Hesaplayıcı", "Yaş Hesaplayıcı")
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
        self.frames["Orantı Hesaplayıcı"] = self.build_proportion_tool()
        self.frames["Yaş Hesaplayıcı"] = self.build_age_tool()
        
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
        
        desc_frame = tk.Frame(frame, bg=self.ui.bg_secondary, padx=10, pady=10)
        desc_frame.pack(fill="x", pady=(0, 15))
        tk.Label(desc_frame, text="KDV Hesaplayıcı", font=self.ui.font_bold, fg=self.ui.accent_color, bg=self.ui.bg_secondary).pack(anchor="w")
        tk.Label(desc_frame, text="Örn: 1.500 TL tutar ve %20 oran girerek KDV payını ve toplam matrahı hesaplayabilirsiniz.", font=self.ui.font_main, fg=self.ui.text_secondary, bg=self.ui.bg_secondary, justify="left", wraplength=360).pack(anchor="w", pady=(2,0))
        
        tax_frame = tk.Frame(frame, bg=self.ui.bg_color)
        tax_frame.pack(fill="x", pady=5)
        
        tk.Label(tax_frame, text="Tutar:", font=self.ui.font_main, fg=self.ui.fg_color, bg=self.ui.bg_color).grid(row=0, column=0, sticky="w", pady=5)
        self.tax_amount_entry = tk.Entry(tax_frame, font=self.ui.font_main, bg=self.ui.shadow_light, fg=self.ui.fg_color, bd=2, relief="sunken", width=15)
        self.tax_amount_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(tax_frame, text="Oran (%):", font=self.ui.font_main, fg=self.ui.fg_color, bg=self.ui.bg_color).grid(row=1, column=0, sticky="w", pady=5)
        self.tax_rate_entry = tk.Entry(tax_frame, font=self.ui.font_main, bg=self.ui.shadow_light, fg=self.ui.fg_color, bd=2, relief="sunken", width=15)
        self.tax_rate_entry.insert(0, "20")
        self.tax_rate_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tax_btn = tk.Button(tax_frame, text="HESAPLA", font=self.ui.font_bold, bg=self.ui.accent_color, fg=self.ui.shadow_light, 
                            bd=2, relief="raised", activebackground=self.ui.accent_hover, activeforeground=self.ui.shadow_light, cursor="hand2", command=self.calculate_tax)
        tax_btn.grid(row=0, column=2, padx=10, sticky="nsew", pady=(5, 2), ipadx=10)
        
        tax_clear_btn = tk.Button(tax_frame, text="Temizle", font=(self.ui.font_main[0], 8), bg=self.ui.bg_secondary, fg=self.ui.text_secondary, 
                                  bd=1, relief="raised", activebackground=self.ui.border_color, cursor="hand2", command=self.clear_data)
        tax_clear_btn.grid(row=1, column=2, padx=10, sticky="nsew", pady=(2, 5))
        
        tax_res_frame = tk.Frame(frame, bg=self.ui.bg_color)
        tax_res_frame.pack(fill="x", pady=(15, 0))
        
        self.tax_labels = {}
        tax_items = [("Ham Tutar:", "ham_tutar"), ("KDV Tutarı:", "kdv_tutari"), ("Toplam Tutar:", "toplam")]
        for i, (text, key) in enumerate(tax_items):
            tk.Label(tax_res_frame, text=text, fg=self.ui.text_secondary, bg=self.ui.bg_color, font=self.ui.font_main).grid(row=i, column=0, sticky="w", pady=4)
            lbl = tk.Label(tax_res_frame, text="-", font=self.ui.font_bold, fg=self.ui.fg_color, bg=self.ui.bg_color)
            lbl.grid(row=i, column=1, sticky="w", padx=20)
            self.tax_labels[key] = lbl
            
        self.tax_info_lbl = tk.Label(frame, text="KDV hesaplamak için tutarı girin", font=self.ui.font_main, fg=self.ui.text_secondary, bg=self.ui.bg_color)
        self.tax_info_lbl.pack(pady=(5, 0))
        
        self.tax_amount_entry.bind('<Return>', self.calculate_tax)
        self.tax_rate_entry.bind('<Return>', self.calculate_tax)
        
        return frame

    def build_discount_tool(self):
        frame = tk.Frame(self.container, bg=self.ui.bg_color)
        
        desc_frame = tk.Frame(frame, bg=self.ui.bg_secondary, padx=10, pady=10)
        desc_frame.pack(fill="x", pady=(0, 15))
        tk.Label(desc_frame, text="İndirim Hesaplayıcı", font=self.ui.font_bold, fg=self.ui.accent_color, bg=self.ui.bg_secondary).pack(anchor="w")
        tk.Label(desc_frame, text="Örn: 2.500 TL'lik bir ürüne %15 indirim uygulandığında net fiyatı ve indirim tutarını gösterir.", font=self.ui.font_main, fg=self.ui.text_secondary, bg=self.ui.bg_secondary, justify="left", wraplength=360).pack(anchor="w", pady=(2,0))
        
        discount_frame = tk.Frame(frame, bg=self.ui.bg_color)
        discount_frame.pack(fill="x", pady=5)
        
        tk.Label(discount_frame, text="Tutar:", font=self.ui.font_main, fg=self.ui.fg_color, bg=self.ui.bg_color).grid(row=0, column=0, sticky="w", pady=5)
        self.discount_amount_entry = tk.Entry(discount_frame, font=self.ui.font_main, bg=self.ui.shadow_light, fg=self.ui.fg_color, bd=2, relief="sunken", width=15)
        self.discount_amount_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(discount_frame, text="İndirim (%):", font=self.ui.font_main, fg=self.ui.fg_color, bg=self.ui.bg_color).grid(row=1, column=0, sticky="w", pady=5)
        self.discount_rate_entry = tk.Entry(discount_frame, font=self.ui.font_main, bg=self.ui.shadow_light, fg=self.ui.fg_color, bd=2, relief="sunken", width=15)
        self.discount_rate_entry.insert(0, "10")
        self.discount_rate_entry.grid(row=1, column=1, padx=10, pady=5)
        
        discount_btn = tk.Button(discount_frame, text="HESAPLA", font=self.ui.font_bold, bg=self.ui.accent_color, fg=self.ui.shadow_light, 
                                 bd=2, relief="raised", activebackground=self.ui.accent_hover, activeforeground=self.ui.shadow_light, cursor="hand2", command=self.calculate_discount)
        discount_btn.grid(row=0, column=2, padx=10, sticky="nsew", pady=(5, 2), ipadx=10)
        
        discount_clear_btn = tk.Button(discount_frame, text="Temizle", font=(self.ui.font_main[0], 8), bg=self.ui.bg_secondary, fg=self.ui.text_secondary, 
                                       bd=1, relief="raised", activebackground=self.ui.border_color, cursor="hand2", command=self.clear_data)
        discount_clear_btn.grid(row=1, column=2, padx=10, sticky="nsew", pady=(2, 5))
        
        discount_res_frame = tk.Frame(frame, bg=self.ui.bg_color)
        discount_res_frame.pack(fill="x", pady=(10, 0))
        
        self.discount_labels = {}
        discount_items = [("Ham Tutar:", "ham_tutar"), ("İndirim Tutarı:", "indirim_tutari"), ("Net Tutar:", "net_tutar")]
        for i, (text, key) in enumerate(discount_items):
            tk.Label(discount_res_frame, text=text, fg=self.ui.text_secondary, bg=self.ui.bg_color, font=self.ui.font_main).grid(row=i, column=0, sticky="w", pady=4)
            lbl = tk.Label(discount_res_frame, text="-", font=self.ui.font_bold, fg=self.ui.fg_color, bg=self.ui.bg_color)
            lbl.grid(row=i, column=1, sticky="w", padx=20)
            self.discount_labels[key] = lbl
            
        self.discount_info_lbl = tk.Label(frame, text="İndirim hesaplamak için tutarı girin", font=self.ui.font_main, fg=self.ui.text_secondary, bg=self.ui.bg_color)
        self.discount_info_lbl.pack(pady=(5, 0))
        
        self.discount_amount_entry.bind('<Return>', self.calculate_discount)
        self.discount_rate_entry.bind('<Return>', self.calculate_discount)
        
        return frame

    def build_change_tool(self):
        frame = tk.Frame(self.container, bg=self.ui.bg_color)
        
        desc_frame = tk.Frame(frame, bg=self.ui.bg_secondary, padx=10, pady=10)
        desc_frame.pack(fill="x", pady=(0, 15))
        tk.Label(desc_frame, text="Yüzdelik Değişim Oranı", font=self.ui.font_bold, fg=self.ui.accent_color, bg=self.ui.bg_secondary).pack(anchor="w")
        tk.Label(desc_frame, text="Örn: Eski fiyatı 150 TL, yeni fiyatı 200 TL olan bir ürünün yüzde kaç zamlandığını hesaplar.", font=self.ui.font_main, fg=self.ui.text_secondary, bg=self.ui.bg_secondary, justify="left", wraplength=360).pack(anchor="w", pady=(2,0))
        
        change_frame = tk.Frame(frame, bg=self.ui.bg_color)
        change_frame.pack(fill="x", pady=5)
        
        tk.Label(change_frame, text="Eski Değer:", font=self.ui.font_main, fg=self.ui.fg_color, bg=self.ui.bg_color).grid(row=0, column=0, sticky="w", pady=5)
        self.old_val_entry = tk.Entry(change_frame, font=self.ui.font_main, bg=self.ui.shadow_light, fg=self.ui.fg_color, bd=2, relief="sunken", width=15)
        self.old_val_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(change_frame, text="Yeni Değer:", font=self.ui.font_main, fg=self.ui.fg_color, bg=self.ui.bg_color).grid(row=1, column=0, sticky="w", pady=5)
        self.new_val_entry = tk.Entry(change_frame, font=self.ui.font_main, bg=self.ui.shadow_light, fg=self.ui.fg_color, bd=2, relief="sunken", width=15)
        self.new_val_entry.grid(row=1, column=1, padx=10, pady=5)
        
        change_btn = tk.Button(change_frame, text="HESAPLA", font=self.ui.font_bold, bg=self.ui.accent_color, fg=self.ui.shadow_light, 
                                 bd=2, relief="raised", activebackground=self.ui.accent_hover, activeforeground=self.ui.shadow_light, cursor="hand2", command=self.calculate_change)
        change_btn.grid(row=0, column=2, padx=10, sticky="nsew", pady=(5, 2), ipadx=10)
        
        change_clear_btn = tk.Button(change_frame, text="Temizle", font=(self.ui.font_main[0], 8), bg=self.ui.bg_secondary, fg=self.ui.text_secondary, 
                                     bd=1, relief="raised", activebackground=self.ui.border_color, cursor="hand2", command=self.clear_data)
        change_clear_btn.grid(row=1, column=2, padx=10, sticky="nsew", pady=(2, 5))
        
        change_res_frame = tk.Frame(frame, bg=self.ui.bg_color)
        change_res_frame.pack(fill="x", pady=(10, 0))
        
        tk.Label(change_res_frame, text="Değişim Oranı:", fg=self.ui.text_secondary, bg=self.ui.bg_color, font=self.ui.font_main).grid(row=0, column=0, sticky="w", pady=4)
        self.change_res_lbl = tk.Label(change_res_frame, text="-", font=self.ui.font_title, fg=self.ui.fg_color, bg=self.ui.bg_color, cursor="hand2")
        self.change_res_lbl.grid(row=0, column=1, sticky="w", padx=20)
        self.change_res_lbl.bind('<Button-1>', self.copy_change_rate)
            
        self.change_info_lbl = tk.Label(frame, text="Artış veya azalışı görmek için değerleri girin", font=self.ui.font_main, fg=self.ui.text_secondary, bg=self.ui.bg_color)
        self.change_info_lbl.pack(pady=(15, 0))
        
        self.old_val_entry.bind('<Return>', self.calculate_change)
        self.new_val_entry.bind('<Return>', self.calculate_change)
        
        return frame

    def build_proportion_tool(self):
        frame = tk.Frame(self.container, bg=self.ui.bg_color)
        
        # Açıklama Panosu (Info Box)
        desc_frame = tk.Frame(frame, bg="#EFEBE6", padx=10, pady=10)
        desc_frame.pack(fill="x", pady=(0, 15))
        tk.Label(desc_frame, text="İçler Dışlar / Doğru Orantı", font=self.ui.font_bold, fg=self.ui.accent_color, bg="#EFEBE6").pack(anchor="w")
        tk.Label(desc_frame, text="Örn: 150 adet mal 4.500 TL ise, 75 adet mal kaç TL yapar?", font=self.ui.font_main, fg="#666666", bg="#EFEBE6", justify="left", wraplength=360).pack(anchor="w", pady=(2,0))
        
        prop_frame = tk.Frame(frame, bg=self.ui.bg_color)
        prop_frame.pack(fill="x", pady=5)
        
        tk.Label(prop_frame, text="1. Değer (A):", font=self.ui.font_main, fg=self.ui.fg_color, bg=self.ui.bg_color).grid(row=0, column=0, sticky="w", pady=5)
        self.prop_a_entry = tk.Entry(prop_frame, font=self.ui.font_main, bg="#FFFFFF", fg=self.ui.fg_color, bd=2, relief="sunken", width=12)
        self.prop_a_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(prop_frame, text="Karşılığı (B):", font=self.ui.font_main, fg=self.ui.fg_color, bg=self.ui.bg_color).grid(row=1, column=0, sticky="w", pady=5)
        self.prop_b_entry = tk.Entry(prop_frame, font=self.ui.font_main, bg="#FFFFFF", fg=self.ui.fg_color, bd=2, relief="sunken", width=12)
        self.prop_b_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(prop_frame, text="3. Değer (C):", font=self.ui.font_main, fg=self.ui.fg_color, bg=self.ui.bg_color).grid(row=2, column=0, sticky="w", pady=5)
        self.prop_c_entry = tk.Entry(prop_frame, font=self.ui.font_main, bg="#FFFFFF", fg=self.ui.fg_color, bd=2, relief="sunken", width=12)
        self.prop_c_entry.grid(row=2, column=1, padx=10, pady=5)
        
        prop_btn = tk.Button(prop_frame, text="HESAPLA", font=self.ui.font_bold, bg=self.ui.accent_color, fg="#FFFFFF", 
                                 bd=2, relief="raised", activebackground=self.ui.accent_hover, activeforeground="#FFFFFF", cursor="hand2", command=self.calculate_proportion)
        prop_btn.grid(row=0, column=2, padx=10, sticky="nsew", pady=(5, 2), ipadx=10)
        
        prop_clear_btn = tk.Button(prop_frame, text="Temizle", font=(self.ui.font_main[0], 8), bg="#EFEBE6", fg="#888888", 
                                     bd=1, relief="raised", activebackground="#E0DCE3", cursor="hand2", command=self.clear_data)
        prop_clear_btn.grid(row=1, column=2, padx=10, sticky="nsew", pady=(2, 5))
        
        prop_res_frame = tk.Frame(frame, bg=self.ui.bg_color)
        prop_res_frame.pack(fill="x", pady=(15, 0))
        
        tk.Label(prop_res_frame, text="Netice (X):", fg=self.ui.text_secondary, bg=self.ui.bg_color, font=self.ui.font_main).grid(row=0, column=0, sticky="w", pady=4)
        self.prop_res_lbl = tk.Label(prop_res_frame, text="-", font=self.ui.font_title, fg=self.ui.fg_color, bg=self.ui.bg_color, cursor="hand2")
        self.prop_res_lbl.grid(row=0, column=1, sticky="w", padx=20)
        self.prop_res_lbl.bind('<Button-1>', self.copy_prop_rate)
            
        self.prop_info_lbl = tk.Label(frame, text="Orantı sonucunu görmek için değerleri girin", font=self.ui.font_main, fg=self.ui.text_secondary, bg=self.ui.bg_color)
        self.prop_info_lbl.pack(pady=(5, 0))
        
        self.prop_a_entry.bind('<Return>', self.calculate_proportion)
        self.prop_b_entry.bind('<Return>', self.calculate_proportion)
        self.prop_c_entry.bind('<Return>', self.calculate_proportion)
        
        return frame

    def build_age_tool(self):
        frame = tk.Frame(self.container, bg=self.ui.bg_color)
        
        desc_frame = tk.Frame(frame, bg=self.ui.bg_secondary, padx=10, pady=10)
        desc_frame.pack(fill="x", pady=(0, 15))
        tk.Label(desc_frame, text="Detaylı Yaş Analizi", font=self.ui.font_bold, fg=self.ui.accent_color, bg=self.ui.bg_secondary).pack(anchor="w")
        tk.Label(desc_frame, text="Örn: 15.05.1990 girerek doğduğunuz günü, tam yaşınızı ve sonraki doğum gününüze kalan süreyi bulun.", font=self.ui.font_main, fg=self.ui.text_secondary, bg=self.ui.bg_secondary, justify="left", wraplength=360).pack(anchor="w", pady=(2,0))
        
        age_frame = tk.Frame(frame, bg=self.ui.bg_color)
        age_frame.pack(fill="x", pady=5)
        
        tk.Label(age_frame, text="Doğum Tarihi:", font=self.ui.font_main, fg=self.ui.fg_color, bg=self.ui.bg_color).grid(row=0, column=0, sticky="w", pady=5)
        self.age_year_entry = tk.Entry(age_frame, font=self.ui.font_main, bg=self.ui.shadow_light, fg=self.ui.text_placeholder, bd=2, relief="sunken", width=15)
        self.age_year_entry.insert(0, "GG.AA.YYYY")
        self.age_year_entry.grid(row=0, column=1, padx=10, pady=5)
        
        def clear_age_placeholder(event):
            if self.age_year_entry.get() == "GG.AA.YYYY":
                self.age_year_entry.delete(0, tk.END)
                self.age_year_entry.config(fg=self.ui.fg_color)
                
        def add_age_placeholder(event):
            if getattr(self.ui, 'context_menu_open', False):
                return
            if not self.age_year_entry.get().strip():
                self.age_year_entry.insert(0, "GG.AA.YYYY")
                self.age_year_entry.config(fg=self.ui.text_placeholder)

        age_btn = tk.Button(age_frame, text="HESAPLA", font=self.ui.font_bold, bg=self.ui.accent_color, fg=self.ui.shadow_light, 
                                 bd=2, relief="raised", activebackground=self.ui.accent_hover, activeforeground=self.ui.shadow_light, cursor="hand2", command=self.calculate_age)
        age_btn.grid(row=0, column=2, padx=10, sticky="nsew", pady=(5, 2), ipadx=10)
        
        age_clear_btn = tk.Button(age_frame, text="Temizle", font=(self.ui.font_main[0], 8), bg=self.ui.bg_secondary, fg=self.ui.text_secondary, 
                                     bd=1, relief="raised", activebackground=self.ui.border_color, cursor="hand2", command=self.clear_data)
        age_clear_btn.grid(row=1, column=2, padx=10, sticky="nsew", pady=(2, 5))
        
        age_res_frame = tk.Frame(frame, bg=self.ui.bg_color)
        age_res_frame.pack(fill="x", pady=(15, 0))
        
        self.age_res_txt = tk.Text(age_res_frame, font=self.ui.font_main, fg=self.ui.fg_color, bg=self.ui.bg_color, cursor="hand2", wrap="word", bd=0, highlightthickness=0, height=10)
        self.age_res_txt.pack(anchor="w", fill="x", padx=5, pady=5)
        self.age_res_txt.tag_configure("bold", font=self.ui.font_bold)
        self.age_res_txt.insert("1.0", "-")
        self.age_res_txt.config(state="disabled")
        self.age_res_txt.bind('<Button-1>', self.copy_age_rate)
            
        self.age_info_lbl = tk.Label(frame, text="Analiz raporunu görmek için doğum tarihinizi girin", font=self.ui.font_main, fg=self.ui.text_secondary, bg=self.ui.bg_color)
        self.age_info_lbl.pack(pady=(15, 0))
        
        self.age_year_entry.bind('<Return>', self.calculate_age)
        self.age_year_entry.bind('<FocusIn>', clear_age_placeholder)
        self.age_year_entry.bind('<FocusOut>', add_age_placeholder)
        
        return frame

    def calculate_tax(self, event=None):
        amount_str = self.tax_amount_entry.get().strip()
        rate_str = self.tax_rate_entry.get().strip()
        
        amount_numbers = MatematikMotoru.metinden_sayilari_ayikla(amount_str)
        rate_numbers = MatematikMotoru.metinden_sayilari_ayikla(rate_str)
        
        if not amount_numbers:
            for lbl in self.tax_labels.values():
                lbl.config(text="-")
            self.tax_info_lbl.config(text="Geçersiz tutar!", fg=self.ui.error_color)
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
            for lbl in self.discount_labels.values():
                lbl.config(text="-")
            self.discount_info_lbl.config(text="Geçersiz tutar!", fg=self.ui.error_color)
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
            self.change_res_lbl.config(text="-")
            self.change_info_lbl.config(text="Eski ve yeni değer eksik!", fg=self.ui.error_color)
            return "break"
            
        old_val = old_nums[0]
        new_val = new_nums[0]
        
        result = FinansMotoru.degisim_orani_hesapla(old_val, new_val)
        oran = result["degisim_orani"]
        
        sembol = "+" if oran > 0 else ""
        self.change_res_lbl.config(text=f"%{sembol}{oran}")
        self.change_info_lbl.config(text="Hesaplandı • Kopyalamak için sonuca tıklayın", fg=self.ui.accent_color)
        return "break"

    def calculate_proportion(self, event=None):
        a_str = self.prop_a_entry.get().strip()
        b_str = self.prop_b_entry.get().strip()
        c_str = self.prop_c_entry.get().strip()
        
        a_nums = MatematikMotoru.metinden_sayilari_ayikla(a_str)
        b_nums = MatematikMotoru.metinden_sayilari_ayikla(b_str)
        c_nums = MatematikMotoru.metinden_sayilari_ayikla(c_str)
        
        if not a_nums or not b_nums or not c_nums:
            self.prop_res_lbl.config(text="-")
            self.prop_info_lbl.config(text="Lütfen üç değeri de eksiksiz girin!", fg=self.ui.error_color)
            return "break"
            
        result = FinansMotoru.oranti_hesapla(a_nums[0], b_nums[0], c_nums[0])
        
        if "hata" in result:
            self.prop_res_lbl.config(text="-")
            self.prop_info_lbl.config(text="1. Değer (A) sıfır olamaz!", fg=self.ui.error_color)
            self.prop_res_lbl.config(text="-")
            return "break"
            
        self.prop_res_lbl.config(text=str(result["sonuc"]))
        self.prop_info_lbl.config(text="Hesaplandı • Kopyalamak için sonuca tıklayın", fg=self.ui.accent_color)
        return "break"

    def calculate_age(self, event=None):
        date_str = self.age_year_entry.get().strip()
        if date_str == "GG.AA.YYYY":
            date_str = ""
        
        if not date_str:
            self.age_res_txt.config(state="normal")
            self.age_res_txt.delete("1.0", tk.END)
            self.age_res_txt.insert("1.0", "-")
            self.age_res_txt.config(state="disabled")
            self.age_info_lbl.config(text="Lütfen doğum tarihinizi girin!", fg=self.ui.error_color)
            return "break"
            
        result = FinansMotoru.yas_hesapla(date_str)
        
        if "hata" in result:
            if result["hata"] == "Gelecek tarih":
                self.age_info_lbl.config(text="Gelecek bir tarih giremezsiniz!", fg=self.ui.error_color)
            else:
                self.age_info_lbl.config(text="Geçersiz format! Örn: 15.05.1990", fg=self.ui.error_color)
            
            self.age_res_txt.config(state="normal")
            self.age_res_txt.delete("1.0", tk.END)
            self.age_res_txt.insert("1.0", "-")
            self.age_res_txt.config(state="disabled")
            return "break"
            
        self.age_res_txt.config(state="normal")
        self.age_res_txt.delete("1.0", tk.END)

        self.age_res_txt.insert(tk.END, "• Tam Yaşınız: ")
        self.age_res_txt.insert(tk.END, f"{result['yillar']}", "bold")
        self.age_res_txt.insert(tk.END, " yıl, ")
        self.age_res_txt.insert(tk.END, f"{result['aylar']}", "bold")
        self.age_res_txt.insert(tk.END, " ay, ")
        self.age_res_txt.insert(tk.END, f"{result['gunler']}", "bold")
        self.age_res_txt.insert(tk.END, " gün\n\n")

        self.age_res_txt.insert(tk.END, "• Gün Alma Durumu: ")
        self.age_res_txt.insert(tk.END, f"{result['yillar']}", "bold")
        self.age_res_txt.insert(tk.END, " yaşınızı doldurdunuz ve ")
        self.age_res_txt.insert(tk.END, f"{int(result['yillar']) + 1}", "bold")
        self.age_res_txt.insert(tk.END, " yaşından gün alıyorsunuz.\n\n")

        self.age_res_txt.insert(tk.END, "• Doğduğunuz Gün: ")
        self.age_res_txt.insert(tk.END, f"{result['dogum_gunu_str']}", "bold")
        self.age_res_txt.insert(tk.END, "\n\n")

        self.age_res_txt.insert(tk.END, "• Sonraki Doğum Günü: ")
        self.age_res_txt.insert(tk.END, f"{result['sonraki_dogum_gunu_str']}", "bold")
        self.age_res_txt.insert(tk.END, f" ({result['kalan_gun']} gün kaldı)\n\n")

        self.age_res_txt.insert(tk.END, "• Yaşanılan Gün Sayısı: Bugüne kadar tam ")
        self.age_res_txt.insert(tk.END, f"{result['yasanilan_gun_str']}", "bold")
        self.age_res_txt.insert(tk.END, " gün yaşadınız.")

        self.age_res_txt.config(state="disabled")
        self.age_info_lbl.config(text="Hesaplandı • Kopyalamak için sonuca tıklayın", fg=self.ui.accent_color)
        return "break"

    def copy_prop_rate(self, event=None):
        result = self.prop_res_lbl.cget("text")
        if result != "-":
            self.ui.root.clipboard_clear()
            self.ui.root.clipboard_append(result)
            self.ui.root.update()
            self.prop_info_lbl.config(text="Kopyalandı!", fg=self.ui.accent_color)
            self.ui.root.after(1500, lambda: self.prop_info_lbl.config(text="Hesaplandı • Kopyalamak için sonuca tıklayın", fg=self.ui.accent_color))

    def copy_age_rate(self, event=None):
        result = self.age_res_txt.get("1.0", "end-1c").strip()
        if result != "-":
            self.ui.root.clipboard_clear()
            self.ui.root.clipboard_append(result)
            self.ui.root.update()
            self.age_info_lbl.config(text="Kopyalandı!", fg=self.ui.accent_color)
            self.ui.root.after(1500, lambda: self.age_info_lbl.config(text="Hesaplandı • Kopyalamak için sonuca tıklayın", fg=self.ui.accent_color))

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
        self.tax_info_lbl.config(text="KDV hesaplamak için tutarı girin", fg=self.ui.text_secondary)
        
        self.discount_amount_entry.delete(0, tk.END)
        self.discount_rate_entry.delete(0, tk.END)
        self.discount_rate_entry.insert(0, "10")
        for lbl in self.discount_labels.values(): lbl.config(text="-")
        self.discount_info_lbl.config(text="İndirim hesaplamak için tutarı girin", fg=self.ui.text_secondary)
        
        self.old_val_entry.delete(0, tk.END)
        self.new_val_entry.delete(0, tk.END)
        self.change_res_lbl.config(text="-")
        self.change_info_lbl.config(text="Artış veya azalışı görmek için değerleri girin", fg=self.ui.text_secondary)
        
        self.prop_a_entry.delete(0, tk.END)
        self.prop_b_entry.delete(0, tk.END)
        self.prop_c_entry.delete(0, tk.END)
        self.prop_res_lbl.config(text="-")
        self.prop_info_lbl.config(text="Orantı sonucunu görmek için değerleri girin", fg=self.ui.text_secondary)
        
        self.age_year_entry.delete(0, tk.END)
        self.age_year_entry.insert(0, "GG.AA.YYYY")
        self.age_year_entry.config(fg=self.ui.text_placeholder)
        self.age_res_txt.config(state="normal")
        self.age_res_txt.delete("1.0", tk.END)
        self.age_res_txt.insert("1.0", "-")
        self.age_res_txt.config(state="disabled")
        self.age_info_lbl.config(text="Örn: 15.05.1990 şeklinde tarihinizi girin", fg=self.ui.text_secondary)