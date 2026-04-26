import tkinter as tk
import time
from typing import Optional, Tuple, TYPE_CHECKING, Callable, Any, Dict, List, Union, Literal

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

    def destroy(self) -> None:
        """Widget yok edilirken arka planda kalan zamanlayıcıları (timer) iptal ederek bellek sızıntısını önler."""
        timer_id = getattr(self, '_msg_timer', None)
        if timer_id is not None:
            self.ui.root.after_cancel(timer_id)
            self._msg_timer = None
        super().destroy()

    def clear_data(self, from_keyboard: bool = False) -> None:
        if from_keyboard:
            self.flash_clear_button()
        self.reset_defaults()
        for lbl in self.result_labels.values():
            lbl.config(text="-")
            
        # Temizle işleminden sonra doğrudan veri girilebilmesi için odağı geri ver
        if self.primary_input:
            self.primary_input.focus_set()

    def _build_header(self, parent: tk.Frame, desc: str) -> None:
        desc_frame = tk.Frame(parent, bg=self.ui.bg_secondary)
        desc_frame.pack(fill="x", pady=(5, 0), padx=(0, 8))

        top_row = tk.Frame(desc_frame, bg=self.ui.bg_secondary)
        top_row.pack(fill="x")

        if self.ui.aktif_dil == "tr":
            title_text = self.get_name().replace('i', 'İ').replace('ı', 'I').upper()
        else:
            title_text = self.get_name().upper()
        tk.Label(top_row, text=title_text, font=self.ui.font_bold, fg=self.ui.accent_color, bg=self.ui.bg_secondary).pack(side="left")

        # Fiziksel Kaşe (Stamp) ve Tıklanabilir Navigasyon Rozeti
        self.badge_frame = tk.Frame(top_row, bg=self.ui.bg_secondary, cursor="hand2", bd=0)
        self.badge_frame.pack(side="right", ipadx=4, ipady=4)
        
        self.badge_cur_lbl = tk.Label(self.badge_frame, text="", font=(self.ui.font_main[0], 8, "bold"), fg=self.ui.text_secondary, bg=self.ui.bg_secondary, cursor="hand2", bd=0)
        self.badge_cur_lbl.pack(side="left")
        
        self.badge_sep_lbl = tk.Label(self.badge_frame, text="/", font=(self.ui.font_main[0], 8, "bold"), fg=self.ui.text_disabled, bg=self.ui.bg_secondary, cursor="hand2", bd=0)
        self.badge_sep_lbl.pack(side="left", padx=4)
        
        self.badge_tot_lbl = tk.Label(self.badge_frame, text="", font=(self.ui.font_main[0], 8, "bold"), fg=self.ui.text_disabled, bg=self.ui.bg_secondary, cursor="hand2", bd=0)
        self.badge_tot_lbl.pack(side="left")

        for w in (self.badge_frame, self.badge_cur_lbl, self.badge_sep_lbl, self.badge_tot_lbl):
            w.bind("<Button-1>", lambda e: self.orchestrator.cycle_tools())
            w.bind("<Enter>", lambda e: self.badge_frame.config(bg=self.ui.tab_inactive_bg) or [lbl.config(bg=self.ui.tab_inactive_bg) for lbl in (self.badge_cur_lbl, self.badge_sep_lbl, self.badge_tot_lbl)])
            w.bind("<Leave>", lambda e: self.badge_frame.config(bg=self.ui.bg_secondary) or [lbl.config(bg=self.ui.bg_secondary) for lbl in (self.badge_cur_lbl, self.badge_sep_lbl, self.badge_tot_lbl)])

        tk.Label(desc_frame, text=desc, font=self.ui.font_main, fg=self.ui.text_disabled, bg=self.ui.bg_secondary, justify="left", wraplength=self.ui.s(264), height=2, anchor="nw").pack(anchor="w", pady=(2, 0), padx=(8, 0), fill="x")

    def set_page_badge(self, current: int, total: int) -> None:
        if hasattr(self, 'badge_cur_lbl'):
            self.badge_cur_lbl.config(text=f"{current:02d}")
            self.badge_tot_lbl.config(text=f"{total:02d}")

    def _validate_entry_length(self, P: str) -> bool:
        return len(P) <= 50

    def _build_input_row(self, parent: tk.Frame, row: int, label_text: str, default_val: str = "", width: int = 15) -> tk.Entry:
        tk.Label(parent, text=label_text, font=self.ui.font_main, fg=self.ui.fg_color, bg=self.ui.bg_secondary).grid(row=row, column=0, sticky="w", pady=3)

        vcmd = (self.register(self._validate_entry_length), '%P')
        entry = tk.Entry(parent, font=self.ui.font_main, bg=self.ui.input_bg, fg=self.ui.fg_color, bd=2, relief="sunken", highlightthickness=1, highlightbackground=self.ui.bg_secondary, highlightcolor=self.ui.accent_color, width=width, validate="key", validatecommand=vcmd, selectbackground=self.ui.shadow_dark, selectforeground=self.ui.fg_color)
        if default_val:
            entry.insert(0, default_val)
        self.default_inputs[entry] = default_val
        entry.grid(row=row, column=1, sticky="ew", padx=8, pady=3)
        parent.columnconfigure(1, weight=1)
        return entry

    def _build_action_buttons(self, parent: tk.Frame, calc_cmd: Callable[..., Any], clear_cmd: Callable[[], None], rowspan: int = 2) -> None:
        self.calc_btn = tk.Button(parent, text=self.ui.lang["btn_calculate"], width=10, font=self.ui.font_bold, bg=self.ui.accent_color, fg=self.ui.shadow_light, bd=2, relief="raised", activebackground=self.ui.accent_hover, activeforeground=self.ui.shadow_light, cursor="hand2", command=calc_cmd)
        self.calc_btn.grid(row=0, column=2, rowspan=max(1, rowspan - 1), padx=(8, 16), sticky="nsew", pady=(8, 4), ipadx=8)
        self.clear_btn = tk.Button(parent, text=self.ui.lang["btn_clear"], width=10, font=self.ui.font_small, bg=self.ui.bg_secondary, fg=self.ui.text_secondary, bd=1, relief="raised", activebackground=self.ui.tab_inactive_bg, cursor="hand2", command=clear_cmd)
        self.clear_btn.grid(row=rowspan - 1, column=2, padx=(8, 16), sticky="nsew", pady=(4, 8))

        for btn in (self.calc_btn, self.clear_btn):
            btn.bind("<Button-1>", lambda e, b=btn: b.config(relief="sunken"))
            btn.bind("<ButtonRelease-1>", lambda e, b=btn: b.config(relief="raised"))

    def flash_calc_button(self) -> bool:
        """Enter tuşu ile hesaplama tetiklendiğinde animasyon verir ve basılı tutma (spam) durumunu engeller."""
        current_time = time.time()
        if hasattr(self, '_last_calc_time') and current_time - getattr(self, '_last_calc_time') < 0.4:
            return False  # 400ms dolmadan yeni bir klavye işlemine izin verme (Debounce)
            
        self._last_calc_time = current_time
        
        if hasattr(self, 'calc_btn') and self.calc_btn.winfo_exists():
            self.calc_btn.config(relief="sunken", bg=self.ui.accent_hover)
            self.ui.root.after(150, lambda: self.calc_btn.config(relief="raised", bg=self.ui.accent_color) if self.calc_btn.winfo_exists() else None)
        return True

    def flash_clear_button(self) -> None:
        """Esc tuşu ile temizleme tetiklendiğinde butona tıklanma animasyonu verir."""
        if hasattr(self, 'clear_btn') and self.clear_btn.winfo_exists():
            self.clear_btn.config(relief="sunken", bg=self.ui.tab_inactive_bg)
            self.ui.root.after(150, lambda: self.clear_btn.config(relief="raised", bg=self.ui.bg_secondary) if self.clear_btn.winfo_exists() else None)

    def _build_info_label(self, parent: tk.Frame, default_msg: str, pad_y: Tuple[int, int] = (21, 21)) -> tk.Label:
        self.default_info_msg = default_msg
        self.info_lbl = tk.Label(parent, text=default_msg, font=self.ui.font_main, fg=self.ui.text_secondary, bg=self.ui.bg_secondary, justify="left", wraplength=self.ui.s(264))
        self.info_lbl.pack(side="bottom", anchor="w", pady=pad_y)
        self._permanent_msg = (default_msg, self.ui.text_secondary)
        self._msg_timer: Optional[str] = None
        return self.info_lbl

    def _make_clickable(self, widget: Union[tk.Label, tk.Text]) -> None:
        widget.config(cursor="hand2", bd=2, relief="flat")
        
        def on_press(e: tk.Event) -> None:
            text = widget.get("1.0", "end-1c").strip() if isinstance(widget, tk.Text) else str(widget.cget("text"))
            if text not in ("", "-"):
                widget.config(relief="sunken", bg=self.ui.shadow_dark, fg=self.ui.accent_color)
                self.copy_to_clipboard(text)
                
        def on_release(e: tk.Event) -> None:
            widget.config(relief="flat", bg=self.ui.bg_secondary, fg=self.ui.fg_color)
            
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
        parent.columnconfigure(0, minsize=self.ui.s(104))
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
            
        if self.ui.aktif_dil == "tr":
            formatted = formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
        return formatted

    def format_percentage(self, val: Union[int, float, str], isaret: str = "") -> str:
        formatted_val = self.format_number(val)
        if self.ui.aktif_dil == "en":
            return f"{isaret}{formatted_val}%"
        return f"%{isaret}{formatted_val}"

    def flash_result(self, widget: Union[tk.Label, tk.Text]) -> None:
        """Hesaplama sonucunun güncellendiğini vurgulamak için metin rengini geçici olarak kiremit rengine boyar."""
        widget.config(fg=self.ui.accent_color)
        self.ui.root.after(1000, lambda: widget.config(fg=self.ui.fg_color) if widget.winfo_exists() else None)

    def show_message(self, text: str, msg_type: Literal["info", "success", "error"] = "info", transient: bool = False, duration: int = 1500) -> None:
        """Akıllı Geri Bildirim Yöneticisi: Mesaj türüne göre renk atar ve geçici/kalıcı durumları hafızada tutarak yönetir."""
        if not self.info_lbl: return
        
        timer_id = getattr(self, '_msg_timer', None)
        if timer_id is not None:
            self.ui.root.after_cancel(timer_id)
            self._msg_timer = None
            
        color_map = {
            "info": self.ui.text_secondary,
            "success": self.ui.accent_color,
            "error": self.ui.error_color
        }
        color = color_map.get(msg_type, self.ui.text_secondary)
        self.info_lbl.config(text=text, fg=color)
        
        if not transient:
            self._permanent_msg = (text, color)
        else:
            # Otomatik İyileştirme (Auto-recovery): Başarı mesajı gelmişse ve kalıcı hafızada hata durumu kaldıysa, durumu sıfırla.
            if msg_type == "success" and hasattr(self, '_permanent_msg') and self._permanent_msg[1] == self.ui.error_color:
                self._permanent_msg = (self.default_info_msg, self.ui.text_secondary)
                
            def restore() -> None:
                if self.info_lbl and hasattr(self, '_permanent_msg'):
                    self.info_lbl.config(text=self._permanent_msg[0], fg=self._permanent_msg[1])
            self._msg_timer = self.ui.root.after(duration, restore)

    def reset_defaults(self) -> None:
        for entry, def_val in self.default_inputs.items():
            entry.delete(0, tk.END)
            entry.insert(0, def_val)
        self.show_message(self.default_info_msg, "info")

    def copy_to_clipboard(self, result_text: str) -> None:
        if not result_text or result_text == "-": return
        self.ui.root.clipboard_clear()
        self.ui.root.clipboard_append(result_text)
        self.ui.root.update()
        self.show_message(self.ui.lang["msg_copied"], "success", transient=True)
