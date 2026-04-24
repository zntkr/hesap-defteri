import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import os
import sys
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
        
        self.build_ui()
        self.build_menu()
        self.build_context_menu()

    def build_menu(self) -> None:
        menubar = tk.Menu(self.root, font=self.font_main, bg=self.bg_secondary, fg=self.fg_color, activebackground=self.accent_color, activeforeground=self.shadow_light)

        file_menu = tk.Menu(menubar, tearoff=0, font=self.font_main, bg=self.bg_secondary, fg=self.fg_color, activebackground=self.accent_color, activeforeground=self.shadow_light)
        file_menu.add_command(label="Dışa Aktar (Çok Yakında)", state="disabled")
        file_menu.add_separator()
        file_menu.add_command(label="Çıkış", command=self.root.quit, accelerator="Alt+F4")

        self.edit_menu = tk.Menu(menubar, tearoff=0, font=self.font_main, bg=self.bg_secondary, fg=self.fg_color, activebackground=self.accent_color, activeforeground=self.shadow_light, postcommand=self._update_edit_menu)
        self.edit_menu.add_command(label="Geri Al", command=lambda: self._trigger_os_event("<<Undo>>"), accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Yeniden Yap", command=lambda: self._trigger_os_event("<<Redo>>"), accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Kes", command=lambda: self._trigger_os_event("<<Cut>>"), accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Kopyala", command=lambda: self._trigger_os_event("<<Copy>>"), accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Yapıştır", command=lambda: self._trigger_os_event("<<Paste>>"), accelerator="Ctrl+V")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Tümünü Seç", command=self._select_all, accelerator="Ctrl+A")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Tümünü Temizle", command=self.clear_all, accelerator="Esc")

        tools_menu = tk.Menu(menubar, tearoff=0, font=self.font_main, bg=self.bg_secondary, fg=self.fg_color, activebackground=self.accent_color, activeforeground=self.shadow_light)
        self.active_tool_var = tk.StringVar()
        for i, tool_name in enumerate(self.main_view.frames.keys(), start=1):
            accel = f"Ctrl+{i}"
            tools_menu.add_radiobutton(label=tool_name, variable=self.active_tool_var, value=tool_name, command=lambda name=tool_name: self.select_tool(name), accelerator=accel)
            self.root.bind(f"<Control-Key-{i}>", lambda e, name=tool_name: self.select_tool(name))

        view_menu = tk.Menu(menubar, tearoff=0, font=self.font_main, bg=self.bg_secondary, fg=self.fg_color, activebackground=self.accent_color, activeforeground=self.shadow_light)
        view_menu.add_checkbutton(label="Her Zaman Üstte Tut", variable=self.always_on_top_var, command=self.toggle_always_on_top)

        help_menu = tk.Menu(menubar, tearoff=0, font=self.font_main, bg=self.bg_secondary, fg=self.fg_color, activebackground=self.accent_color, activeforeground=self.shadow_light)
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
        self.context_menu = tk.Menu(self.root, tearoff=0, font=self.font_main, bg=self.bg_secondary, fg=self.fg_color, activebackground=self.accent_color, activeforeground=self.shadow_light)
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
        
        style.configure("TNotebook", background=self.bg_color, borderwidth=0, tabmargins=[0, 2, 2, 0],
                        lightcolor=self.shadow_light, darkcolor=self.shadow_dark)
        
        style.configure("TNotebook.Tab", 
                        background=self.bg_secondary, foreground=self.fg_color, font=self.font_main, 
                        padding=[16, 8], borderwidth=2,
                        lightcolor=self.shadow_light, darkcolor=self.shadow_dark,
                        focuscolor="", focusthickness=0)
        
        style.map("TNotebook.Tab", 
                  background=[("selected", self.bg_secondary)], 
                  foreground=[("selected", self.accent_color)],
                  expand=[("selected", [2, 2, 2, 2])]) 

        self.main_view = ToolsTab(self.root, self)
        self.main_view.pack(expand=True, fill="both")
        
        # --- KLAVYE KISAYOLLARI (KEYBOARD-FIRST) ---
        self.root.bind('<Escape>', self.clear_all)
        self.root.bind('<Control-Tab>', lambda e: self.main_view.cycle_tools(e))

    def clear_all(self, event: Optional[tk.Event] = None) -> None:
        if hasattr(self, 'main_view'):
            self.main_view.clear_data()

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

        tk.Label(about_win, text=self.app_name, font=(self.font_bold[0], 14, "bold"), fg=self.fg_color, bg=self.bg_color).pack(pady=(32, 4))
        tk.Label(about_win, text=f"Versiyon {self.app_version} (Build {self.build_year})", font=self.font_main, fg=self.text_secondary, bg=self.bg_color).pack()
        
        copyright_text = f"Telif Hakkı © {self.build_year} | MIT Lisansı\nSıfır bloatware, maksimum odak."
        tk.Label(about_win, text=copyright_text, font=(self.font_main[0], 8), fg=self.text_disabled, bg=self.bg_color, justify="center").pack(pady=(16, 16))

        close_btn = tk.Button(about_win, text="TAMAM", font=self.font_bold, bg=self.accent_color, fg=self.shadow_light, 
                              bd=2, relief="raised", activebackground=self.accent_hover, activeforeground=self.shadow_light, cursor="hand2", command=about_win.destroy)
        close_btn.pack(pady=(0, 24), ipadx=24, ipady=4)
        
        about_win.deiconify()

    def show_guide(self) -> None:
        guide_win = self._create_centered_modal("Kullanma Rehberi", 520, 504)

        guide_title = "KULLANMA REHBERİ"
        tk.Label(guide_win, text=guide_title, font=(self.font_bold[0], 13, "bold"), fg=self.accent_color, bg=self.bg_color).pack(anchor="w", padx=16, pady=(16, 8))

        # Butonu alta yerleştir (Önce paketlenir ki taşma durumunda kesilmesin)
        close_btn = tk.Button(guide_win, text="TAMAM", font=self.font_bold, bg=self.accent_color, fg=self.shadow_light, 
                              bd=2, relief="raised", activebackground=self.accent_hover, activeforeground=self.shadow_light, cursor="hand2", command=guide_win.destroy)
        close_btn.pack(side="bottom", pady=(8, 16), ipadx=16, ipady=4)

        text_frame = tk.Frame(guide_win, bg=self.bg_color)
        text_frame.pack(fill="both", expand=True, padx=16, pady=(0, 8))
        
        guide_text = tk.Text(text_frame, font=self.font_main, bg=self.bg_secondary, fg=self.text_secondary, 
                             wrap="word", bd=1, relief="sunken", padx=16, pady=16, cursor="arrow")
        guide_text.pack(side="left", fill="both", expand=True)

        # Metin içi stil etiketleri (Tags)
        guide_text.tag_configure("header", font=self.font_bold, foreground=self.accent_color, spacing1=8, spacing3=4)
        guide_text.tag_configure("highlight", font=self.font_bold, foreground=self.fg_color)
        guide_text.tag_configure("key", font=self.font_bold, foreground=self.shadow_light, background=self.accent_color)
        guide_text.tag_configure("bullet", foreground=self.accent_color, font=self.font_bold)

        content = [
            ("ORTALAMA HESAPLAMA MOTORU\n", "header"),
            ("• ", "bullet"), ("Agnostik Veri Girişi: ", "highlight"), ("Kopyaladığınız metinleri doğrudan yapıştırın. Sistem harfleri ve boşlukları yoksayarak içindeki sayıları (TR/US formatlı) otomatik ayıklar.\n", "normal"),
            ("• ", "bullet"), ("Tek Tıkla Kopyalama: ", "highlight"), ("Hesaplanan Sayının üzerine tıklayarak değeri kopyalayabilirsiniz.\n", "normal"),
            
            ("ARAÇ KUTUSU\n", "header"),
            ("• ", "bullet"), ("Geniş Yelpaze: ", "highlight"), ("Ofis ihtiyaçlarınız için programlanmış araçlara açılır menüden geçiş yapabilirsiniz.\n", "normal"),

            ("KLAVYE KISAYOLLARI\n", "header"),
            (" [ Enter ] ", "key"), ("    Aktif araçta hesaplama talimatını verir.\n", "normal"),
            (" [ ESC ] ", "key"), ("      Verileri anında temizler ve işaretçiyi odaklar.\n", "normal"),
            (" [ Ctrl+Tab ] ", "key"), (" Araçlar arasında hızlı geçiş yapar.\n", "normal"),
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