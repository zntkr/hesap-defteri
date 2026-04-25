import tkinter as tk
from typing import Optional
from core.finans_motoru import FinansMotoru
from ui.base_tool import BaseToolWidget

class ChangeToolWidget(BaseToolWidget):
    def get_short_name(self) -> str: return self.ui.lang["chng_short"]
    def get_name(self) -> str: return self.ui.lang["chng_name"]

    def build_ui(self) -> None:
        L = self.ui.lang
        self._build_header(self, L["chng_desc"])
        change_frame = tk.Frame(self, bg=self.ui.bg_secondary)
        change_frame.pack(fill="x", pady=8)

        self.old_val_entry = self._build_input_row(change_frame, 0, L["chng_label_old"])
        self.new_val_entry = self._build_input_row(change_frame, 1, L["chng_label_new"])
        self._build_action_buttons(change_frame, self.calculate_change, self.clear_data)

        change_res_frame = tk.Frame(self, bg=self.ui.bg_secondary)
        change_res_frame.pack(fill="x", pady=(16, 0))

        tk.Label(change_res_frame, text=L["chng_label_rate"], fg=self.ui.text_secondary, bg=self.ui.bg_secondary, font=self.ui.font_main).grid(row=0, column=0, sticky="w", pady=4)
        self.change_res_lbl = tk.Label(change_res_frame, text="-", font=self.ui.font_title, fg=self.ui.fg_color, bg=self.ui.bg_secondary)
        self.change_res_lbl.grid(row=0, column=1, sticky="w", padx=24)
        self._make_label_clickable(self.change_res_lbl)
        self.result_labels["degisim_orani"] = self.change_res_lbl

        self._build_info_label(self, L["chng_info_default"])
        self.old_val_entry.bind('<Return>', self.calculate_change)
        self.new_val_entry.bind('<Return>', self.calculate_change)
        self.primary_input = self.old_val_entry

    def calculate_change(self, event: Optional[tk.Event] = None) -> Optional[str]:
        L = self.ui.lang
        old_nums = self._get_numbers(self.old_val_entry)
        new_nums = self._get_numbers(self.new_val_entry)

        if not old_nums and not new_nums:
            self.change_res_lbl.config(text="-")
            self.show_message(L["chng_info_error"], "error")
            return "break"
        elif not old_nums:
            self.change_res_lbl.config(text="-")
            self.show_message(L["chng_info_err_old"], "error")
            return "break"
        elif not new_nums:
            self.change_res_lbl.config(text="-")
            self.show_message(L["chng_info_err_new"], "error")
            return "break"

        result = FinansMotoru.degisim_orani_hesapla(old_nums[0], new_nums[0])
        oran = result["degisim_orani"]
        
        isaret = '+' if oran > 0 else ''
        oran_str = self.format_percentage(oran, isaret)
        self.change_res_lbl.config(text=oran_str)
        self.flash_result(self.change_res_lbl)
        self.show_message(self._MSG_HESAPLANDI, "success", transient=True)
        self.ui.add_to_tape(
            L["chng_tape_title"],
            f"{L['chng_tape_old']}: {self.format_number(old_nums[0])}\n{L['chng_tape_new']}: {self.format_number(new_nums[0])}",
            oran_str,
        )
        return "break"
