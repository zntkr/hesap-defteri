import tkinter as tk
from typing import Optional, Tuple, TYPE_CHECKING, Callable, Any, Dict, List, Union

if TYPE_CHECKING:
    from ui.arayuz_tasarimi import MainUI
    from ui.tools_tab import ToolsTab

from core.matematik_motoru import MatematikMotoru

class BaseToolWidget(tk.Frame):
    """Tüm araçların miras alacağı, ortak arayüz elemanlarını barındıran temel (Base) sınıf."""

    @property
    def _MSG_HESAPLANDI(self) -> str:
        return self.ui.lang["msg_calculated"]

    def __init__(self, parent: tk.Widget, ui: 'MainUI', orchestrator: 'ToolsTab') -> None:
        super().__init__(parent, bg=ui.bg_secondary)
        self.ui = ui
        self.orchestrator = orchestrator
        self.primary_input: Optional[tk.Widget] = None
        self.default_inputs: Dict[tk.Entry, str] = {}
        self.result_labels: Dict[str, tk.Label] = {}
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
        self.reset_defaults()
        for lbl in self.result_labels.values():
            lbl.config(text="-")
            
        # Temizle işleminden sonra doğrudan veri girilebilmesi için odağı geri ver
        if self.primary_input:
            self.primary_input.focus_set()

    def _build_header(self, parent: tk.Frame, desc: str) -> None:
        desc_frame = tk.Frame(parent, bg=self.ui.bg_secondary, pady=8)
        desc_frame.pack(fill="x", pady=(0, 16), padx=(0, 8))

        top_row = tk.Frame(desc_frame, bg=self.ui.bg_secondary)
        top_row.pack(fill="x")

        if self.ui.aktif_dil == "tr":
            title_text = self.get_name().replace('i', 'İ').replace('ı', 'I').upper()
        else:
            title_text = self.get_name().upper()
        tk.Label(top_row, text=title_text, font=self.ui.font_bold, fg=self.ui.accent_color, bg=self.ui.bg_secondary).pack(side="left")

        self.badge_lbl = tk.Label(top_row, text="", font=(self.ui.font_main[0], 9, "bold"), fg=self.ui.text_disabled, bg=self.ui.bg_secondary)
        self.badge_lbl.pack(side="right")

        tk.Label(desc_frame, text=desc, font=self.ui.font_main, fg=self.ui.text_disabled, bg=self.ui.bg_secondary, justify="left", wraplength=320, height=3, anchor="nw").pack(anchor="w", pady=(4, 0), fill="x")

    def set_page_badge(self, current: int, total: int) -> None:
        if hasattr(self, 'badge_lbl'):
            self.badge_lbl.config(text=f"[ {current:02d} / {total:02d} ]")

    def _validate_entry_length(self, P: str) -> bool:
        return len(P) <= 50

    def _build_input_row(self, parent: tk.Frame, row: int, label_text: str, default_val: str = "", width: int = 15) -> tk.Entry:
        tk.Label(parent, text=label_text, font=self.ui.font_main, fg=self.ui.fg_color, bg=self.ui.bg_secondary).grid(row=row, column=0, sticky="w", pady=8)
        
        vcmd = (self.register(self._validate_entry_length), '%P')
        entry = tk.Entry(parent, font=self.ui.font_main, bg=self.ui.input_bg, fg=self.ui.fg_color, bd=2, relief="sunken", highlightthickness=1, highlightbackground=self.ui.bg_secondary, highlightcolor=self.ui.accent_color, width=width, validate="key", validatecommand=vcmd, selectbackground=self.ui.shadow_dark, selectforeground=self.ui.fg_color)
        if default_val:
            entry.insert(0, default_val)
        self.default_inputs[entry] = default_val
        entry.grid(row=row, column=1, sticky="w", padx=8, pady=8)
        parent.columnconfigure(0, minsize=120)
        parent.columnconfigure(1, weight=1)
        return entry

    def _build_action_buttons(self, parent: tk.Frame, calc_cmd: Callable[..., Any], clear_cmd: Callable[[], None], rowspan: int = 2) -> None:
        calc_btn = tk.Button(parent, text=self.ui.lang["btn_calculate"], font=self.ui.font_bold, bg=self.ui.accent_color, fg=self.ui.shadow_light, bd=2, relief="raised", activebackground=self.ui.accent_hover, activeforeground=self.ui.shadow_light, cursor="hand2", command=calc_cmd)
        calc_btn.grid(row=0, column=2, rowspan=max(1, rowspan - 1), padx=8, sticky="nsew", pady=(8, 4), ipadx=8)
        clear_btn = tk.Button(parent, text=self.ui.lang["btn_clear"], font=self.ui.font_small, bg=self.ui.bg_secondary, fg=self.ui.text_secondary, bd=1, relief="raised", activebackground=self.ui.tab_inactive_bg, cursor="hand2", command=clear_cmd)
        clear_btn.grid(row=rowspan - 1, column=2, padx=8, sticky="nsew", pady=(4, 8))

        for btn in (calc_btn, clear_btn):
            btn.bind("<Button-1>", lambda e, b=btn: b.config(relief="sunken"))
            btn.bind("<ButtonRelease-1>", lambda e, b=btn: b.config(relief="raised"))

    def _build_info_label(self, parent: tk.Frame, default_msg: str, pad_y: Tuple[int, int] = (16, 16)) -> tk.Label:
        self.default_info_msg = default_msg
        self.info_lbl = tk.Label(parent, text=default_msg, font=self.ui.font_main, fg=self.ui.text_secondary, bg=self.ui.bg_secondary, justify="left", wraplength=312)
        self.info_lbl.pack(side="bottom", anchor="w", pady=pad_y)
        return self.info_lbl

    def _make_clickable(self, widget: Union[tk.Label, tk.Text]) -> None:
        widget.config(cursor="hand2", bd=2, relief="flat")
        
        def on_press(e: tk.Event, w: Union[tk.Label, tk.Text] = widget) -> None:
            text = w.get("1.0", "end-1c").strip() if isinstance(w, tk.Text) else w.cget("text")
            if text not in ("", "-"):
                w.config(relief="sunken", bg=self.ui.shadow_dark, fg=self.ui.accent_color)
                self.copy_to_clipboard(text)
                
        def on_release(e: tk.Event, w: Union[tk.Label, tk.Text] = widget) -> None:
            w.config(relief="flat", bg=self.ui.bg_secondary, fg=self.ui.fg_color)
            
        widget.bind('<Button-1>', on_press)
        widget.bind('<ButtonRelease-1>', on_release)

    def _make_label_clickable(self, lbl: tk.Label) -> None:
        self._make_clickable(lbl)

    def _build_result_labels(self, parent: tk.Frame, items: List[Tuple[str, str]], padx: int = 24) -> Dict[str, tk.Label]:
        for i, (text, key) in enumerate(items):
            tk.Label(parent, text=text, fg=self.ui.text_secondary, bg=self.ui.bg_secondary, font=self.ui.font_main).grid(row=i, column=0, sticky="w", pady=4)
            lbl = tk.Label(parent, text="-", font=self.ui.font_bold, fg=self.ui.fg_color, bg=self.ui.bg_secondary)
            lbl.grid(row=i, column=1, sticky="w", padx=padx)
            self._make_label_clickable(lbl)
            self.result_labels[key] = lbl
        parent.columnconfigure(0, minsize=120)
        return self.result_labels

    def _get_numbers(self, entry: tk.Entry) -> List[float]:
        return MatematikMotoru.metinden_sayilari_ayikla(entry.get().strip())

    def format_number(self, val: Union[int, float, str], max_len: int = 14) -> str:
        if isinstance(val, str): return val
        
        if isinstance(val, float) and not val.is_integer():
            formatted = f"{val:,.4f}".rstrip('0').rstrip('.')
        else:
            formatted = f"{int(val):,}"
            
        # Arayüz taşımasını önlemek için "Bilimsel Gösterim" (Scientific Notation) geçişi
        if len(formatted) > max_len:
            formatted = f"{val:.4e}"
            
        if getattr(self.ui, 'aktif_dil', 'tr') == "tr":
            formatted = formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
        return formatted

    def format_percentage(self, val: Union[int, float, str], isaret: str = "") -> str:
        formatted_val = self.format_number(val)
        if getattr(self.ui, 'aktif_dil', 'tr') == "en":
            return f"{isaret}{formatted_val}%"
        return f"%{isaret}{formatted_val}"

    def flash_result(self, widget: Union[tk.Label, tk.Text]) -> None:
        """Hesaplama sonucunun güncellendiğini vurgulamak için metin rengini geçici olarak kiremit rengine boyar."""
        widget.config(fg=self.ui.accent_color)
        self.ui.root.after(1000, lambda: widget.config(fg=self.ui.fg_color) if widget.winfo_exists() else None)

    def reset_defaults(self) -> None:
        for entry, def_val in self.default_inputs.items():
            entry.delete(0, tk.END)
            entry.insert(0, def_val)
        if self.info_lbl:
            self.info_lbl.config(text=self.default_info_msg, fg=self.ui.text_secondary)

    def copy_to_clipboard(self, result_text: str) -> None:
        if not result_text or result_text == "-": return
        self.ui.root.clipboard_clear()
        self.ui.root.clipboard_append(result_text)
        self.ui.root.update()
        if self.info_lbl:
            self.info_lbl.config(text=self.ui.lang["msg_copied"], fg=self.ui.accent_color)
            self.ui.root.after(1500, lambda: self.info_lbl.config(text=self.default_info_msg, fg=self.ui.text_secondary) if self.info_lbl else None)
