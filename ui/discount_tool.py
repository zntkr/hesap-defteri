import tkinter as tk
from typing import Optional
from core.finans_motoru import FinansMotoru
from ui.base_tool import BaseToolWidget

class DiscountToolWidget(BaseToolWidget):
    def get_short_name(self) -> str: return self.ui.lang["disc_short"]
    def get_name(self) -> str: return self.ui.lang["disc_name"]

    def build_ui(self) -> None:
        L = self.ui.lang
        self._build_header(self, L["disc_desc"])
        discount_frame = tk.Frame(self, bg=self.ui.bg_secondary)
        discount_frame.pack(fill="x", pady=8)

        self.discount_amount_entry = self._build_input_row(discount_frame, 0, L["disc_label_amount"])
        self.discount_rate_entry = self._build_input_row(discount_frame, 1, L["disc_label_rate"], "10")
        self._build_action_buttons(discount_frame, self.calculate_discount, self.clear_data)

        discount_res_frame = tk.Frame(self, bg=self.ui.bg_secondary)
        discount_res_frame.pack(fill="x", pady=(16, 0))

        self._build_result_labels(discount_res_frame, [
            (L["disc_label_price"], "ham_tutar"),
            (L["disc_label_discount"], "indirim_tutari"),
            (L["disc_label_net"], "net_tutar"),
        ])

        self.result_labels["net_tutar"].config(font=self.ui.font_title)

        self._build_info_label(self, L["disc_info_default"])
        self.discount_amount_entry.bind('<Return>', self.calculate_discount)
        self.discount_rate_entry.bind('<Return>', self.calculate_discount)
        self.primary_input = self.discount_amount_entry

    def calculate_discount(self, event: Optional[tk.Event] = None) -> Optional[str]:
        L = self.ui.lang
        amount_numbers = self._get_numbers(self.discount_amount_entry)
        rate_numbers = self._get_numbers(self.discount_rate_entry)

        if not amount_numbers:
            for lbl in self.result_labels.values(): lbl.config(text="-")
            if self.info_lbl: self.info_lbl.config(text=L["disc_info_error"], fg=self.ui.error_color)
            return "break"

        rate = rate_numbers[0] if rate_numbers else 10.0
        result = FinansMotoru.indirim_hesapla(amount_numbers[0], rate)
        for key, lbl in self.result_labels.items(): 
            lbl.config(text=self.format_number(result[key]))
            self.flash_result(lbl)
        if self.info_lbl: self.info_lbl.config(text=L["disc_info_ok"], fg=self.ui.accent_color)
        self.ui.add_to_tape(
            L["disc_tape_title"],
            f"{L['disc_tape_amount']}: {self.format_number(amount_numbers[0])}\n{L['disc_tape_rate']}: {self.format_percentage(rate)}",
            self.format_number(result['net_tutar']),
        )
        return "break"
