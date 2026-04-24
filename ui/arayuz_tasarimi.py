import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import os
import sys
from datetime import datetime
from typing import Optional, Any

# Proje kök dizinini Python yoluna ekle (Pylance import hatalarını önlemek için)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui.tools_tab import ToolsTab

class MainUI:
    """
    Main Orchestrator class for the UI (Presentation Layer).
    Manages the application state, menus, and tab component instantiation.
    """
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        
        # --- APP CONFIG ---
        self.app_name = "Hesap Defteri"
        self.app_version = "1.0.0"
        self.build_year = "2026"
        self.date_placeholder = "GG.AA.YYYY"
        
        self.root.title(f"{self.app_name} - v{self.app_version}")
        self.root.geometry("432x544") 
        self.root.resizable(False, False)
        
        # --- NEO-RETRO THEME VARIABLES ---
        self.bg_color = "#4A423A" # Koyu grimsi ahşap/deri masa
        self.bg_shadow = "#38322C" # Masaya düşen 45 derece solid gölge
        self.fg_color = "#2D2D2D"
        self.accent_color = "#C85A47"
        self.accent_hover = "#A84534"
        self.accent_light = "#E08D7D"
        self.border_color = "#E0DCE3"
        self.shadow_dark = "#D3CFC8"
        self.shadow_light = "#FFFFFF"
        self.text_secondary = "#666666"
        self.text_disabled = "#B0B0B0"
        self.bg_secondary = "#EFEBE6"
        self.tape_bg = "#F4F1EA" # Hesap şeridi (yazar kasa fişi) için sarımsı saman kağıdı
        self.input_bg = "#F9F8F6" # Saf beyaz yerine defter kağıdından bir tık açık krem
        self.error_color = "#D32F2F"
        self.text_placeholder = "#888888"
        self.text_inverse = "#D0CFCB" # Koyu arka planlar için açık krem/gri
        self.tab_inactive_bg = "#5A524A" # Pasif sekmelerin masa üzerindeki gölgeli rengi
        
        # --- TYPOGRAPHY ---
        available_fonts = tkfont.families()
        preferred_fonts = ["IBM Plex Mono", "Consolas", "Courier New", "Courier"]
        selected_font = next((f for f in preferred_fonts if f in available_fonts), "Courier")
        
        self.font_main = (selected_font, 10)
        self.font_bold = (selected_font, 10, "bold")
        self.font_small = (selected_font, 8)
        self.font_title = (selected_font, 24)
        
        self.placeholder_text = "Sayıları yazın veya bir liste yapıştırın...\nÖrn: 150  22.5  300  1.250,75"
        self.root.config(bg=self.bg_color)
        self.always_on_top_var = tk.BooleanVar(value=False)
        self.show_tape_var = tk.BooleanVar(value=False)
        
        self.build_ui()
        self.build_menu()
        self.build_context_menu()

    def build_menu(self) -> None:
        menubar = tk.Menu(self.root, font=self.font_main, bg=self.bg_secondary, fg=self.fg_color, activebackground=self.shadow_dark, activeforeground=self.fg_color)

        file_menu = tk.Menu(menubar, tearoff=0, font=self.font_main, bg=self.bg_secondary, fg=self.fg_color, activebackground=self.shadow_dark, activeforeground=self.fg_color)
        file_menu.add_command(label="Çıkış", command=self.root.quit, accelerator="Alt+F4")

        self.edit_menu = tk.Menu(menubar, tearoff=0, font=self.font_main, bg=self.bg_secondary, fg=self.fg_color, activebackground=self.shadow_dark, activeforeground=self.fg_color, postcommand=self._update_edit_menu)
        self.edit_menu.add_command(label="Kes", command=lambda: self._trigger_os_event("<<Cut>>"), accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Kopyala", command=lambda: self._trigger_os_event("<<Copy>>"), accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Yapıştır", command=lambda: self._trigger_os_event("<<Paste>>"), accelerator="Ctrl+V")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Tümünü Seç", command=self._select_all, accelerator="Ctrl+A")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Tümünü Temizle", command=self.clear_all, accelerator="Esc")

        tools_menu = tk.Menu(menubar, tearoff=0, font=self.font_main, bg=self.bg_secondary, fg=self.fg_color, activebackground=self.shadow_dark, activeforeground=self.fg_color)
        self.active_tool_var = tk.StringVar()
        for i, tool_name in enumerate(self.main_view.frames.keys(), start=1):
            accel = f"Ctrl+{i}"
            tools_menu.add_radiobutton(label=tool_name, variable=self.active_tool_var, value=tool_name, command=lambda name=tool_name: self.select_tool(name), accelerator=accel)
            self.root.bind(f"<Control-Key-{i}>", lambda e, name=tool_name: self.select_tool(name))

        view_menu = tk.Menu(menubar, tearoff=0, font=self.font_main, bg=self.bg_secondary, fg=self.fg_color, activebackground=self.shadow_dark, activeforeground=self.fg_color)
        view_menu.add_checkbutton(label="Her Zaman Üstte Tut", variable=self.always_on_top_var, command=self.toggle_always_on_top)
        view_menu.add_separator()
        view_menu.add_checkbutton(label="Hesap Şeridini Göster", variable=self.show_tape_var, command=self.toggle_tape, accelerator="Ctrl+H")
        
        self.root.bind("<Control-h>", self.toggle_tape)
        self.root.bind("<Control-H>", self.toggle_tape)

        help_menu = tk.Menu(menubar, tearoff=0, font=self.font_main, bg=self.bg_secondary, fg=self.fg_color, activebackground=self.shadow_dark, activeforeground=self.fg_color)
        help_menu.add_command(label="Kullanma Rehberi", command=self.show_guide, accelerator="F1")
        help_menu.add_separator()
        help_menu.add_command(label="Hakkında", command=self.show_about)
        
        menubar.add_cascade(label="Dosya", menu=file_menu)
        menubar.add_cascade(label="Düzenle", menu=self.edit_menu)
        menubar.add_cascade(label="Araçlar", menu=tools_menu)
        menubar.add_cascade(label="Görünüş", menu=view_menu)
        menubar.add_cascade(label="Yardım", menu=help_menu)
        self.root.config(menu=menubar)
        
        self.root.bind("<F1>", lambda e: self.show_guide())

    def _update_edit_menu(self) -> None:
        """Düzenle menüsü açılmadan hemen önce tetiklenir ve öğelerin aktif/pasif durumunu belirler."""
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
        self.edit_menu.entryconfig("Kes", state=state)
        self.edit_menu.entryconfig("Kopyala", state=state)
        
        # Yapıştır kontrolü (Pano boş mu dolu mu)
        try:
            clipboard = self.root.clipboard_get()
            paste_state = "normal" if clipboard else "disabled"
        except tk.TclError:
            paste_state = "disabled"
            
        self.edit_menu.entryconfig("Yapıştır", state=paste_state)

    def select_tool(self, tool_name: str) -> None:
        """Üst menüden seçilen aracı aktif eder ve Araçlar sekmesine geçer."""
        if hasattr(self, 'main_view'):
            self.active_tool_var.set(tool_name)
            self.main_view.tool_var.set(tool_name)
            self.main_view.on_tool_change()

    def _trigger_os_event(self, event_str: str) -> None:
        """İşletim sisteminin yerleşik Kes/Kopyala/Yapıştır olaylarını (Virtual Events) tetikler."""
        try:
            widget = self.root.focus_get()
            if not isinstance(widget, (tk.Text, tk.Entry)):
                widget = getattr(self, 'last_active_widget', None)
                
            if widget:
                widget.event_generate(event_str)
        except tk.TclError:
            pass # Odaklanan widget (örn: buton) bu işlemi desteklemiyorsa sessizce yoksay

    def _select_all(self) -> None:
        """Aktif metin kutusundaki tüm içeriği seçer."""
        widget = self.root.focus_get()
        if isinstance(widget, tk.Text):
            widget.tag_add("sel", "1.0", "end")
        elif isinstance(widget, tk.Entry):
            widget.select_range(0, "end")

    def build_context_menu(self) -> None:
        """Metin kutuları için sağ tık (bağlam) menüsünü oluşturur ve sisteme bağlar."""
        self.context_menu = tk.Menu(self.root, tearoff=0, font=self.font_main, bg=self.bg_secondary, fg=self.fg_color, activebackground=self.shadow_dark, activeforeground=self.fg_color)
        self.context_menu.add_command(label="Kes", command=lambda: self._trigger_os_event("<<Cut>>"))
        self.context_menu.add_command(label="Kopyala", command=lambda: self._trigger_os_event("<<Copy>>"))
        self.context_menu.add_command(label="Yapıştır", command=lambda: self._trigger_os_event("<<Paste>>"))
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Tümünü Seç", command=self._select_all)
        
        # Tüm Entry ve Text widget'larına sağ tık menüsünü otomatik bağla
        self.root.bind_class("Text", "<Button-3>", self.show_context_menu)
        self.root.bind_class("Entry", "<Button-3>", self.show_context_menu)

    def _check_and_restore_placeholder(self, widget: Any) -> None:
        """Menü kapandıktan sonra kutu boş kalmışsa yer tutucuyu geri getirir."""
        if isinstance(widget, tk.Text) and not widget.get("1.0", "end-1c").strip():
            widget.event_generate("<FocusOut>")
        elif isinstance(widget, tk.Entry) and not widget.get().strip():
            widget.event_generate("<FocusOut>")

    def show_context_menu(self, event: tk.Event) -> None:
        widget = event.widget
        widget.focus_set()
        self.last_active_widget = widget
        
        # Yer tutucuları sağ tıklandığı an güvenle temizle
        if isinstance(widget, tk.Text) and widget.get("1.0", "end-1c") == self.placeholder_text:
            widget.delete("1.0", tk.END)
            widget.config(fg=self.fg_color)
        elif isinstance(widget, tk.Entry) and widget.get() == self.date_placeholder:
            widget.delete(0, tk.END)
            widget.config(fg=self.fg_color)
            
        self.context_menu_open = True
        
        # Metin seçili mi diye kontrol et
        has_selection = False
        try:
            if isinstance(widget, tk.Text):
                has_selection = bool(widget.tag_ranges("sel"))
            elif isinstance(widget, tk.Entry):
                has_selection = widget.select_present()
        except tk.TclError:
            pass

        self.context_menu.entryconfig("Kes", state="normal" if has_selection else "disabled")
        self.context_menu.entryconfig("Kopyala", state="normal" if has_selection else "disabled")
        
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu_open = False
            self.root.after(50, lambda: self._check_and_restore_placeholder(widget))

    def toggle_always_on_top(self) -> None:
        self.root.wm_attributes("-topmost", self.always_on_top_var.get())

    def build_ui(self) -> None:
        # Combobox'ın açılan listesindeki mavi işletim sistemi seçim rengini kiremit rengine ezme
        self.root.option_add('*TCombobox*Listbox.selectBackground', self.accent_color)
        self.root.option_add('*TCombobox*Listbox.selectForeground', self.shadow_light)
        
        style = ttk.Style()
        style.theme_use('classic') 
        
        style.map("TCombobox", 
                  selectbackground=[("readonly", self.accent_color), ("focus", self.accent_color)],
                  selectforeground=[("readonly", self.shadow_light), ("focus", self.shadow_light)])
        
        style.configure("TNotebook", background=self.bg_color, borderwidth=0, tabmargins=[0, 2, 10, 0],
                        lightcolor=self.shadow_light, darkcolor=self.shadow_dark)
        
        style.configure("TNotebook.Tab", 
                        background=self.bg_secondary, foreground=self.fg_color, font=self.font_main, 
                        padding=[16, 8], borderwidth=2,
                        lightcolor=self.shadow_light, darkcolor=self.shadow_dark,
                        bordercolor=self.shadow_dark,
                        focuscolor="", focusthickness=0)
        
        style.map("TNotebook.Tab", 
                  background=[("selected", self.bg_secondary)], 
                  foreground=[("selected", self.accent_color)],
                  expand=[("selected", [2, 2, 2, 2])]) 

        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(expand=True, fill="both")
        
        self.tape_container = tk.Frame(main_container, bg=self.bg_color, width=240)
        self.tape_container.pack_propagate(False)
        self._build_paper_tape(self.tape_container)
        
        self.main_view = ToolsTab(main_container, self)
        self.main_view.pack(side="left", expand=True, fill="both")
        
        # --- KLAVYE KISAYOLLARI (KEYBOARD-FIRST) ---

    def toggle_tape(self, event: Optional[tk.Event] = None) -> None:
        if event:
            self.show_tape_var.set(not self.show_tape_var.get())
            
        is_open = self.show_tape_var.get()
        x, y = self.root.winfo_x(), self.root.winfo_y()
        
        if is_open:
            self.root.geometry(f"688x544+{x}+{y}")
            self.tape_container.pack(side="right", fill="y", padx=(0, 16), pady=16, before=self.main_view)
        else:
            self.root.geometry(f"432x544+{x}+{y}")
            self.tape_container.pack_forget()

    def _build_paper_tape(self, parent: tk.Frame) -> None:
        """Ekranın sağ tarafındaki fiziksel 'Hesap Şeridi'ni (Yazar Kasa Fişi) inşa eder."""
        wrapper = tk.Frame(parent, bg=self.bg_color, bd=0)
        wrapper.pack(fill="both", expand=True)

        tk.Frame(wrapper, bg=self.bg_shadow, height=8).pack(side="bottom", fill="x", padx=(8, 0))
        middle = tk.Frame(wrapper, bg=self.bg_color, bd=0)
        middle.pack(side="top", fill="both", expand=True)
        tk.Frame(middle, bg=self.bg_shadow, width=8).pack(side="right", fill="y", pady=(8, 0))

        paper = tk.Frame(middle, bg=self.tape_bg, bd=0)
        paper.pack(side="left", fill="both", expand=True)

        tk.Frame(paper, bg=self.shadow_light, width=2).pack(side="left", fill="y")
        tk.Frame(paper, bg=self.shadow_dark, width=2).pack(side="right", fill="y")
        tk.Frame(paper, bg=self.shadow_dark, height=2).pack(side="bottom", fill="x")

        header_frame = tk.Frame(paper, bg=self.tape_bg)
        header_frame.pack(fill="x", pady=(16, 8))
        tk.Label(header_frame, text="HESAP ŞERİDİ", font=(self.font_bold[0], 9, "bold"), fg=self.accent_color, bg=self.tape_bg).pack()
        tk.Label(paper, text="- "*18, font=self.font_small, fg=self.shadow_dark, bg=self.tape_bg).pack(fill="x")

        self.tape_text = tk.Text(paper, font=self.font_small, bg=self.tape_bg, fg=self.fg_color, bd=0, highlightthickness=0, wrap="word", state="disabled", padx=16, pady=8)
        self.tape_text.pack(fill="both", expand=True)
        
        self.tape_text.tag_configure("header", foreground=self.text_secondary, font=(self.font_main[0], 8, "bold"))
        self.tape_text.tag_configure("result", foreground=self.fg_color, font=(self.font_bold[0], 9, "bold"))
        self.tape_text.tag_configure("flash", background=self.shadow_dark)
        
        btn_frame = tk.Frame(paper, bg=self.tape_bg)
        btn_frame.pack(fill="x", pady=16, padx=16)
        
        tk.Button(btn_frame, text="Kopyala", font=self.font_small, bg=self.tape_bg, fg=self.fg_color, bd=1, relief="raised", cursor="hand2", command=self._copy_tape).pack(side="left", fill="x", expand=True, padx=(0, 4))
        tk.Button(btn_frame, text="Temizle", font=self.font_small, bg=self.tape_bg, fg=self.text_secondary, bd=1, relief="raised", cursor="hand2", command=self._clear_tape).pack(side="left", fill="x", expand=True, padx=(4, 0))

    def _copy_tape(self) -> None:
        content = self.tape_text.get("1.0", tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.root.update()

    def _clear_tape(self) -> None:
        self.tape_text.config(state="normal")
        self.tape_text.delete("1.0", tk.END)
        self.tape_text.config(state="disabled")

    def add_to_tape(self, title: str, details: str, result: str) -> None:
        self.tape_text.config(state="normal")
        
        start_idx = self.tape_text.index("end-1c")
        if start_idx != "1.0": 
            self.tape_text.insert(tk.END, "\n")
            start_idx = self.tape_text.index("end-1c")
            
        saat = datetime.now().strftime("%H:%M:%S")
        self.tape_text.insert(tk.END, f"{title} ({saat})\n", "header")
        self.tape_text.insert(tk.END, f"{details}\n{'-'*24}\n", "normal")
        self.tape_text.insert(tk.END, f"Sonuç: {result}\n", "result")
        self.tape_text.insert(tk.END, f"{'='*24}\n", "normal")
        
        self.tape_text.tag_add("flash", start_idx, tk.END)
        self.root.after(800, lambda: self.tape_text.tag_remove("flash", "1.0", tk.END))
        
        self.tape_text.see(tk.END)
        self.tape_text.config(state="disabled")
        self.root.bind('<Escape>', self.clear_all)
        self.root.bind('<Control-Tab>', lambda e: self.main_view.cycle_tools(e))

    def clear_all(self, event: Optional[tk.Event] = None) -> None:
        if hasattr(self, 'main_view'):
            self.main_view.clear_data()
        if hasattr(self, 'tape_text'):
            self._clear_tape()

    def _create_centered_modal(self, title: str, width: int, height: int) -> tk.Toplevel:
        """Yardımcı Metot: Belirtilen boyutlarda, ekranın ortasında açılan modal pencere üretir."""
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
        about_win = self._create_centered_modal("Hakkında", 344, 216)
        about_win.config(bg=self.bg_secondary)

        tk.Label(about_win, text=self.app_name, font=(self.font_bold[0], 16, "bold"), fg=self.fg_color, bg=self.bg_secondary).pack(pady=(32, 4))
        tk.Label(about_win, text=f"Versiyon {self.app_version} (Build {self.build_year})", font=self.font_main, fg=self.text_secondary, bg=self.bg_secondary).pack()
        
        copyright_text = f"Telif Hakkı © {self.build_year} | MIT Lisansı\nSıfır bloatware, maksimum odak."
        tk.Label(about_win, text=copyright_text, font=(self.font_main[0], 8), fg=self.text_disabled, bg=self.bg_secondary, justify="center").pack(pady=(16, 16))

        close_btn = tk.Button(about_win, text="TAMAM", font=self.font_bold, bg=self.accent_color, fg=self.shadow_light, 
                              bd=2, relief="raised", activebackground=self.accent_hover, activeforeground=self.shadow_light, cursor="hand2", command=about_win.destroy)
        close_btn.pack(pady=(0, 24), ipadx=24)
        
        about_win.deiconify()

    def show_guide(self) -> None:
        guide_win = self._create_centered_modal("Kullanma Rehberi", 480, 480)
        guide_win.config(bg=self.bg_secondary)

        guide_title = "KULLANMA KILAVUZU"
        tk.Label(guide_win, text=guide_title, font=(self.font_bold[0], 16, "bold"), fg=self.accent_color, bg=self.bg_secondary).pack(anchor="w", padx=24, pady=(24, 8))

        # Butonu alta yerleştir (Önce paketlenir ki taşma durumunda kesilmesin)
        close_btn = tk.Button(guide_win, text="TAMAM", font=self.font_bold, bg=self.accent_color, fg=self.shadow_light, 
                              bd=2, relief="raised", activebackground=self.accent_hover, activeforeground=self.shadow_light, cursor="hand2", command=guide_win.destroy)
        close_btn.pack(side="bottom", pady=(8, 24), ipadx=24)

        text_frame = tk.Frame(guide_win, bg=self.bg_secondary)
        text_frame.pack(fill="both", expand=True, padx=24, pady=(0, 8))
        
        guide_text = tk.Text(text_frame, font=self.font_main, bg=self.bg_secondary, fg=self.text_secondary, 
                             wrap="word", bd=0, highlightthickness=0, padx=0, pady=8, cursor="arrow")
        guide_text.pack(side="left", fill="both", expand=True)

        # Metin içi stil etiketleri (Tags)
        guide_text.tag_configure("header", font=self.font_bold, foreground=self.accent_color, spacing1=8, spacing3=4)
        guide_text.tag_configure("highlight", font=self.font_bold, foreground=self.fg_color)
        guide_text.tag_configure("key", font=self.font_bold, foreground=self.shadow_light, background=self.accent_color)
        guide_text.tag_configure("bullet", foreground=self.accent_color, font=self.font_bold)

        content = [
            ("HESAP DEFTERİ ARAÇLARI\n", "header"),
            ("• ", "bullet"), ("Sekmeli Yapı: ", "highlight"), ("Hesaplama araçlarına (Ortalama, KDV, Yaş vb.) üst kısımdaki sekme kulaklarına tıklayarak anında geçiş yapabilirsiniz.\n", "normal"),
            ("• ", "bullet"), ("Agnostik Veri Girişi: ", "highlight"), ("Metinleri doğrudan yapıştırın. Sistem harfleri yoksayarak içindeki sayıları (TR/US formatlı) otomatik ayıklar.\n", "normal"),
            ("• ", "bullet"), ("Dokunsal Kopyalama: ", "highlight"), ("Hesaplanan bir sonucun üzerine tıkladığınızda değer anında panoya kopyalanır.\n", "normal"),

            ("KLAVYE KISAYOLLARI\n", "header"),
            (" [ Enter ] ", "key"), ("    Aktif araçta hesaplama talimatını verir.\n", "normal"),
            (" [ ESC ] ", "key"), ("      Verileri anında temizler ve işaretçiyi odaklar.\n", "normal"),
            (" [ Ctrl+Tab ] ", "key"), (" Sekmeler (araçlar) arasında sırayla gezinir.\n", "normal"),
            (" [ Ctrl+1..6 ] ", "key"),(" İstediğiniz araca doğrudan geçiş yapar.\n", "normal"),
            (" Sağ Tık ", "key"), ("      Standart Kes/Kopyala/Yapıştır menüsünü açar.\n", "normal"),

            ("DİĞER ÖZELLİKLER\n", "header"),
            ("• ", "bullet"), ("Görünüş ", "highlight"), ("menüsünden pencereyi her zaman üstte tutabilirsiniz.\n", "normal"),
        ]

        for text, tag in content:
            guide_text.insert(tk.END, text, tag if tag != "normal" else "")

        # Sadece klavye girdilerini engelleyerek metni salt okunur ancak seçilebilir/kopyalanabilir yapıyoruz
        guide_text.bind("<Key>", lambda e: "break" if e.keysym not in ("c", "C") or not (isinstance(e.state, int) and (e.state & 0x0004)) else None)
        
        # --- Klavye Kısayolları (Keyboard-First) ---
        guide_win.bind('<Escape>', lambda e: guide_win.destroy())
        guide_win.bind('<Return>', lambda e: guide_win.destroy())
        
        guide_win.deiconify()