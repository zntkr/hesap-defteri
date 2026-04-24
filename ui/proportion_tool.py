import tkinter as tk
from typing import Optional
from core.finans_motoru import FinansMotoru
from ui.base_tool import BaseToolWidget

class ProportionToolWidget(BaseToolWidget):
    def get_short_name(self) -> str: return "ORANTI"
    def get_name(self) -> str: return "Orantı Hesaplayıcı"

    def build_ui(self) -> None:
        self._build_header(self, "Örn: 150 adet mal 4.500 TL ise, 75 adet mal kaç TL yapar?")
        prop_frame = tk.Frame(self, bg=self.ui.bg_secondary)
        prop_frame.pack(fill="x", pady=8)

        self.prop_a_entry = self._build_input_row(prop_frame, 0, "1. Değer (A):", width=12)
        self.prop_b_entry = self._build_input_row(prop_frame, 1, "Karşılığı (B):", width=12)
        self.prop_c_entry = self._build_input_row(prop_frame, 2, "3. Değer (C):", width=12)
        self._build_action_buttons(prop_frame, self.calculate_proportion, self.clear_data)

        prop_res_frame = tk.Frame(self, bg=self.ui.bg_secondary)
        prop_res_frame.pack(fill="x", pady=(16, 0))

        tk.Label(prop_res_frame, text="Netice (X):", fg=self.ui.text_secondary, bg=self.ui.bg_secondary, font=self.ui.font_main).grid(row=0, column=0, sticky="w", pady=4)
        self.prop_res_lbl = tk.Label(prop_res_frame, text="-", font=self.ui.font_title, fg=self.ui.fg_color, bg=self.ui.bg_secondary)
        self.prop_res_lbl.grid(row=0, column=1, sticky="w", padx=24)
        self._make_label_clickable(self.prop_res_lbl)
        self.result_labels["sonuc"] = self.prop_res_lbl

        self._build_info_label(self, "Orantı sonucunu görmek için değerleri girin")
        self.prop_a_entry.bind('<Return>', self.calculate_proportion)
        self.prop_b_entry.bind('<Return>', self.calculate_proportion)
        self.prop_c_entry.bind('<Return>', self.calculate_proportion)
        self.primary_input = self.prop_a_entry

    def calculate_proportion(self, event: Optional[tk.Event] = None) -> Optional[str]:
        a_nums = self._get_numbers(self.prop_a_entry)
        b_nums = self._get_numbers(self.prop_b_entry)
        c_nums = self._get_numbers(self.prop_c_entry)

        if not a_nums or not b_nums or not c_nums:
            self.prop_res_lbl.config(text="-")
            self.info_lbl.config(text="Lütfen üç değeri de eksiksiz girin!", fg=self.ui.error_color)
            return "break"

        result = FinansMotoru.oranti_hesapla(a_nums[0], b_nums[0], c_nums[0])
        if "hata" in result:
            self.prop_res_lbl.config(text="-")
            self.info_lbl.config(text="1. Değer (A) sıfır olamaz!", fg=self.ui.error_color)
            return "break"

        self.prop_res_lbl.config(text=str(result["sonuc"]))
        self.info_lbl.config(text=self._MSG_HESAPLANDI, fg=self.ui.accent_color)
        return "break"
