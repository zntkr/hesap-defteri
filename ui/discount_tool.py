import tkinter as tk
from typing import Optional
from core.finans_motoru import FinansMotoru
from ui.base_tool import BaseToolWidget

class DiscountToolWidget(BaseToolWidget):
    def get_short_name(self) -> str: return "İSKONTO"
    def get_name(self) -> str: return "İndirim Hesaplayıcı"

    def build_ui(self) -> None:
        self._build_header(self, "Örn: 2.500 TL'lik bir malın %15 indirim yapıldığında indirimli fiyatını ve indirim miktarını hesaplar.")
        discount_frame = tk.Frame(self, bg=self.ui.bg_secondary)
        discount_frame.pack(fill="x", pady=8)

        self.discount_amount_entry = self._build_input_row(discount_frame, 0, "Tutar:")
        self.discount_rate_entry = self._build_input_row(discount_frame, 1, "İndirim (%):", "10")
        self._build_action_buttons(discount_frame, self.calculate_discount, self.clear_data)

        discount_res_frame = tk.Frame(self, bg=self.ui.bg_secondary)
        discount_res_frame.pack(fill="x", pady=(16, 0))

        self._build_result_labels(discount_res_frame, [
            ("Fiyat:", "ham_tutar"),
            ("İndirim Miktarı:", "indirim_tutari"),
            ("İndirimli Fiyat:", "net_tutar"),
        ])
        
        self.result_labels["net_tutar"].config(font=self.ui.font_title)

        self._build_info_label(self, "İndirim hesaplamak için tutarı girin")
        self.discount_amount_entry.bind('<Return>', self.calculate_discount)
        self.discount_rate_entry.bind('<Return>', self.calculate_discount)
        self.primary_input = self.discount_amount_entry

    def calculate_discount(self, event: Optional[tk.Event] = None) -> Optional[str]:
        amount_numbers = self._get_numbers(self.discount_amount_entry)
        rate_numbers = self._get_numbers(self.discount_rate_entry)

        if not amount_numbers:
            for lbl in self.result_labels.values(): lbl.config(text="-")
            if self.info_lbl: self.info_lbl.config(text="Geçersiz tutar!", fg=self.ui.error_color)
            return "break"

        result = FinansMotoru.indirim_hesapla(amount_numbers[0], rate_numbers[0] if rate_numbers else 10.0)
        for key, lbl in self.result_labels.items(): lbl.config(text=str(result[key]))
        if self.info_lbl: self.info_lbl.config(text="İndirim hesaplandı", fg=self.ui.accent_color)
        self.ui.add_to_tape("İNDİRİM HESABI", f"Tutar: {amount_numbers[0]:g}\nİndirim: %{rate_numbers[0] if rate_numbers else 10.0:g}", str(result['net_tutar']))
        return "break"
