import tkinter as tk
from tkinter import ttk
from typing import Optional
import re
from core.matematik_motoru import MatematikMotoru
from ui.base_tool import BaseToolWidget

class AverageToolWidget(BaseToolWidget):
    def get_short_name(self) -> str: return "ORTALAMA"
    def get_name(self) -> str: return "Ortalama Hesaplayıcı"

    def build_ui(self) -> None:
        self._build_header(self, "Metin içindeki sayıları ayıklayıp ortalamasını ve istatistiklerini hesaplar.")
        input_frame = tk.Frame(self, bg=self.ui.bg_secondary)
        input_frame.pack(fill="x", pady=8)
        
        text_wrapper = tk.Frame(input_frame, bg=self.ui.bg_secondary)
        text_wrapper.grid(row=0, column=0, columnspan=2, rowspan=3, sticky="nsew", padx=(0, 8), pady=8)
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(2, weight=1)
        
        self.avg_char_count_lbl = tk.Label(text_wrapper, text="0 / 5.000", font=self.ui.font_small, fg=self.ui.text_disabled, bg=self.ui.bg_secondary)
        self.avg_char_count_lbl.pack(side="bottom", anchor="e")

        scrollbar = ttk.Scrollbar(text_wrapper)
        scrollbar.pack(side="right", fill="y")
        
        self.avg_text_input = tk.Text(text_wrapper, height=3, width=10, font=self.ui.font_main, bg=self.ui.input_bg, fg=self.ui.text_placeholder, bd=2, relief="sunken", wrap="word", yscrollcommand=scrollbar.set, selectbackground=self.ui.shadow_dark, selectforeground=self.ui.fg_color)
        self.avg_text_input.insert("1.0", self.ui.placeholder_text)
        self.avg_text_input.pack(side="left", fill="both", expand=True)
        self.avg_text_input.tag_configure("detected_number", font=self.ui.font_bold, foreground=self.ui.accent_color)
        scrollbar.config(command=self.avg_text_input.yview)
        
        self.avg_text_input.bind('<KeyPress>', self.clear_avg_placeholder)
        self.avg_text_input.bind('<Button-1>', self.clear_avg_placeholder)
        self.avg_text_input.bind('<FocusIn>', self.clear_avg_placeholder)
        self.avg_text_input.bind('<FocusOut>', self.add_avg_placeholder)
        self.avg_text_input.bind('<KeyRelease>', self.update_avg_char_count)
        self.avg_text_input.bind('<<Paste>>', self._handle_paste)
        self.avg_text_input.bind('<<Cut>>', lambda e: self.ui.root.after(10, self.update_avg_char_count))
        self.avg_text_input.bind('<Return>', self.calculate_average)

        self._build_action_buttons(input_frame, self.calculate_average, lambda: self.clear_data(keep_input=False), rowspan=3)
        
        res_frame = tk.Frame(self, bg=self.ui.bg_secondary)
        res_frame.pack(fill="x")
        
        top_res_frame = tk.Frame(res_frame, bg=self.ui.bg_secondary)
        top_res_frame.pack(fill="x")
        
        tk.Label(top_res_frame, text="Ortalama:", fg=self.ui.text_secondary, bg=self.ui.bg_secondary, font=self.ui.font_main).grid(row=0, column=0, sticky="w", pady=4)
        self.avg_result_lbl = tk.Label(top_res_frame, text="-", font=self.ui.font_title, fg=self.ui.fg_color, bg=self.ui.bg_secondary)
        self.avg_result_lbl.grid(row=0, column=1, sticky="w", padx=24)
        self._make_label_clickable(self.avg_result_lbl)

        tk.Label(top_res_frame, text="Toplam:", fg=self.ui.text_secondary, bg=self.ui.bg_secondary, font=self.ui.font_main).grid(row=1, column=0, sticky="w", pady=4)
        self.avg_sum_lbl = tk.Label(top_res_frame, text="-", font=self.ui.font_bold, fg=self.ui.fg_color, bg=self.ui.bg_secondary)
        self.avg_sum_lbl.grid(row=1, column=1, sticky="w", padx=24)
        self._make_label_clickable(self.avg_sum_lbl)
        
        stats_frame = tk.Frame(res_frame, bg=self.ui.bg_secondary)
        stats_frame.pack(fill="x", pady=(16, 0))
        
        self.avg_stats_labels = {}
        items = [("VERİ ADEDİ:", "adet"), ("MEDYAN:", "medyan"), ("EN BÜYÜK:", "en_buyuk"), ("AÇIKLIK (FARK):", "aciklik"), ("EN KÜÇÜK:", "en_kucuk"), ("STD. SAPMA:", "std_sapma")]
        
        for i, (text, key) in enumerate(items):
            row, col = i // 2, (i % 2) * 2
            tk.Label(stats_frame, text=text, fg=self.ui.text_secondary, bg=self.ui.bg_secondary, font=self.ui.font_main).grid(row=row, column=col, sticky="w", pady=4, padx=(16 if col == 2 else 0, 8))
            lbl = tk.Label(stats_frame, text="-", font=self.ui.font_bold, fg=self.ui.fg_color, bg=self.ui.bg_secondary)
            lbl.grid(row=row, column=col+1, sticky="w")
            self._make_label_clickable(lbl)
            self.avg_stats_labels[key] = lbl


        
        self._build_info_label(self, "Sayıları yapıştırıp Enter'a basın")
        self.primary_input = self.avg_text_input

    def clear_avg_placeholder(self, event: Optional[tk.Event] = None) -> Optional[str]:
        result = self._handle_text_focus_in(self.avg_text_input, self.ui.placeholder_text, event)
        self.ui.root.after(10, self.update_avg_char_count)
        return result

    def add_avg_placeholder(self, event: Optional[tk.Event] = None) -> None:
        self._handle_text_focus_out(self.avg_text_input, self.ui.placeholder_text)
        self.update_avg_char_count()

    def update_avg_char_count(self, event: Optional[tk.Event] = None) -> None:
        text = self.avg_text_input.get("1.0", "end-1c")
        count = 0 if text == self.ui.placeholder_text else len(text)
        color = self.ui.error_color if count > 5000 else self.ui.text_disabled
        self.avg_char_count_lbl.config(text=f"{count:,}".replace(",", ".") + " / 5.000", fg=color)

    def _handle_paste(self, event: Optional[tk.Event] = None) -> Optional[str]:
        try:
            clipboard_text = self.ui.root.clipboard_get()
        except tk.TclError:
            return "break"
            
        current_text = self.avg_text_input.get("1.0", "end-1c")
        is_placeholder = (current_text == self.ui.placeholder_text)
        
        try:
            sel_start = self.avg_text_input.index(tk.SEL_FIRST)
            sel_end = self.avg_text_input.index(tk.SEL_LAST)
            sel_len = len(self.avg_text_input.get(sel_start, sel_end))
        except tk.TclError:
            sel_len = 0
            
        current_len = 0 if is_placeholder else len(current_text)
        available_space = 5000 - (current_len - sel_len)
        
        if available_space <= 0:
            if self.info_lbl: self.info_lbl.config(text="Limit aşıldı! En fazla 5.000 karakter girilebilir.", fg=self.ui.error_color)
            return "break"
            
        if is_placeholder:
            self.avg_text_input.delete("1.0", tk.END)
            self.avg_text_input.config(fg=self.ui.fg_color)
            
        if len(clipboard_text) > available_space:
            clipboard_text = clipboard_text[:available_space]
            if self.info_lbl: self.info_lbl.config(text="Metin çok uzundu, 5.000 karaktere kırpılarak yapıştırıldı.", fg=self.ui.error_color)
            
        if sel_len > 0 and not is_placeholder:
            self.avg_text_input.delete(tk.SEL_FIRST, tk.SEL_LAST)
            
        self.avg_text_input.insert(tk.INSERT, clipboard_text)
        self.ui.root.after(10, self.update_avg_char_count)
        return "break"

    def calculate_average(self, event: Optional[tk.Event] = None) -> Optional[str]:
        full_text = self.avg_text_input.get("1.0", "end-1c")
        if full_text == self.ui.placeholder_text: full_text = ""
            
        raw_input = full_text.strip()
        
        # Hata olsa da olmasa da eski Regex vurgularını en baştan temizle
        self.avg_text_input.tag_remove("detected_number", "1.0", tk.END)
        
        if len(raw_input) > 5000:
            self.clear_data(keep_input=True)
            if self.info_lbl: self.info_lbl.config(text="Limit aşıldı! En fazla 5.000 karakter girilebilir.", fg=self.ui.error_color)
            return "break"

        numbers = MatematikMotoru.metinden_sayilari_ayikla(raw_input)
        analysis = MatematikMotoru.detayli_analiz_yap(numbers)

        if analysis:
            self.avg_result_lbl.config(text=str(analysis["ortalama"]), fg=self.ui.fg_color)
            self.avg_sum_lbl.config(text=str(analysis['toplam']))
            if self.info_lbl: self.info_lbl.config(text=f"{analysis['adet']} sayı hesaplandı • Kopyalamak için rakama tıklayın", fg=self.ui.accent_color)
            
            for key, lbl in self.avg_stats_labels.items():
                if key in analysis: lbl.config(text=str(analysis[key]))
                    

            
            for match in re.finditer(MatematikMotoru.SAYI_PATERNI, full_text):
                self.avg_text_input.tag_add("detected_number", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")
            self.ui.add_to_tape("ORTALAMA HESABI", f"Adet: {analysis['adet']}\nToplam: {analysis['toplam']}", str(analysis['ortalama']))
        else:
            self.clear_data(keep_input=True)
            if self.info_lbl: self.info_lbl.config(text="Sayı bulunamadı veya geçersiz veri girişi!", fg=self.ui.error_color)
            
        return "break"

    def clear_data(self, keep_input: bool = False) -> None:
        if not keep_input:
            self.avg_text_input.delete("1.0", tk.END)
            self.add_avg_placeholder()
        self.avg_text_input.tag_remove("detected_number", "1.0", tk.END)
        self.avg_result_lbl.config(text="-")
        self.avg_sum_lbl.config(text="-")
        self.reset_defaults()
        for lbl in self.avg_stats_labels.values(): lbl.config(text="-")