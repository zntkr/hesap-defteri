import tkinter as tk
from typing import Optional
from core.matematik_motoru import MatematikMotoru
from core.finans_motoru import FinansMotoru
from ui.base_tool import BaseToolWidget

class DiscountToolWidget(BaseToolWidget):
    def get_name(self) -> str: return "İndirim Hesaplayıcı"

    def build_ui(self) -> None:
        self._build_header(self, "İndirim Hesaplayıcı", "Örn: 2.500 TL'lik bir ürüne %15 indirim uygulandığında net fiyatı ve indirim tutarını gösterir.")
        discount_frame = tk.Frame(self, bg=self.ui.bg_color)
        discount_frame.pack(fill="x", pady=5)
        
        self.discount_amount_entry = self._build_input_row(discount_frame, 0, "Tutar:")
        self.discount_rate_entry = self._build_input_row(discount_frame, 1, "İndirim (%):", "10")
        self._build_action_buttons(discount_frame, self.calculate_discount, self.clear_data)
        
        discount_res_frame = tk.Frame(self, bg=self.ui.bg_color)
        discount_res_frame.pack(fill="x", pady=(10, 0))
        
        self.discount_labels = {}
        discount_items = [("Ham Tutar:", "ham_tutar"), ("İndirim Tutarı:", "indirim_tutari"), ("Net Tutar:", "net_tutar")]
        for i, (text, key) in enumerate(discount_items):
            tk.Label(discount_res_frame, text=text, fg=self.ui.text_secondary, bg=self.ui.bg_color, font=self.ui.font_main).grid(row=i, column=0, sticky="w", pady=4)
            lbl = tk.Label(discount_res_frame, text="-", font=self.ui.font_bold, fg=self.ui.fg_color, bg=self.ui.bg_color)
            lbl.grid(row=i, column=1, sticky="w", padx=20)
            self.discount_labels[key] = lbl
            
        self.discount_info_lbl = self._build_info_label(self, "İndirim hesaplamak için tutarı girin")
        self.discount_amount_entry.bind('<Return>', self.calculate_discount)
        self.discount_rate_entry.bind('<Return>', self.calculate_discount)
        self.primary_input = self.discount_amount_entry

    def calculate_discount(self, event: Optional[tk.Event] = None) -> Optional[str]:
        amount_numbers = MatematikMotoru.metinden_sayilari_ayikla(self.discount_amount_entry.get().strip())
        rate_numbers = MatematikMotoru.metinden_sayilari_ayikla(self.discount_rate_entry.get().strip())
        
        if not amount_numbers:
            for lbl in self.discount_labels.values(): lbl.config(text="-")
            self.discount_info_lbl.config(text="Geçersiz tutar!", fg=self.ui.error_color)
            return "break"
            
        result = FinansMotoru.indirim_hesapla(amount_numbers[0], rate_numbers[0] if rate_numbers else 10.0)
        for key, lbl in self.discount_labels.items(): lbl.config(text=str(result[key]))
        self.discount_info_lbl.config(text="İndirim hesaplandı", fg=self.ui.accent_color)
        return "break"

    def clear_data(self) -> None:
        self.discount_amount_entry.delete(0, tk.END)
        self.discount_rate_entry.delete(0, tk.END)
        self.discount_rate_entry.insert(0, "10")
        for lbl in self.discount_labels.values(): lbl.config(text="-")
        self.discount_info_lbl.config(text="İndirim hesaplamak için tutarı girin", fg=self.ui.text_secondary)