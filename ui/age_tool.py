import tkinter as tk
from typing import Optional
from core.finans_motoru import FinansMotoru
from ui.base_tool import BaseToolWidget

class AgeToolWidget(BaseToolWidget):
    def get_name(self) -> str: return "Yaş Hesaplayıcı"

    def build_ui(self) -> None:
        self._build_header(self, "Örn: 15.05.1990 girerek doğduğunuz günü, tam yaşınızı ve sonraki doğum gününüze kalan süreyi bulun.")
        age_frame = tk.Frame(self, bg=self.ui.bg_color)
        age_frame.pack(fill="x", pady=5)
        
        self.age_year_entry = self._build_input_row(age_frame, 0, "Doğum Tarihi:", self.ui.date_placeholder)
        self.age_year_entry.config(fg=self.ui.text_placeholder)
        self._build_action_buttons(age_frame, self.calculate_age, self.clear_data)
        
        age_res_frame = tk.Frame(self, bg=self.ui.bg_color)
        age_res_frame.pack(fill="x", pady=(15, 0))
        
        self.age_res_txt = tk.Text(age_res_frame, font=self.ui.font_main, fg=self.ui.fg_color, bg=self.ui.bg_color, cursor="hand2", wrap="word", bd=0, highlightthickness=0, height=10)
        self.age_res_txt.pack(anchor="w", fill="x", padx=5, pady=5)
        self.age_res_txt.tag_configure("bold", font=self.ui.font_bold)
        self.age_res_txt.insert("1.0", "-")
        self.age_res_txt.config(state="disabled")
        self.age_res_txt.bind('<Button-1>', lambda e: self.copy_to_clipboard(self.age_res_txt.get("1.0", "end-1c").strip()))
            
        self._build_info_label(self, "Yaş hesaplama raporu için doğum tarihinizi girin", pad_y=(15, 0))
        
        self.age_year_entry.bind('<Return>', self.calculate_age)
        self.age_year_entry.bind('<FocusIn>', self._clear_age_placeholder)
        self.age_year_entry.bind('<FocusOut>', self._add_age_placeholder)
        self.primary_input = self.age_year_entry

    def _clear_age_placeholder(self, event: tk.Event) -> None:
        if self.age_year_entry.get() == self.ui.date_placeholder:
            self.age_year_entry.delete(0, tk.END)
            self.age_year_entry.config(fg=self.ui.fg_color)
            
    def _add_age_placeholder(self, event: tk.Event) -> None:
        if getattr(self.ui, 'context_menu_open', False): return
        if not self.age_year_entry.get().strip():
            self.age_year_entry.insert(0, self.ui.date_placeholder)
            self.age_year_entry.config(fg=self.ui.text_placeholder)

    def calculate_age(self, event: Optional[tk.Event] = None) -> Optional[str]:
        date_str = self.age_year_entry.get().strip()
        if date_str == self.ui.date_placeholder: date_str = ""
        
        if not date_str:
            self._set_result("-")
            self.info_lbl.config(text="Lütfen doğum tarihinizi girin!", fg=self.ui.error_color)
            return "break"
            
        result = FinansMotoru.yas_hesapla(date_str)
        if "hata" in result:
            err_msg = "Gelecek bir tarih giremezsiniz!" if result["hata"] == "Gelecek tarih" else "Geçersiz format! Örn: 15.05.1990"
            self.info_lbl.config(text=err_msg, fg=self.ui.error_color)
            self._set_result("-")
            return "break"
            
        self.age_res_txt.config(state="normal")
        self.age_res_txt.delete("1.0", tk.END)
        self.age_res_txt.insert(tk.END, "• Yaşınız: ")
        self.age_res_txt.insert(tk.END, f"{result['yillar']}", "bold")
        self.age_res_txt.insert(tk.END, " yıl, ")
        self.age_res_txt.insert(tk.END, f"{result['aylar']}", "bold")
        self.age_res_txt.insert(tk.END, " ay, ")
        self.age_res_txt.insert(tk.END, f"{result['gunler']}", "bold")
        self.age_res_txt.insert(tk.END, " gün\n\n• Gün Alma Durumu: ")
        self.age_res_txt.insert(tk.END, f"{result['yillar']}", "bold")
        self.age_res_txt.insert(tk.END, " yaşınızı doldurdunuz ve ")
        self.age_res_txt.insert(tk.END, f"{int(result['yillar']) + 1}", "bold")
        self.age_res_txt.insert(tk.END, " yaşından gün alıyorsunuz.\n\n• Doğduğunuz Gün: ")
        self.age_res_txt.insert(tk.END, f"{result['dogum_gunu_str']}", "bold")
        self.age_res_txt.insert(tk.END, "\n\n• Sonraki Doğum Günü: ")
        self.age_res_txt.insert(tk.END, f"{result['sonraki_dogum_gunu_str']}", "bold")
        self.age_res_txt.insert(tk.END, f" ({result['kalan_gun']} gün kaldı)\n\n• Yaşanılan Gün Sayısı: Bugüne kadar tam ")
        self.age_res_txt.insert(tk.END, f"{result['yasanilan_gun_str']}", "bold")
        self.age_res_txt.insert(tk.END, " gün yaşadınız.")
        self.age_res_txt.config(state="disabled")
        
        self.info_lbl.config(text="Hesaplandı • Kopyalamak için cevaba tıklayın", fg=self.ui.accent_color)
        return "break"

    def _set_result(self, text: str) -> None:
        self.age_res_txt.config(state="normal")
        self.age_res_txt.delete("1.0", tk.END)
        self.age_res_txt.insert("1.0", text)
        self.age_res_txt.config(state="disabled")

    def clear_data(self) -> None:
        self.reset_defaults()
        self.age_year_entry.config(fg=self.ui.text_placeholder)
        self._set_result("-")