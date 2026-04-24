import tkinter as tk
from typing import Optional, Tuple, TYPE_CHECKING, Callable, Any, Dict

if TYPE_CHECKING:
    from ui.arayuz_tasarimi import MainUI
    from ui.tools_tab import ToolsTab

class BaseToolWidget(tk.Frame):
    """Tüm araçların miras alacağı, ortak arayüz elemanlarını barındıran temel (Base) sınıf."""
    def __init__(self, parent: tk.Widget, ui: 'MainUI', orchestrator: 'ToolsTab') -> None:
        super().__init__(parent, bg=ui.bg_secondary)
        self.ui = ui
        self.orchestrator = orchestrator
        self.primary_input: Optional[tk.Widget] = None
        self.default_inputs: Dict[tk.Entry, str] = {}
        self.info_lbl: Optional[tk.Label] = None
        self.default_info_msg: str = ""
        self.build_ui()

    def get_name(self) -> str:
        raise NotImplementedError("Alt sınıf kendi adını tanımlamalıdır.")

    def get_short_name(self) -> str:
        return self.get_name()

    def build_ui(self) -> None:
        raise NotImplementedError("Alt sınıf arayüzünü (UI) tanımlamalıdır.")

    def clear_data(self) -> None:
        pass

    def _build_header(self, parent: tk.Frame, desc: str) -> None:
        desc_frame = tk.Frame(parent, bg=self.ui.bg_secondary, pady=8)
        desc_frame.pack(fill="x", pady=(0, 16), padx=(0, 8))
        
        top_row = tk.Frame(desc_frame, bg=self.ui.bg_secondary)
        top_row.pack(fill="x")
        
        tk.Label(top_row, text=self.get_name(), font=self.ui.font_bold, fg=self.ui.accent_color, bg=self.ui.bg_secondary).pack(side="left")
        
        self.badge_lbl = tk.Label(top_row, text="", font=(self.ui.font_main[0], 9, "bold"), fg=self.ui.text_disabled, bg=self.ui.bg_secondary)
        self.badge_lbl.pack(side="right")
        
        tk.Label(desc_frame, text=desc, font=self.ui.font_main, fg=self.ui.text_secondary, bg=self.ui.bg_secondary, justify="left", wraplength=320).pack(anchor="w", pady=(4,0))

    def set_page_badge(self, current: int, total: int) -> None:
        if hasattr(self, 'badge_lbl'):
            self.badge_lbl.config(text=f"[ {current:02d} / {total:02d} ]")

    def _build_input_row(self, parent: tk.Frame, row: int, label_text: str, default_val: str = "", width: int = 15) -> tk.Entry:
        tk.Label(parent, text=label_text, font=self.ui.font_main, fg=self.ui.fg_color, bg=self.ui.bg_secondary).grid(row=row, column=0, sticky="w", pady=8)
        entry = tk.Entry(parent, font=self.ui.font_main, bg=self.ui.shadow_light, fg=self.ui.fg_color, bd=1, relief="solid", width=width)
        if default_val:
            entry.insert(0, default_val)
            self.default_inputs[entry] = default_val
        entry.grid(row=row, column=1, sticky="w", padx=8, pady=8)
        parent.columnconfigure(1, weight=1)
        return entry

    def _build_action_buttons(self, parent: tk.Frame, calc_cmd: Callable[..., Any], clear_cmd: Callable[[], None]) -> None:
        calc_btn = tk.Button(parent, text="HESAPLA", font=self.ui.font_bold, bg=self.ui.accent_color, fg=self.ui.shadow_light, bd=2, relief="raised", activebackground=self.ui.accent_hover, activeforeground=self.ui.shadow_light, cursor="hand2", command=calc_cmd)
        calc_btn.grid(row=0, column=2, padx=8, sticky="nsew", pady=(8, 4), ipadx=8)
        clear_btn = tk.Button(parent, text="Temizle", font=(self.ui.font_main[0], 8), bg=self.ui.bg_secondary, fg=self.ui.text_secondary, bd=1, relief="raised", activebackground=self.ui.border_color, cursor="hand2", command=clear_cmd)
        clear_btn.grid(row=1, column=2, padx=8, sticky="nsew", pady=(4, 8))

    def _build_info_label(self, parent: tk.Frame, default_msg: str, pad_y: Tuple[int, int] = (16, 0)) -> tk.Label:
        self.default_info_msg = default_msg
        self.info_lbl = tk.Label(parent, text=default_msg, font=self.ui.font_main, fg=self.ui.text_secondary, bg=self.ui.bg_secondary, justify="center", wraplength=312)
        self.info_lbl.pack(pady=pad_y)
        return self.info_lbl

    def reset_defaults(self) -> None:
        """Kayıtlı tüm form elemanlarını varsayılan değerlerine döndürür."""
        for entry, def_val in self.default_inputs.items():
            entry.delete(0, tk.END)
            entry.insert(0, def_val)
        if self.info_lbl:
            self.info_lbl.config(text=self.default_info_msg, fg=self.ui.text_secondary)

    def copy_to_clipboard(self, result_text: str) -> None:
        """Sonucu panoya kopyalar ve bilgi etiketini (info_lbl) geçici olarak günceller."""
        if not result_text or result_text == "-": return
        self.ui.root.clipboard_clear()
        self.ui.root.clipboard_append(result_text)
        self.ui.root.update()
        if self.info_lbl:
            self.info_lbl.config(text="Kopyalandı!", fg=self.ui.accent_color)
            self.ui.root.after(1500, lambda: self.info_lbl.config(text=self.default_info_msg, fg=self.ui.text_secondary))