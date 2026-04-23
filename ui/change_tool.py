import tkinter as tk
from typing import Optional
from core.matematik_motoru import MatematikMotoru
from core.finans_motoru import FinansMotoru
from ui.base_tool import BaseToolWidget

class ChangeToolWidget(BaseToolWidget):
    def get_name(self) -> str: return "Değişiklik Hesaplayıcı"

    def build_ui(self) -> None:
        self._build_header(self, "Örn: Eski fiyatı 150 TL, yeni fiyatı 200 TL olan bir malınyüzde kaç zamlandığını hesaplar.")
        change_frame = tk.Frame(self, bg=self.ui.bg_color)
        change_frame.pack(fill="x", pady=5)
        
        self.old_val_entry = self._build_input_row(change_frame, 0, "Eski Değer:")
        self.new_val_entry = self._build_input_row(change_frame, 1, "Yeni Değer:")
        self._build_action_buttons(change_frame, self.calculate_change, self.clear_data)
        
        change_res_frame = tk.Frame(self, bg=self.ui.bg_color)
        change_res_frame.pack(fill="x", pady=(10, 0))
        
        tk.Label(change_res_frame, text="Değişiklik Oranı:", fg=self.ui.text_secondary, bg=self.ui.bg_color, font=self.ui.font_main).grid(row=0, column=0, sticky="w", pady=4)
        self.change_res_lbl = tk.Label(change_res_frame, text="-", font=self.ui.font_title, fg=self.ui.fg_color, bg=self.ui.bg_color, cursor="hand2")
        self.change_res_lbl.grid(row=0, column=1, sticky="w", padx=20)
        self.change_res_lbl.bind('<Button-1>', lambda e: self.copy_to_clipboard(self.change_res_lbl.cget("text")))
            
        self._build_info_label(self, "Artış veya azalışı görmek için değerleri girin", pad_y=(15, 0))
        
        self.old_val_entry.bind('<Return>', self.calculate_change)
        self.new_val_entry.bind('<Return>', self.calculate_change)
        self.primary_input = self.old_val_entry

    def calculate_change(self, event: Optional[tk.Event] = None) -> Optional[str]:
        old_nums = MatematikMotoru.metinden_sayilari_ayikla(self.old_val_entry.get().strip())
        new_nums = MatematikMotoru.metinden_sayilari_ayikla(self.new_val_entry.get().strip())
        
        if not old_nums or not new_nums:
            self.change_res_lbl.config(text="-")
            self.info_lbl.config(text="Eski ve yeni değer eksik!", fg=self.ui.error_color)
            return "break"
            
        result = FinansMotoru.degisim_orani_hesapla(old_nums[0], new_nums[0])
        oran = result["degisim_orani"]
        self.change_res_lbl.config(text=f"%{'+' if oran > 0 else ''}{oran}")
        self.info_lbl.config(text="Hesaplandı • Kopyalamak için sonuca tıklayın", fg=self.ui.accent_color)
        return "break"

    def clear_data(self) -> None:
        self.reset_defaults()
        self.change_res_lbl.config(text="-")