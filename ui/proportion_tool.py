import tkinter as tk
from typing import Optional
from core.finans_motoru import FinansMotoru
from ui.base_tool import BaseToolWidget

class ProportionToolWidget(BaseToolWidget):
    def get_short_name(self) -> str: return self.ui.lang["prop_short"]
    def get_name(self) -> str: return self.ui.lang["prop_name"]

    def build_ui(self) -> None:
        L = self.ui.lang
        self._build_header(self, L["prop_desc"])
        prop_frame = tk.Frame(self, bg=self.ui.bg_secondary)
        prop_frame.pack(fill="x", pady=8)

        self.prop_a_entry = self._build_input_row(prop_frame, 0, L["prop_label_a"], width=12)
        self.prop_b_entry = self._build_input_row(prop_frame, 1, L["prop_label_b"], width=12)
        self.prop_c_entry = self._build_input_row(prop_frame, 2, L["prop_label_c"], width=12)
        self._build_action_buttons(prop_frame, self.calculate_proportion, self.clear_data)

        prop_res_frame = tk.Frame(self, bg=self.ui.bg_secondary)
        prop_res_frame.pack(fill="x", pady=(13, 0))

        tk.Label(prop_res_frame, text=L["prop_label_result"], fg=self.ui.text_secondary, bg=self.ui.bg_secondary, font=self.ui.font_main).grid(row=0, column=0, sticky="w", pady=4)
        self.prop_res_lbl = tk.Label(prop_res_frame, text="-", font=self.ui.font_title, fg=self.ui.fg_color, bg=self.ui.bg_secondary)
        self.prop_res_lbl.grid(row=0, column=1, sticky="w", padx=24)
        self._make_label_clickable(self.prop_res_lbl)
        self.result_labels["sonuc"] = self.prop_res_lbl

        self._build_info_label(self, L["prop_info_default"])
        self.prop_a_entry.bind('<Return>', self.calculate_proportion)
        self.prop_b_entry.bind('<Return>', self.calculate_proportion)
        self.prop_c_entry.bind('<Return>', self.calculate_proportion)
        self.primary_input = self.prop_a_entry

    def calculate_proportion(self, event: Optional[tk.Event] = None) -> Optional[str]:
        if event and not self.flash_calc_button():
            return "break"
        L = self.ui.lang
        a_nums = self._get_numbers(self.prop_a_entry)
        b_nums = self._get_numbers(self.prop_b_entry)
        c_nums = self._get_numbers(self.prop_c_entry)

        if not a_nums and not b_nums and not c_nums:
            self.prop_res_lbl.config(text="-")
            self.show_message(L["prop_info_error_missing"], "error")
            return "break"
        elif not a_nums:
            self.prop_res_lbl.config(text="-")
            self.show_message(L["prop_info_err_a"], "error")
            return "break"
        elif not b_nums:
            self.prop_res_lbl.config(text="-")
            self.show_message(L["prop_info_err_b"], "error")
            return "break"
        elif not c_nums:
            self.prop_res_lbl.config(text="-")
            self.show_message(L["prop_info_err_c"], "error")
            return "break"

        result = FinansMotoru.oranti_hesapla(a_nums[0], b_nums[0], c_nums[0])
        if "hata" in result:
            self.prop_res_lbl.config(text="-")
            self.show_message(L["prop_info_error_zero"], "error")
            return "break"

        self.prop_res_lbl.config(text=self.format_number(result["sonuc"]))
        self.flash_result(self.prop_res_lbl)
        self.show_message(self._MSG_HESAPLANDI, "success", transient=True)
        self.ui.add_to_tape(
            L["prop_tape_title"],
            f"A: {self.format_number(a_nums[0])}\nB: {self.format_number(b_nums[0])}\nC: {self.format_number(c_nums[0])}",
            self.format_number(result['sonuc']),
        )
        return "break"
