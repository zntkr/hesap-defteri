import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import os
import sys
from datetime import datetime
from typing import Optional, Any, Union

# Proje kök dizinini Python yoluna ekle (Pylance import hatalarını önlemek için)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui.tools_tab import ToolsTab, PaperShadowCanvas
import core.dil as dil
import core.ayarlar as ayarlar

class MainUI:
    """
    Main Orchestrator class for the UI (Presentation Layer).
    Manages the application state, menus, and tab component instantiation.
    """
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.sf = root.winfo_fpixels('1i') / 96.0

        # --- APP CONFIG ---
        self.app_version = "1.0.0"
        self.build_year = str(datetime.now().year)

        # --- LANGUAGE ---
        self.aktif_dil = ayarlar.load()["lang"]
        self.lang = dil.LANGS[self.aktif_dil]

        self.date_placeholder = self.lang["date_placeholder"]
        self.placeholder_text = self.lang["placeholder_text"]

        self.root.title(f"{self.lang['app_name']} - v{self.app_version}")
        self.root.geometry(f"{self.s(376)}x{self.s(544)}")

        # --- NEO-RETRO THEME VARIABLES ---
        self.bg_color = "#4A423A"
        self.bg_shadow = "#38322C"
        self.fg_color = "#2D2D2D"
        self.accent_color = "#C85A47"
        self.accent_hover = "#A84534"
        self.accent_light = "#E08D7D"
        self.border_color = "#E0DCE3"
        self.shadow_dark = "#AFAFAF"
        self.shadow_light = "#FFFFFF"
        self.text_secondary = "#666666"
        self.text_disabled = "#B0B0B0"
        self.bg_secondary = "#EFEBE6"
        self.tape_bg = "#F4F1EA"
        self.input_bg = "#F9F8F6"
        self.error_color = "#D32F2F"
        self.text_placeholder = "#888888"
        self.text_inverse = "#D0CFCB"
        self.tab_inactive_bg = "#E0DCD7" # bg_secondary'den 15 birim karanlık — bir ton koyusu

        # --- TYPOGRAPHY ---
        available_fonts = tkfont.families()
        preferred_fonts = ["IBM Plex Mono", "Consolas", "Courier New", "Courier"]
        selected_font = next((f for f in preferred_fonts if f in available_fonts), "Courier")

        self.font_main = (selected_font, 9)
        self.font_bold = (selected_font, 9, "bold")
        self.font_small = (selected_font, 8)
        self.font_title = (selected_font, 16)

        self.root.config(bg=self.bg_color)
        self.always_on_top_var = tk.BooleanVar(value=False)
        self.show_tape_var = tk.BooleanVar(value=False)

        self.build_ui()
        self.build_menu()
        self.build_context_menu()
        
    def s(self, val: Union[int, float]) -> int:
        """DPI ölçekleme çarpanına göre piksel değerlerini dinamik olarak net/vektörel büyütür."""
        return int(val * self.sf)

    def _switch_language(self, lang_code: str) -> None:
        if lang_code == self.aktif_dil:
            return

        topmost_val = self.always_on_top_var.get()
        tape_val = self.show_tape_var.get()

        # withdraw/deiconify yerine alpha kullanılıyor: WM_SHOW sırasında Windows'un
        # pencereyi beyaz sistem rengiyle silmesi (WM_ERASEBKGND) bu yöntemle tetiklenmiyor.
        self.root.wm_attributes("-alpha", 0.0)
        try:
            self.aktif_dil = lang_code
            self.lang = dil.LANGS[lang_code]
            ayarlar.save({"lang": lang_code})
            self.date_placeholder = self.lang["date_placeholder"]
            self.placeholder_text = self.lang["placeholder_text"]

            self.root.title(f"{self.lang['app_name']} - v{self.app_version}")

            self._print_queue = []
            self._is_printing = False
            self.root["menu"] = ""
            for widget in self.root.winfo_children():
                widget.destroy()

            self.always_on_top_var = tk.BooleanVar(value=topmost_val)
            self.show_tape_var = tk.BooleanVar(value=tape_val)

            self.build_ui()
            self.build_menu()
            self.build_context_menu()

            self.root.wm_attributes("-topmost", topmost_val)
            self.root.update_idletasks()
            self.toggle_tape()
        finally:
            self.root.wm_attributes("-alpha", 1.0)

    def build_menu(self) -> None:
        L = self.lang
        menubar = tk.Menu(self.root, font=self.font_main, bg=self.bg_secondary, fg=self.fg_color, activebackground=self.shadow_dark, activeforeground=self.fg_color)

        file_menu = tk.Menu(menubar, tearoff=0, font=self.font_main, bg=self.bg_secondary, fg=self.fg_color, activebackground=self.shadow_dark, activeforeground=self.fg_color)
        file_menu.add_command(label=L["menu_exit"], command=self.root.quit, accelerator="Alt+F4")

        self.edit_menu = tk.Menu(menubar, tearoff=0, font=self.font_main, bg=self.bg_secondary, fg=self.fg_color, activebackground=self.shadow_dark, activeforeground=self.fg_color, postcommand=self._update_edit_menu)
        self.edit_menu.add_command(label=L["menu_cut"], command=lambda: self._trigger_os_event("<<Cut>>"), accelerator="Ctrl+X")
        self.edit_menu.add_command(label=L["menu_copy"], command=lambda: self._trigger_os_event("<<Copy>>"), accelerator="Ctrl+C")
        self.edit_menu.add_command(label=L["menu_paste"], command=lambda: self._trigger_os_event("<<Paste>>"), accelerator="Ctrl+V")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label=L["menu_select_all"], command=self._select_all, accelerator="Ctrl+A")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label=L["menu_clear_all"], command=self.clear_all, accelerator="Esc")

        tools_menu = tk.Menu(menubar, tearoff=0, font=self.font_main, bg=self.bg_secondary, fg=self.fg_color, activebackground=self.shadow_dark, activeforeground=self.fg_color)
        self.active_tool_var = tk.StringVar()
        for i, tool_name in enumerate(self.main_view.frames.keys(), start=1):
            accel = f"Ctrl+{i}"
            tools_menu.add_radiobutton(label=tool_name, variable=self.active_tool_var, value=tool_name, command=lambda name=tool_name: self.select_tool(name), accelerator=accel)
            self.root.bind(f"<Control-Key-{i}>", lambda _, name=tool_name: self.select_tool(name))

        view_menu = tk.Menu(menubar, tearoff=0, font=self.font_main, bg=self.bg_secondary, fg=self.fg_color, activebackground=self.shadow_dark, activeforeground=self.fg_color)
        view_menu.add_checkbutton(label=L["menu_always_on_top"], variable=self.always_on_top_var, command=self.toggle_always_on_top)
        view_menu.add_separator()
        view_menu.add_checkbutton(label=L["menu_show_tape"], variable=self.show_tape_var, command=self.toggle_tape, accelerator="Ctrl+H")

        self.root.bind("<Control-h>", self.toggle_tape)
        self.root.bind("<Control-H>", self.toggle_tape)

        lang_menu = tk.Menu(menubar, tearoff=0, font=self.font_main, bg=self.bg_secondary, fg=self.fg_color, activebackground=self.shadow_dark, activeforeground=self.fg_color)
        self._lang_var = tk.StringVar(value=self.aktif_dil)
        lang_menu.add_radiobutton(label=L["lang_tr"], variable=self._lang_var, value="tr", command=lambda: self._switch_language("tr"))
        lang_menu.add_radiobutton(label=L["lang_en"], variable=self._lang_var, value="en", command=lambda: self._switch_language("en"))

        help_menu = tk.Menu(menubar, tearoff=0, font=self.font_main, bg=self.bg_secondary, fg=self.fg_color, activebackground=self.shadow_dark, activeforeground=self.fg_color)
        help_menu.add_command(label=L["menu_guide"], command=self.show_guide, accelerator="F1")
        help_menu.add_separator()
        help_menu.add_command(label=L["menu_about"], command=self.show_about)

        menubar.add_cascade(label=L["menu_file"], menu=file_menu)
        menubar.add_cascade(label=L["menu_edit"], menu=self.edit_menu)
        menubar.add_cascade(label=L["menu_tools"], menu=tools_menu)
        menubar.add_cascade(label=L["menu_view"], menu=view_menu)
        menubar.add_cascade(label=L["menu_language"], menu=lang_menu)
        menubar.add_cascade(label=L["menu_help"], menu=help_menu)
        self.root.config(menu=menubar)

        self.root.bind("<F1>", lambda _: self.show_guide())

    def _update_edit_menu(self) -> None:
        L = self.lang
        widget = self.root.focus_get()
        has_selection = False
        try:
            if isinstance(widget, tk.Text):
                has_selection = bool(widget.tag_ranges("sel"))
            elif isinstance(widget, tk.Entry):
                has_selection = widget.select_present()
        except tk.TclError:
            pass

        state = "normal" if has_selection else "disabled"
        self.edit_menu.entryconfig(L["menu_cut"], state=state)
        self.edit_menu.entryconfig(L["menu_copy"], state=state)

        try:
            clipboard = self.root.clipboard_get()
            paste_state = "normal" if clipboard else "disabled"
        except tk.TclError:
            paste_state = "disabled"

        self.edit_menu.entryconfig(L["menu_paste"], state=paste_state)

    def select_tool(self, tool_name: str) -> None:
        if hasattr(self, 'main_view'):
            self.active_tool_var.set(tool_name)
            self.main_view.tool_var.set(tool_name)
            self.main_view.on_tool_change()

    def _trigger_os_event(self, event_str: str) -> None:
        try:
            widget = self.root.focus_get()
            if not isinstance(widget, (tk.Text, tk.Entry)):
                widget = getattr(self, 'last_active_widget', None)

            if widget:
                widget.event_generate(event_str)
        except tk.TclError:
            pass

    def _select_all(self) -> None:
        widget = self.root.focus_get()
        if isinstance(widget, tk.Text):
            widget.tag_add("sel", "1.0", "end")
        elif isinstance(widget, tk.Entry):
            widget.select_range(0, "end")

    def build_context_menu(self) -> None:
        L = self.lang
        self.context_menu = tk.Menu(self.root, tearoff=0, font=self.font_main, bg=self.bg_secondary, fg=self.fg_color, activebackground=self.shadow_dark, activeforeground=self.fg_color)
        self.context_menu.add_command(label=L["menu_cut"], command=lambda: self._trigger_os_event("<<Cut>>"))
        self.context_menu.add_command(label=L["menu_copy"], command=lambda: self._trigger_os_event("<<Copy>>"))
        self.context_menu.add_command(label=L["menu_paste"], command=lambda: self._trigger_os_event("<<Paste>>"))
        self.context_menu.add_separator()
        self.context_menu.add_command(label=L["menu_select_all"], command=self._select_all)

        self.root.bind_class("Text", "<Button-3>", self.show_context_menu)
        self.root.bind_class("Entry", "<Button-3>", self.show_context_menu)

    def show_context_menu(self, event: tk.Event) -> None:
        L = self.lang
        widget = event.widget
        widget.focus_set()
        self.last_active_widget = widget

        self.context_menu_open = True

        has_selection = False
        try:
            if isinstance(widget, tk.Text):
                has_selection = bool(widget.tag_ranges("sel"))
            elif isinstance(widget, tk.Entry):
                has_selection = widget.select_present()
        except tk.TclError:
            pass

        self.context_menu.entryconfig(L["menu_cut"], state="normal" if has_selection else "disabled")
        self.context_menu.entryconfig(L["menu_copy"], state="normal" if has_selection else "disabled")

        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu_open = False

    def toggle_always_on_top(self) -> None:
        self.root.wm_attributes("-topmost", self.always_on_top_var.get())

    def build_ui(self) -> None:
        self.root.option_add('*TCombobox*Listbox.selectBackground', self.accent_color)
        self.root.option_add('*TCombobox*Listbox.selectForeground', self.shadow_light)

        style = ttk.Style()
        style.theme_use('classic')

        style.map("TCombobox",
                  selectbackground=[("readonly", self.accent_color), ("focus", self.accent_color)],
                  selectforeground=[("readonly", self.shadow_light), ("focus", self.shadow_light)])

        # Sabit boyutlu konteyner ile Off-Screen Rendering (Clipping) modeli:
        main_container = tk.Frame(self.root, bg=self.bg_color, width=self.s(608), height=self.s(544))
        main_container.place(x=0, y=0, width=self.s(608), height=self.s(544))

        self.main_view = ToolsTab(main_container, self)
        self.main_view.place(x=0, y=0, width=self.s(376), height=self.s(544))

        self.tape_container = tk.Frame(main_container, bg=self.bg_color)
        self.tape_container.pack_propagate(False)
        self.tape_container.place(x=self.s(376), y=0, width=self.s(232), height=self.s(544))
        self._build_paper_tape(self.tape_container)

    def toggle_tape(self, event: Optional[tk.Event] = None) -> None:
        if event:
            self.show_tape_var.set(not self.show_tape_var.get())

        is_open = self.show_tape_var.get()
        x, y = self.root.winfo_x(), self.root.winfo_y()

        if is_open:
            self.root.geometry(f"{self.s(608)}x{self.s(544)}+{x}+{y}")
        else:
            self.root.geometry(f"{self.s(376)}x{self.s(544)}+{x}+{y}")

    def _build_paper_tape(self, parent: tk.Frame) -> None:
        L = self.lang

        offset = self.s(8)
        pad_16 = self.s(16)
        pad_8 = self.s(8)

        tape_block = tk.Frame(parent, bg=self.bg_color, bd=0)
        # Ana defterin sağ tarafında zaten 16px masa boşluğu olduğu için, 
        # aradaki toplam boşluğun 16px olması adına şeridin sol padding'ini 0 yapıyoruz.
        tape_block.pack(fill="both", expand=True, padx=(0, pad_8), pady=(pad_16, pad_16))

        # 1. Katman: Kusursuz 45 derece gölge çizimi (Ana defterle aynı mantık)
        shadow_canvas = PaperShadowCanvas(tape_block, self, offset=offset)
        shadow_canvas.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)

        # 2. Katman: Hesap Şeridi Kağıdı
        paper = tk.Frame(tape_block, bg=self.tape_bg, bd=0)
        paper.pack(side="top", fill="both", expand=True, padx=(0, offset), pady=(0, offset))

        # Yazar Kasa / Rulo Çıkış Yuvası Efekti (Kağıdın çıktığı yerdeki karanlık yarık)
        slot_frame = tk.Frame(paper, bg=self.bg_shadow, height=self.s(6))
        slot_frame.pack(side="top", fill="x")
        tk.Frame(slot_frame, bg=self.shadow_dark, height=1).pack(side="bottom", fill="x")

        tk.Frame(paper, bg=self.shadow_light, height=2).pack(side="top", fill="x")
        tk.Frame(paper, bg=self.shadow_dark, height=2).pack(side="bottom", fill="x")
        tk.Frame(paper, bg=self.shadow_light, width=2).pack(side="left", fill="y")
        tk.Frame(paper, bg=self.shadow_dark, width=2).pack(side="right", fill="y")

        header_frame = tk.Frame(paper, bg=self.tape_bg)
        header_frame.pack(fill="x", pady=(16, 8))
        tk.Label(header_frame, text=L["tape_header"], font=self.font_bold, fg=self.accent_color, bg=self.tape_bg).pack()
        tk.Label(paper, text="- "*13, font=self.font_small, fg=self.shadow_dark, bg=self.tape_bg).pack(fill="x")

        self.tape_text = tk.Text(paper, font=self.font_small, bg=self.tape_bg, fg=self.fg_color, bd=0, highlightthickness=0, wrap="word", state="disabled", padx=16, pady=8, selectbackground=self.shadow_dark, selectforeground=self.fg_color)
        self.tape_text.pack(fill="both", expand=True)

        self.tape_text.tag_configure("header", foreground=self.text_secondary, font=(self.font_main[0], 8, "bold"))
        self.tape_text.tag_configure("result", foreground=self.accent_color, font=self.font_bold)
        self.tape_text.tag_configure("flash", background=self.shadow_dark)

        btn_frame = tk.Frame(paper, bg=self.tape_bg)
        btn_frame.pack(fill="x", pady=(8, 16), padx=16)

        copy_btn = tk.Button(btn_frame, text=L["tape_copy_btn"], font=self.font_small, bg=self.tape_bg, fg=self.text_secondary, bd=1, relief="raised", activebackground=self.tab_inactive_bg, cursor="hand2", command=self._copy_tape)
        copy_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))
        
        self.tape_clear_btn = tk.Button(btn_frame, text=L["tape_clear_btn"], font=self.font_small, bg=self.tape_bg, fg=self.text_secondary, bd=1, relief="raised", activebackground=self.tab_inactive_bg, cursor="hand2", command=self._clear_tape)
        self.tape_clear_btn.pack(side="left", fill="x", expand=True, padx=(4, 0))

        for btn in (copy_btn, self.tape_clear_btn):
            btn.bind("<Button-1>", lambda e, b=btn: b.config(relief="sunken"))
            btn.bind("<ButtonRelease-1>", lambda e, b=btn: b.config(relief="raised"))

    def _copy_tape(self) -> None:
        content = self.tape_text.get("1.0", tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.root.update()

    def _clear_tape(self, from_keyboard: bool = False) -> None:
        if from_keyboard and hasattr(self, 'tape_clear_btn') and self.tape_clear_btn.winfo_exists():
            self.tape_clear_btn.config(relief="sunken", bg=self.tab_inactive_bg)
            self.root.after(150, lambda: self.tape_clear_btn.config(relief="raised", bg=self.tape_bg) if self.tape_clear_btn.winfo_exists() else None)

        self.tape_text.config(state="normal")
        self.tape_text.delete("1.0", tk.END)
        self.tape_text.config(state="disabled")
        if hasattr(self, '_print_queue'):
            self._print_queue.clear()

    def add_to_tape(self, title: str, details: str, result: str) -> None:
        self.tape_text.config(state="normal")

        # Memory leak önlemi: Satır sayısı 500'ü aşarsa en eski kayıtları silerek RAM'i sabit tutar
        num_lines = int(self.tape_text.index("end-1c").split(".")[0])
        if num_lines > 500:
            self.tape_text.delete("1.0", f"{num_lines - 450}.0")

        start_idx = self.tape_text.index("end-1c")
        if start_idx != "1.0":
            self.tape_text.insert(tk.END, "\n")
            start_idx = self.tape_text.index("end-1c")

        saat = datetime.now().strftime("%H:%M:%S")
        
        lines_to_print = [
            (f"{title} ({saat})\n", "header"),
            *[(f"{line}\n", "normal") for line in details.split('\n')],
            (f"{'-'*24}\n", "normal"),
            (f"{self.lang['tape_result_label']}: {result}\n", "result"),
            (f"{'='*24}\n", "normal")
        ]

        if not hasattr(self, '_print_queue'):
            self._print_queue = []
            self._is_printing = False

        # Her satırı (metin, etiket, başlangıç_indexi) olarak sıraya ekle
        for item in lines_to_print:
            self._print_queue.append((item[0], item[1], start_idx))

        if self._is_printing:
            return
            
        self._is_printing = True
        
        def print_next():
            if not self._print_queue:
                self._is_printing = False
                # Yazdırma bittikten sonra şerit parlaklığını ana arayüzle senkron (600ms) olarak kaldır
                self.root.after(600, lambda: self.tape_text.tag_remove("flash", "1.0", tk.END))
                return
                
            self.tape_text.config(state="normal")
            text, tag, flash_idx = self._print_queue.pop(0)
            self.tape_text.insert(tk.END, text, tag)
            self.tape_text.tag_add("flash", flash_idx, tk.END)
            self.tape_text.see(tk.END)
            self.tape_text.config(state="disabled")
            
            # Mekanik nokta vuruşlu yazıcı hissi için 30ms gecikme
            self.root.after(30, print_next)

        print_next()
        self.root.bind('<Escape>', self.clear_all)
        self.root.bind('<Control-Tab>', lambda e: self.main_view.cycle_tools(e))

    def clear_all(self, _event: Optional[tk.Event] = None) -> None:
        from_keyboard = bool(_event)
        if hasattr(self, 'main_view'):
            self.main_view.clear_data(from_keyboard=from_keyboard)
        if hasattr(self, 'tape_text'):
            self._clear_tape(from_keyboard=from_keyboard)

    def _create_centered_modal(self, title: str, width: int, height: int) -> tk.Toplevel:
        modal = tk.Toplevel(self.root)
        modal.withdraw()

        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        icon_path = os.path.join(base_path, "app_icon.ico")
        if os.path.exists(icon_path):
            modal.iconbitmap(icon_path)

        modal.title(title)
        modal.resizable(False, False)
        modal.config(bg=self.bg_color)

        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (width // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (height // 2)
        modal.geometry(f"{width}x{height}+{x}+{y}")

        modal.transient(self.root)
        modal.grab_set()
        modal.focus_set()

        return modal

    def show_about(self) -> None:
        L = self.lang
        about_win = self._create_centered_modal(L["about_title"], self.s(272), self.s(168))
        about_win.config(bg=self.bg_secondary)

        tk.Label(about_win, text=L["app_name"], font=(self.font_bold[0], 16, "bold"), fg=self.fg_color, bg=self.bg_secondary).pack(pady=(16, 2))
        tk.Label(about_win, text=f"v{self.app_version} (Build {self.build_year})", font=self.font_main, fg=self.text_secondary, bg=self.bg_secondary).pack()

        copyright_text = L["about_copyright"].format(year=self.build_year)
        tk.Label(about_win, text=copyright_text, font=(self.font_main[0], 8), fg=self.text_disabled, bg=self.bg_secondary, justify="center").pack(pady=(8, 16))

        close_btn = tk.Button(about_win, text=L["about_ok"], font=self.font_bold, bg=self.accent_color, fg=self.shadow_light,
                              bd=2, relief="raised", activebackground=self.accent_hover, activeforeground=self.shadow_light, cursor="hand2", command=about_win.destroy)
        close_btn.pack(pady=(0, 16), ipadx=24)

        about_win.deiconify()

    def show_guide(self) -> None:
        L = self.lang
        guide_win = self._create_centered_modal(L["guide_title"], self.s(376), self.s(608))
        guide_win.config(bg=self.bg_secondary)

        tk.Label(guide_win, text=L["guide_heading"], font=(self.font_bold[0], 16, "bold"), fg=self.accent_color, bg=self.bg_secondary).pack(anchor="w", padx=24, pady=(24, 6))
        tk.Frame(guide_win, bg=self.shadow_dark, height=1).pack(fill="x", padx=24, pady=(0, 8))

        close_btn = tk.Button(guide_win, text=L["guide_ok"], font=self.font_bold, bg=self.accent_color, fg=self.shadow_light,
                              bd=2, relief="raised", activebackground=self.accent_hover, activeforeground=self.shadow_light, cursor="hand2", command=guide_win.destroy)
        close_btn.pack(side="bottom", pady=(8, 24), ipadx=24)

        text_frame = tk.Frame(guide_win, bg=self.bg_secondary)
        text_frame.pack(fill="both", expand=True, padx=24, pady=(0, 8))

        guide_text = tk.Text(text_frame, font=self.font_main, bg=self.bg_secondary, fg=self.text_secondary, wrap="word",
                             bd=0, highlightthickness=0, padx=16, pady=8, cursor="arrow", selectbackground=self.shadow_dark, selectforeground=self.fg_color)
        guide_text.pack(side="left", fill="both", expand=True)

        # Tipografik Stil ve Paragraf Yönetimi
        guide_text.tag_configure("header", font=(self.font_bold[0], 12, "bold"), foreground=self.accent_color, spacing1="16", spacing3="8")
        guide_text.tag_configure("highlight", font=self.font_bold, foreground=self.fg_color)
        
        guide_text.tag_configure("bullet", foreground=self.accent_color, font=self.font_bold, spacing2="4", spacing3="8", lmargin1=str(self.s(8)), lmargin2=str(self.s(24)))
        guide_text.tag_configure("list_item", spacing2="4", spacing3="8", lmargin1=str(self.s(8)), lmargin2=str(self.s(24)))

        guide_text.tag_configure("key", font=(self.font_main[0], 9, "bold"), background=self.tab_inactive_bg, foreground=self.fg_color, relief="raised", borderwidth="1", spacing2="4", spacing3="8", lmargin1=str(self.s(8)), lmargin2=str(self.s(120)), tabs=(str(self.s(120)), "left"))
        guide_text.tag_configure("shortcut", spacing2="4", spacing3="8", lmargin1=str(self.s(8)), lmargin2=str(self.s(120)), tabs=(str(self.s(120)), "left"))

        for text, tag in L["guide_content"]:
            guide_text.insert(tk.END, text, tag)

        guide_text.bind("<Key>", lambda e: "break" if e.keysym not in ("c", "C") or not (isinstance(e.state, int) and (e.state & 0x0004)) else None)

        guide_win.bind('<Escape>', lambda e: guide_win.destroy())
        guide_win.bind('<Return>', lambda e: guide_win.destroy())

        guide_win.deiconify()
