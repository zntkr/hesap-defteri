import tkinter as tk
from tkinter import ttk
from typing import Optional
import re
from core.matematik_motoru import MatematikMotoru
from ui.base_tool import BaseToolWidget

class AverageToolWidget(BaseToolWidget):
    def get_name(self) -> str: return "Ortalama Hesaplayıcı"

    def build_ui(self) -> None:
        self._build_header(self, "Metin içindeki sayıları ayıklayıp ortalamasını ve istatistiklerini hesaplar.")
        input_frame = tk.Frame(self, bg=self.ui.bg_secondary)
        input_frame.pack(fill="x", pady=5)
        
        text_wrapper = tk.Frame(input_frame, bg=self.ui.bg_secondary)
        text_wrapper.grid(row=0, column=0, columnspan=2, rowspan=2, sticky="nsew", padx=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        self.avg_char_count_lbl = tk.Label(text_wrapper, text="0 / 5.000", font=(self.ui.font_main[0], 8), fg=self.ui.text_disabled, bg=self.ui.bg_secondary)
        self.avg_char_count_lbl.pack(side="bottom", anchor="e")

        scrollbar = ttk.Scrollbar(text_wrapper)
        scrollbar.pack(side="right", fill="y")
        
        self.avg_text_input = tk.Text(text_wrapper, height=3, width=10, font=self.ui.font_main, bg=self.ui.shadow_light, fg=self.ui.text_placeholder, bd=1, relief="solid", wrap="word", yscrollcommand=scrollbar.set, selectbackground=self.ui.accent_light, selectforeground=self.ui.shadow_light)
        self.avg_text_input.insert("1.0", self.ui.placeholder_text)
        self.avg_text_input.pack(side="left", fill="both", expand=True)
        self.avg_text_input.tag_configure("detected_number", font=self.ui.font_bold, foreground=self.ui.accent_color)
        scrollbar.config(command=self.avg_text_input.yview)
        
        self.avg_text_input.bind('<KeyPress>', self.clear_avg_placeholder)
        self.avg_text_input.bind('<Button-1>', self.clear_avg_placeholder)
        self.avg_text_input.bind('<FocusIn>', self.clear_avg_placeholder)
        self.avg_text_input.bind('<FocusOut>', self.add_avg_placeholder)
        self.avg_text_input.bind('<KeyRelease>', self.update_avg_char_count)
        self.avg_text_input.bind('<<Paste>>', lambda e: self.ui.root.after(10, self.update_avg_char_count))
        self.avg_text_input.bind('<<Cut>>', lambda e: self.ui.root.after(10, self.update_avg_char_count))
        self.avg_text_input.bind('<Return>', self.calculate_average)

        self._build_action_buttons(input_frame, self.calculate_average, lambda: self.clear_data(keep_input=False))
        
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=(10, 5))
        
        res_frame = tk.Frame(self, bg=self.ui.bg_secondary)
        res_frame.pack(fill="both", expand=True)
        
        top_res_frame = tk.Frame(res_frame, bg=self.ui.bg_secondary)
        top_res_frame.pack(fill="x")
        
        tk.Label(top_res_frame, text="Ortalama:", fg=self.ui.text_secondary, bg=self.ui.bg_secondary, font=self.ui.font_main).grid(row=0, column=0, sticky="w", pady=4)
        self.avg_result_lbl = tk.Label(top_res_frame, text="-", font=self.ui.font_title, fg=self.ui.fg_color, bg=self.ui.bg_secondary, cursor="hand2")
        self.avg_result_lbl.grid(row=0, column=1, sticky="w", padx=20)
        self.avg_result_lbl.bind('<Button-1>', lambda e: self.copy_to_clipboard(self.avg_result_lbl.cget("text")))
        
        tk.Label(top_res_frame, text="Toplam:", fg=self.ui.text_secondary, bg=self.ui.bg_secondary, font=self.ui.font_main).grid(row=1, column=0, sticky="w", pady=4)
        self.avg_sum_lbl = tk.Label(top_res_frame, text="-", font=self.ui.font_bold, fg=self.ui.fg_color, bg=self.ui.bg_secondary, cursor="hand2")
        self.avg_sum_lbl.grid(row=1, column=1, sticky="w", padx=20)
        self.avg_sum_lbl.bind('<Button-1>', lambda e: self.copy_to_clipboard(self.avg_sum_lbl.cget("text")))
        
        stats_frame = tk.Frame(res_frame, bg=self.ui.bg_secondary)
        stats_frame.pack(fill="x", pady=(15, 0))
        
        self.avg_stats_labels = {}
        items = [("VERİ ADEDİ:", "adet"), ("MEDYAN:", "medyan"), ("EN BÜYÜK:", "en_buyuk"), ("AÇIKLIK (FARK):", "aciklik"), ("EN KÜÇÜK:", "en_kucuk"), ("STD. SAPMA:", "std_sapma")]
        
        for i, (text, key) in enumerate(items):
            row, col = i // 2, (i % 2) * 2
            tk.Label(stats_frame, text=text, fg=self.ui.text_secondary, bg=self.ui.bg_secondary, font=self.ui.font_main).grid(row=row, column=col, sticky="w", pady=4, padx=(30 if col == 2 else 0, 5))
            lbl = tk.Label(stats_frame, text="-", font=self.ui.font_bold, fg=self.ui.fg_color, bg=self.ui.bg_secondary, cursor="hand2")
            lbl.grid(row=row, column=col+1, sticky="w")
            lbl.bind('<Button-1>', lambda e, l=lbl: self.copy_to_clipboard(l.cget("text")))
            self.avg_stats_labels[key] = lbl


        
        self._build_info_label(self, "Sayıları yapıştırıp Enter'a basın", pad_y=(15, 0))
        self.primary_input = self.avg_text_input

    def clear_avg_placeholder(self, event: Optional[tk.Event] = None) -> Optional[str]:
        is_placeholder = (self.avg_text_input.get("1.0", "end-1c") == self.ui.placeholder_text)
        if is_placeholder:
            self.avg_text_input.delete("1.0", tk.END)
            self.avg_text_input.config(fg=self.ui.fg_color)
            self.avg_text_input.mark_set("insert", "1.0")
        self.ui.root.after(10, self.update_avg_char_count)
        if is_placeholder and event and event.type == tk.EventType.ButtonPress: return "break"

    def add_avg_placeholder(self, event: Optional[tk.Event] = None) -> None:
        if getattr(self.ui, 'context_menu_open', False): return
        if not self.avg_text_input.get("1.0", tk.END).strip():
            self.avg_text_input.delete("1.0", tk.END)
            self.avg_text_input.insert("1.0", self.ui.placeholder_text)
            self.avg_text_input.config(fg=self.ui.text_placeholder)
        self.update_avg_char_count()

    def update_avg_char_count(self, event: Optional[tk.Event] = None) -> None:
        text = self.avg_text_input.get("1.0", "end-1c")
        count = 0 if text == self.ui.placeholder_text else len(text)
        color = self.ui.error_color if count > 5000 else self.ui.text_disabled
        self.avg_char_count_lbl.config(text=f"{count:,}".replace(",", ".") + " / 5.000", fg=color)

    def calculate_average(self, event: Optional[tk.Event] = None) -> Optional[str]:
        full_text = self.avg_text_input.get("1.0", "end-1c")
        if full_text == self.ui.placeholder_text: full_text = ""
            
        raw_input = full_text.strip()
        
        # Hata olsa da olmasa da eski Regex vurgularını en baştan temizle
        self.avg_text_input.tag_remove("detected_number", "1.0", tk.END)
        
        if len(raw_input) > 5000:
            self.clear_data(keep_input=True)
            self.info_lbl.config(text="Limit aşıldı! En fazla 5.000 karakter girilebilir.", fg=self.ui.error_color)
            return "break"

        numbers = MatematikMotoru.metinden_sayilari_ayikla(raw_input)
        analysis = MatematikMotoru.detayli_analiz_yap(numbers)

        if analysis:
            self.avg_result_lbl.config(text=str(analysis["ortalama"]), fg=self.ui.fg_color)
            self.avg_sum_lbl.config(text=str(analysis['toplam']))
            self.info_lbl.config(text=f"{analysis['adet']} sayı hesaplandı • Kopyalamak için rakama tıklayın", fg=self.ui.accent_color)
            
            for key, lbl in self.avg_stats_labels.items():
                if key in analysis: lbl.config(text=str(analysis[key]))
                    

            
            for match in re.finditer(MatematikMotoru.SAYI_PATERNI, full_text):
                self.avg_text_input.tag_add("detected_number", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")
        else:
            self.clear_data(keep_input=True)
            self.info_lbl.config(text="Sayı bulunamadı veya geçersiz veri girişi!", fg=self.ui.error_color)
            
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