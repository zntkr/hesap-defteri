import tkinter as tk
from tkinter import ttk
from typing import Optional
import re
from core.matematik_motoru import MatematikMotoru
from ui.base_tool import BaseToolWidget

class AverageToolWidget(BaseToolWidget):
    def get_short_name(self) -> str: return self.ui.lang["avg_short"]
    def get_name(self) -> str: return self.ui.lang["avg_name"]

    def build_ui(self) -> None:
        L = self.ui.lang
        self._build_header(self, L["avg_desc"])
        input_frame = tk.Frame(self, bg=self.ui.bg_secondary)
        input_frame.pack(fill="x", pady=self.ui.s(8))

        text_wrapper = tk.Frame(input_frame, bg=self.ui.bg_secondary)
        text_wrapper.grid(row=0, column=0, columnspan=2, rowspan=2, sticky="nsew", padx=(0, self.ui.s(8)), pady=self.ui.s(4))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)
        input_frame.rowconfigure(1, weight=1)

        self.avg_char_count_lbl = tk.Label(text_wrapper, text="", font=self.ui.font_small, fg=self.ui.text_disabled, bg=self.ui.bg_secondary)
        self.avg_char_count_lbl.pack(side="bottom", anchor="e")

        scrollbar = ttk.Scrollbar(text_wrapper)
        scrollbar.pack(side="right", fill="y")

        self.avg_text_input = tk.Text(text_wrapper, height=2, width=10, font=self.ui.font_main, bg=self.ui.input_bg, fg=self.ui.fg_color, bd=2, relief="sunken", highlightthickness=1, highlightbackground=self.ui.bg_secondary, highlightcolor=self.ui.accent_color, wrap="word", yscrollcommand=scrollbar.set, selectbackground=self.ui.shadow_dark, selectforeground=self.ui.fg_color)
        self.avg_text_input.pack(side="left", fill="both", expand=True)
        self.avg_text_input.tag_configure("detected_number", font=self.ui.font_bold, foreground=self.ui.accent_color)
        self.avg_text_input.tag_configure("detected_scientific", font=self.ui.font_bold, foreground=self.ui.color_scientific)
        scrollbar.config(command=self.avg_text_input.yview)

        self.avg_text_input.bind('<KeyRelease>', self.update_avg_char_count)
        self.avg_text_input.bind('<<Paste>>', self._handle_paste)
        self.avg_text_input.bind('<<Cut>>', lambda e: self.ui.root.after(10, self.update_avg_char_count))
        self.avg_text_input.bind('<Return>', self.calculate_average)
        self.avg_text_input.bind('<Tab>', self._handle_tab)
        self.avg_text_input.bind('<Shift-Tab>', self._handle_shift_tab)

        self.calc_btn = tk.Button(input_frame, text=self.ui.lang["btn_calculate"], width=9, font=self.ui.font_bold, bg=self.ui.btn_bg, fg=self.ui.shadow_light, bd=2, relief="raised", activebackground=self.ui.btn_hover, activeforeground=self.ui.shadow_light, cursor="hand2", command=self.calculate_average)
        self.clear_btn = tk.Button(input_frame, text=self.ui.lang["btn_clear"], width=9, font=self.ui.font_small, bg=self.ui.bg_secondary, fg=self.ui.text_secondary, bd=1, relief="raised", activebackground=self.ui.tab_inactive_bg, cursor="hand2", command=lambda: self.clear_data(keep_input=False))
        self.calc_btn.grid(row=0, column=2, sticky="ew", padx=(self.ui.s(8), self.ui.s(16)), pady=self.ui.s(4))
        self.clear_btn.grid(row=1, column=2, sticky="ew", padx=(self.ui.s(8), self.ui.s(16)), pady=self.ui.s(4))
        for btn in (self.calc_btn, self.clear_btn):
            btn.bind("<Button-1>", lambda _, b=btn: b.config(relief="sunken"))
            btn.bind("<ButtonRelease-1>", lambda _, b=btn: b.config(relief="raised"))

        res_frame = tk.Frame(self, bg=self.ui.bg_secondary)
        res_frame.pack(fill="x")

        top_res_frame = tk.Frame(res_frame, bg=self.ui.bg_secondary)
        top_res_frame.pack(fill="x")

        tk.Label(top_res_frame, text=L["avg_label_avg"], fg=self.ui.text_secondary, bg=self.ui.bg_secondary, font=self.ui.font_main).grid(row=0, column=0, sticky="w", pady=self.ui.s(4))
        self.avg_result_lbl = tk.Label(top_res_frame, text="-", font=self.ui.font_title, fg=self.ui.fg_color, bg=self.ui.bg_secondary)
        self.avg_result_lbl.grid(row=0, column=1, sticky="w", padx=self.ui.s(8))
        self._make_label_clickable(self.avg_result_lbl)

        tk.Label(top_res_frame, text=L["avg_label_sum"], fg=self.ui.text_secondary, bg=self.ui.bg_secondary, font=self.ui.font_main).grid(row=1, column=0, sticky="w", pady=self.ui.s(4))
        self.avg_sum_lbl = tk.Label(top_res_frame, text="-", font=self.ui.font_bold, fg=self.ui.fg_color, bg=self.ui.bg_secondary)
        self.avg_sum_lbl.grid(row=1, column=1, sticky="w", padx=self.ui.s(8))
        self._make_label_clickable(self.avg_sum_lbl)

        top_res_frame.columnconfigure(0, minsize=self.ui.s(88))

        stats_frame = tk.Frame(res_frame, bg=self.ui.bg_secondary)
        stats_frame.pack(fill="x", pady=(self.ui.s(8), 0))

        self.avg_stats_labels = {}
        items = [
            (L["avg_stat_count"], "adet"),
            (L["avg_stat_median"], "medyan"),
            (L["avg_stat_max"], "en_buyuk"),
            (L["avg_stat_range"], "aciklik"),
            (L["avg_stat_min"], "en_kucuk"),
            (L["avg_stat_std"], "std_sapma"),
        ]

        stat_val_font = (self.ui.font_small[0], self.ui.font_small[1], "bold")
        for i, (text, key) in enumerate(items):
            tk.Label(stats_frame, text=text, fg=self.ui.text_secondary, bg=self.ui.bg_secondary, font=self.ui.font_small).grid(row=i, column=0, sticky="w", pady=self.ui.s(2))
            lbl = tk.Label(stats_frame, text="-", font=stat_val_font, fg=self.ui.fg_color, bg=self.ui.bg_secondary)
            lbl.grid(row=i, column=1, sticky="w", padx=self.ui.s(8))
            self._make_label_clickable(lbl)
            self.avg_stats_labels[key] = lbl
            
        stats_frame.columnconfigure(0, minsize=self.ui.s(88))

        self._build_info_label(self, L["avg_info_default"])
        self.primary_input = self.avg_text_input
        self.update_avg_char_count()

    def _handle_tab(self, event: tk.Event) -> str:
        next_widget = self.avg_text_input.tk_focusNext()
        if next_widget:
            next_widget.focus_set()
        return "break"

    def _handle_shift_tab(self, event: tk.Event) -> str:
        prev_widget = self.avg_text_input.tk_focusPrev()
        if prev_widget:
            prev_widget.focus_set()
        return "break"

    def update_avg_char_count(self, event: Optional[tk.Event] = None) -> None:
        text = self.avg_text_input.get("1.0", "end-1c")
        count = len(text)
        
        if count == 0:
            self.avg_char_count_lbl.config(text="") # Zen Modu: Kutu boşsa sayacı gizle
            return
            
        L = self.ui.lang
        if count <= 4000:
            color = self.ui.text_disabled
            count_str = f"{count:,} / 5,000" if self.ui.aktif_dil == "en" else f"{count:,}".replace(",", ".") + " / 5.000"
        elif count <= 5000:
            color = self.ui.accent_color
            count_str = L["avg_char_warning"].format(n=5000 - count)
        else:
            color = self.ui.error_color
            count_str = L["avg_char_over"].format(n=count - 5000)
            
        self.avg_char_count_lbl.config(text=count_str, fg=color)

    def _handle_paste(self, event: Optional[tk.Event] = None) -> Optional[str]:
        L = self.ui.lang
        try:
            clipboard_text = self.ui.root.clipboard_get()
        except tk.TclError:
            return "break"

        current_text = self.avg_text_input.get("1.0", "end-1c")

        try:
            sel_start = self.avg_text_input.index(tk.SEL_FIRST)
            sel_end = self.avg_text_input.index(tk.SEL_LAST)
            sel_len = len(self.avg_text_input.get(sel_start, sel_end))
        except tk.TclError:
            sel_len = 0

        current_len = len(current_text)
        available_space = 5000 - (current_len - sel_len)

        if available_space <= 0:
            self.show_message(L["avg_info_limit"], "error")
            return "break"

        if len(clipboard_text) > available_space:
            clipboard_text = clipboard_text[:available_space]
            self.show_message(L["avg_info_truncated"], "error", transient=True)

        if sel_len > 0:
            self.avg_text_input.delete(tk.SEL_FIRST, tk.SEL_LAST)

        self.avg_text_input.insert(tk.INSERT, clipboard_text)
        self.ui.root.after(10, self.update_avg_char_count)
        return "break"

    def calculate_average(self, event: Optional[tk.Event] = None) -> Optional[str]:
        if event and not self.flash_calc_button():
            return "break"
        L = self.ui.lang
        full_text = self.avg_text_input.get("1.0", "end-1c")

        raw_input = full_text.strip()
        self.avg_text_input.tag_remove("detected_number", "1.0", tk.END)
        self.avg_text_input.tag_remove("detected_scientific", "1.0", tk.END)

        if len(raw_input) > 5000:
            self.clear_data(keep_input=True)
            self.show_message(L["avg_info_limit"], "error")
            return "break"

        numbers = MatematikMotoru.metinden_sayilari_ayikla(raw_input)
        analysis = MatematikMotoru.detayli_analiz_yap(numbers)

        if analysis:
            self.avg_result_lbl.config(text=self.format_number(analysis["ortalama"]), fg=self.ui.fg_color)
            self.flash_result(self.avg_result_lbl)
            self.avg_sum_lbl.config(text=self.format_number(analysis['toplam']))
            self.flash_result(self.avg_sum_lbl)
            self.show_message(L["avg_info_result"].format(count=self.format_number(analysis['adet'])), "success", transient=True)

            for key, lbl in self.avg_stats_labels.items():
                if key in analysis:
                    val = analysis[key]
                    lbl.config(text=val if isinstance(val, str) else self.format_number(val))
                    self.flash_result(lbl)

            for match in MatematikMotoru.SAYI_PATERNI.finditer(full_text):
                tag_name = "detected_scientific" if "e" in match.group().lower() else "detected_number"
                self.avg_text_input.tag_add(tag_name, f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")
            self.ui.add_to_tape(
                L["avg_tape_title"],
                f"{L['avg_tape_count']}: {self.format_number(analysis['adet'])}\n{L['avg_tape_sum']}: {self.format_number(analysis['toplam'])}",
                self.format_number(analysis['ortalama']),
            )
        else:
            self.clear_data(keep_input=True)
            self.show_message(L["avg_info_error"], "error")

        return "break"

    def clear_data(self, from_keyboard: bool = False, keep_input: bool = False) -> None:
        if from_keyboard:
            self.flash_clear_button()
        if not keep_input:
            self.avg_text_input.delete("1.0", tk.END)
        self.avg_text_input.tag_remove("detected_number", "1.0", tk.END)
        self.avg_text_input.tag_remove("detected_scientific", "1.0", tk.END)
        self.avg_result_lbl.config(text="-")
        self.avg_sum_lbl.config(text="-")
        self.reset_defaults()
        for lbl in self.avg_stats_labels.values(): lbl.config(text="-")

        if not keep_input:
            self.avg_text_input.focus_set()
            self.update_avg_char_count()
