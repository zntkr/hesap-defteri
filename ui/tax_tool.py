import tkinter as tk
from typing import Optional
from core.matematik_motoru import MatematikMotoru
from core.finans_motoru import FinansMotoru
from ui.base_tool import BaseToolWidget

class TaxToolWidget(BaseToolWidget):
    def get_short_name(self) -> str: return "KDV"
    def get_name(self) -> str: return "KDV Hesaplayıcı"

    def build_ui(self) -> None:
        self._build_header(self, "Örn: 1.500 TL tutar ve %20 oran girerek KDV payını ve toplam matrahı hesaplayabilirsiniz.")
        tax_frame = tk.Frame(self, bg=self.ui.bg_secondary)
        tax_frame.pack(fill="x", pady=5)
        
        self.tax_amount_entry = self._build_input_row(tax_frame, 0, "Tutar:")
        self.tax_rate_entry = self._build_input_row(tax_frame, 1, "Oran (%):", "20")
        self._build_action_buttons(tax_frame, self.calculate_tax, self.clear_data)
        
        tax_res_frame = tk.Frame(self, bg=self.ui.bg_secondary)
        tax_res_frame.pack(fill="x", pady=(15, 0))
        
        self.tax_labels = {}
        tax_items = [("Ham Tutar:", "ham_tutar"), ("KDV Tutarı:", "kdv_tutari"), ("Toplam Tutar:", "toplam")]
        for i, (text, key) in enumerate(tax_items):
            tk.Label(tax_res_frame, text=text, fg=self.ui.text_secondary, bg=self.ui.bg_secondary, font=self.ui.font_main).grid(row=i, column=0, sticky="w", pady=4)
            lbl = tk.Label(tax_res_frame, text="-", font=self.ui.font_bold, fg=self.ui.fg_color, bg=self.ui.bg_secondary, cursor="hand2")
            lbl.grid(row=i, column=1, sticky="w", padx=20)
            lbl.bind('<Button-1>', lambda e, l=lbl: self.copy_to_clipboard(l.cget("text")))
            self.tax_labels[key] = lbl
            
        self._build_info_label(self, "KDV hesaplamak için tutarı girin")
        self.tax_amount_entry.bind('<Return>', self.calculate_tax)
        self.tax_rate_entry.bind('<Return>', self.calculate_tax)
        self.primary_input = self.tax_amount_entry

    def calculate_tax(self, event: Optional[tk.Event] = None) -> Optional[str]:
        amount_numbers = MatematikMotoru.metinden_sayilari_ayikla(self.tax_amount_entry.get().strip())
        rate_numbers = MatematikMotoru.metinden_sayilari_ayikla(self.tax_rate_entry.get().strip())
        
        if not amount_numbers:
            for lbl in self.tax_labels.values(): lbl.config(text="-")
            self.info_lbl.config(text="Geçersiz tutar!", fg=self.ui.error_color)
            return "break"
            
        result = FinansMotoru.kdv_hesapla(amount_numbers[0], rate_numbers[0] if rate_numbers else 20.0)
        for key, lbl in self.tax_labels.items(): lbl.config(text=str(result[key]))
        self.info_lbl.config(text="KDV hesaplandı", fg=self.ui.accent_color)
        return "break"

    def clear_data(self) -> None:
        self.reset_defaults()
        for lbl in self.tax_labels.values(): lbl.config(text="-")