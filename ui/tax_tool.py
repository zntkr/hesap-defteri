import tkinter as tk
from typing import Optional
from core.finans_motoru import FinansMotoru
from ui.base_tool import BaseToolWidget

class TaxToolWidget(BaseToolWidget):
    def get_short_name(self) -> str: return self.ui.lang["tax_short"]
    def get_name(self) -> str: return self.ui.lang["tax_name"]

    def build_ui(self) -> None:
        L = self.ui.lang
        self._build_header(self, L["tax_desc"])
        tax_frame = tk.Frame(self, bg=self.ui.bg_secondary)
        tax_frame.pack(fill="x", pady=8)

        self.tax_amount_entry = self._build_input_row(tax_frame, 0, L["tax_label_amount"])
        self.tax_rate_entry = self._build_input_row(tax_frame, 1, L["tax_label_rate"], "20")
        self._build_action_buttons(tax_frame, self.calculate_tax, self.clear_data)

        tax_res_frame = tk.Frame(self, bg=self.ui.bg_secondary)
        tax_res_frame.pack(fill="x", pady=(16, 0))

        self._build_result_labels(tax_res_frame, [
            (L["tax_label_gross"], "ham_tutar"),
            (L["tax_label_vat"], "kdv_tutari"),
            (L["tax_label_total"], "toplam"),
        ])

        self.result_labels["toplam"].config(font=self.ui.font_title)

        self._build_info_label(self, L["tax_info_default"])
        self.tax_amount_entry.bind('<Return>', self.calculate_tax)
        self.tax_rate_entry.bind('<Return>', self.calculate_tax)
        self.primary_input = self.tax_amount_entry

    def calculate_tax(self, event: Optional[tk.Event] = None) -> Optional[str]:
        L = self.ui.lang
        amount_numbers = self._get_numbers(self.tax_amount_entry)
        rate_numbers = self._get_numbers(self.tax_rate_entry)

        if not amount_numbers:
            for lbl in self.result_labels.values(): lbl.config(text="-")
            if self.info_lbl: self.info_lbl.config(text=L["tax_info_error"], fg=self.ui.error_color)
            return "break"

        rate = rate_numbers[0] if rate_numbers else 20.0
        result = FinansMotoru.kdv_hesapla(amount_numbers[0], rate)
        for key, lbl in self.result_labels.items(): 
            lbl.config(text=self.format_number(result[key]))
            self.flash_result(lbl)
        if self.info_lbl: self.info_lbl.config(text=L["tax_info_ok"], fg=self.ui.accent_color)
        self.ui.add_to_tape(
            L["tax_tape_title"],
            f"{L['tax_tape_amount']}: {self.format_number(amount_numbers[0])}\n{L['tax_tape_rate']}: {self.format_percentage(rate)}",
            self.format_number(result['toplam']),
        )
        return "break"
