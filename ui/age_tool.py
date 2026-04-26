import tkinter as tk
from typing import Optional
from core.finans_motoru import FinansMotoru
from ui.base_tool import BaseToolWidget

class AgeToolWidget(BaseToolWidget):
    def get_short_name(self) -> str: return self.ui.lang["age_short"]
    def get_name(self) -> str: return self.ui.lang["age_name"]

    def build_ui(self) -> None:
        L = self.ui.lang
        self._build_header(self, L["age_desc"])
        age_frame = tk.Frame(self, bg=self.ui.bg_secondary)
        age_frame.pack(fill="x", pady=8)

        self.age_year_entry = self._build_input_row(age_frame, 0, L["age_label_dob"], "")
        self._build_action_buttons(age_frame, self.calculate_age, self.clear_data)

        age_res_frame = tk.Frame(self, bg=self.ui.bg_secondary)
        age_res_frame.pack(fill="x", pady=(16, 0))

        self.age_res_txt = tk.Text(age_res_frame, font=self.ui.font_main, fg=self.ui.fg_color, bg=self.ui.bg_secondary, cursor="hand2", wrap="word", bd=0, highlightthickness=0, height=13, selectbackground=self.ui.shadow_dark, selectforeground=self.ui.fg_color)
        self.age_res_txt.pack(anchor="w", fill="x", padx=8, pady=8)
        self.age_res_txt.tag_configure("bold", font=self.ui.font_bold)
        self.age_res_txt.insert("1.0", "-")
        self.age_res_txt.config(state="disabled")
        self._make_clickable(self.age_res_txt)

        self._build_info_label(self, L["age_info_default"])

        self.age_year_entry.bind('<Return>', self.calculate_age)
        self.primary_input = self.age_year_entry

    def calculate_age(self, event: Optional[tk.Event] = None) -> Optional[str]:
        if event and not self.flash_calc_button():
            return "break"
        L = self.ui.lang
        date_str = self.age_year_entry.get().strip()

        if not date_str:
            self._set_result("-")
            self.show_message(L["age_info_error_empty"], "error")
            return "break"

        result = FinansMotoru.yas_hesapla(date_str, lang=self.ui.aktif_dil)
        if "hata" in result:
            err_msg = L["age_info_error_future"] if result["hata"] == "Gelecek tarih" else L["age_info_error_format"]
            self.show_message(err_msg, "error")
            self._set_result("-")
            return "break"

        self.age_res_txt.config(state="normal")
        self.age_res_txt.delete("1.0", tk.END)
        self.age_res_txt.insert(tk.END, L["age_res_prefix"])
        self.age_res_txt.insert(tk.END, f"{result['yillar']}", "bold")
        self.age_res_txt.insert(tk.END, L["age_res_years"])
        self.age_res_txt.insert(tk.END, f"{result['aylar']}", "bold")
        self.age_res_txt.insert(tk.END, L["age_res_months"])
        self.age_res_txt.insert(tk.END, f"{result['gunler']}", "bold")
        self.age_res_txt.insert(tk.END, L["age_res_days_section"])
        self.age_res_txt.insert(tk.END, f"{result['yillar']}", "bold")
        self.age_res_txt.insert(tk.END, L["age_res_completed"])
        self.age_res_txt.insert(tk.END, f"{int(result['yillar']) + 1}", "bold")
        self.age_res_txt.insert(tk.END, L["age_res_taking"])
        self.age_res_txt.insert(tk.END, f"{result['dogum_gunu_str']}", "bold")
        self.age_res_txt.insert(tk.END, L["age_res_next_bd"])
        if result['kalan_gun'] == 0:
            self.age_res_txt.insert(tk.END, L.get("age_res_today_bd", "Bugün Doğum Gününüz! 🎂"), "bold")
        else:
            self.age_res_txt.insert(tk.END, f"{result['sonraki_dogum_gunu_str']}", "bold")
            self.age_res_txt.insert(tk.END, f" ({result['kalan_gun']} {L['age_res_days_left']})")
        self.age_res_txt.insert(tk.END, L["age_res_lived"])
        self.age_res_txt.insert(tk.END, f"{result['yasanilan_gun_str']}", "bold")
        self.age_res_txt.insert(tk.END, L["age_res_lived_end"])
        self.age_res_txt.config(state="disabled")
        self.flash_result(self.age_res_txt)

        self.show_message(L["age_info_ok"], "success", transient=True)
        self.ui.add_to_tape(
            L["age_tape_title"],
            f"{L['age_tape_born_label']}: {date_str}",
            f"{result['yillar']} {L['age_tape_years']}, {result['aylar']} {L['age_tape_months']}",
        )
        return "break"

    def _set_result(self, text: str) -> None:
        self.age_res_txt.config(state="normal")
        self.age_res_txt.delete("1.0", tk.END)
        self.age_res_txt.insert("1.0", text)
        self.age_res_txt.config(state="disabled")

    def clear_data(self, from_keyboard: bool = False) -> None:
        super().clear_data(from_keyboard=from_keyboard)
        self._set_result("-")
