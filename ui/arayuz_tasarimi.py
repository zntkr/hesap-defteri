import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import os
import sys
import re

# Proje kök dizinini Python yoluna ekle (Pylance import hatalarını önlemek için)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.matematik_motoru import MatematikMotoru
from ui.dashboard_tab import DashboardTab
from ui.history_tab import HistoryTab
from ui.tools_tab import ToolsTab

class MainUI:
    """
    Main Orchestrator class for the UI (Presentation Layer).
    Manages the application state, menus, and tab component instantiation.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Ortalama Hesaplama v1.0.0")
        self.root.geometry("440x640") 
        self.root.resizable(False, False)
        
        # --- NEO-RETRO THEME VARIABLES ---
        self.bg_color = "#F9F8F6"
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
        
        # --- TYPOGRAPHY ---
        available_fonts = tkfont.families()
        preferred_fonts = ["IBM Plex Mono", "Consolas", "Courier New", "Courier"]
        selected_font = next((f for f in preferred_fonts if f in available_fonts), "Courier")
        
        self.font_main = (selected_font, 10)
        self.font_bold = (selected_font, 10, "bold")
        self.font_title = (selected_font, 24)
        
        self.placeholder_text = "Sayıları yazın veya bir liste yapıştırın...\nÖrn: 150  22.5  300  1.250,75"
        self.root.config(bg=self.bg_color)
        self.history = []
        self.always_on_top_var = tk.BooleanVar(value=False)
        
        self.build_menu()
        self.build_context_menu()
        self.build_ui()

    def build_menu(self):
        menubar = tk.Menu(self.root, font=self.font_main, bg=self.bg_color, fg=self.fg_color, activebackground=self.accent_color, activeforeground=self.shadow_light)
        
        file_menu = tk.Menu(menubar, tearoff=0, font=self.font_main, bg=self.bg_color, fg=self.fg_color, activebackground=self.accent_color, activeforeground=self.shadow_light)
        file_menu.add_command(label="Temizle", command=self.clear_all)
        file_menu.add_separator()
        file_menu.add_command(label="Çıkış", command=self.root.quit)
        
        edit_menu = tk.Menu(menubar, tearoff=0, font=self.font_main, bg=self.bg_color, fg=self.fg_color, activebackground=self.accent_color, activeforeground=self.shadow_light)
        edit_menu.add_command(label="Kes", command=lambda: self._trigger_os_event("<<Cut>>"), accelerator="Ctrl+X")
        edit_menu.add_command(label="Kopyala", command=lambda: self._trigger_os_event("<<Copy>>"), accelerator="Ctrl+C")
        edit_menu.add_command(label="Yapıştır", command=lambda: self._trigger_os_event("<<Paste>>"), accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Tümünü Seç", command=self._select_all, accelerator="Ctrl+A")

        tools_menu = tk.Menu(menubar, tearoff=0, font=self.font_main, bg=self.bg_color, fg=self.fg_color, activebackground=self.accent_color, activeforeground=self.shadow_light)
        tools_menu.add_command(label="Değişim Oranı", command=lambda: self.select_tool("Değişim Oranı"))
        tools_menu.add_command(label="KDV Hesaplayıcı", command=lambda: self.select_tool("KDV Hesaplayıcı"))
        tools_menu.add_command(label="İndirim Hesaplayıcı", command=lambda: self.select_tool("İndirim Hesaplayıcı"))
        tools_menu.add_command(label="Orantı Hesaplayıcı", command=lambda: self.select_tool("Orantı Hesaplayıcı"))
        tools_menu.add_command(label="Yaş Hesaplayıcı", command=lambda: self.select_tool("Yaş Hesaplayıcı"))

        view_menu = tk.Menu(menubar, tearoff=0, font=self.font_main, bg=self.bg_color, fg=self.fg_color, activebackground=self.accent_color, activeforeground=self.shadow_light)
        view_menu.add_checkbutton(label="Her Zaman Üstte Tut", variable=self.always_on_top_var, command=self.toggle_always_on_top)
        
        help_menu = tk.Menu(menubar, tearoff=0, font=self.font_main, bg=self.bg_color, fg=self.fg_color, activebackground=self.accent_color, activeforeground=self.shadow_light)
        help_menu.add_command(label="Kullanma Rehberi", command=self.show_guide)
        help_menu.add_separator()
        help_menu.add_command(label="Hakkında", command=self.show_about)
        
        menubar.add_cascade(label="Dosya", menu=file_menu)
        menubar.add_cascade(label="Düzenle", menu=edit_menu)
        menubar.add_cascade(label="Araçlar", menu=tools_menu)
        menubar.add_cascade(label="Görünüş", menu=view_menu)
        menubar.add_cascade(label="Yardım", menu=help_menu)
        self.root.config(menu=menubar)

    def select_tool(self, tool_name):
        """Üst menüden seçilen aracı aktif eder ve Araçlar sekmesine geçer."""
        self.tabs.select(self.tab_tools)
        self.tab_tools.tool_var.set(tool_name)
        self.tab_tools.on_tool_change()

    def _trigger_os_event(self, event_str):
        """İşletim sisteminin yerleşik Kes/Kopyala/Yapıştır olaylarını (Virtual Events) tetikler."""
        try:
            widget = self.root.focus_get()
            if not isinstance(widget, (tk.Text, tk.Entry)):
                widget = getattr(self, 'last_active_widget', None)
                
            if widget:
                widget.event_generate(event_str)
                if event_str == "<<Paste>>":
                    self.root.after(10, self.update_char_count)
        except tk.TclError:
            pass # Odaklanan widget (örn: buton) bu işlemi desteklemiyorsa sessizce yoksay

    def _select_all(self):
        """Aktif metin kutusundaki tüm içeriği seçer."""
        widget = self.root.focus_get()
        if isinstance(widget, tk.Text):
            widget.tag_add("sel", "1.0", "end")
        elif isinstance(widget, tk.Entry):
            widget.select_range(0, "end")

    def build_context_menu(self):
        """Metin kutuları için sağ tık (bağlam) menüsünü oluşturur ve sisteme bağlar."""
        self.context_menu = tk.Menu(self.root, tearoff=0, font=self.font_main, bg=self.bg_color, fg=self.fg_color, activebackground=self.accent_color, activeforeground=self.shadow_light)
        self.context_menu.add_command(label="Kes", command=lambda: self._trigger_os_event("<<Cut>>"))
        self.context_menu.add_command(label="Kopyala", command=lambda: self._trigger_os_event("<<Copy>>"))
        self.context_menu.add_command(label="Yapıştır", command=lambda: self._trigger_os_event("<<Paste>>"))
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Tümünü Seç", command=self._select_all)
        
        # Tüm Entry ve Text widget'larına sağ tık menüsünü otomatik bağla
        self.root.bind_class("Text", "<Button-3>", self.show_context_menu)
        self.root.bind_class("Entry", "<Button-3>", self.show_context_menu)

    def _check_and_restore_placeholder(self, widget):
        """Menü kapandıktan sonra kutu boş kalmışsa yer tutucuyu geri getirir."""
        if isinstance(widget, tk.Text):
            if not widget.get("1.0", "end-1c").strip():
                self.add_placeholder()
        elif isinstance(widget, tk.Entry):
            if not widget.get().strip():
                widget.event_generate("<FocusOut>")

    def show_context_menu(self, event):
        widget = event.widget
        widget.focus_set()
        self.last_active_widget = widget
        
        # Yer tutucuları sağ tıklandığı an güvenle temizle
        if isinstance(widget, tk.Text) and widget.get("1.0", "end-1c") == self.placeholder_text:
            widget.delete("1.0", tk.END)
            widget.config(fg=self.fg_color)
        elif isinstance(widget, tk.Entry) and widget.get() == "GG.AA.YYYY":
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

    def toggle_always_on_top(self):
        self.root.wm_attributes("-topmost", self.always_on_top_var.get())

    def build_ui(self):
        # Combobox'ın açılan listesindeki mavi işletim sistemi seçim rengini kiremit rengine ezme
        self.root.option_add('*TCombobox*Listbox.selectBackground', self.accent_color)
        self.root.option_add('*TCombobox*Listbox.selectForeground', self.shadow_light)
        
        style = ttk.Style()
        style.theme_use('classic') 
        
        style.map("TCombobox", 
                  selectbackground=[("readonly", self.accent_color), ("focus", self.accent_color)],
                  selectforeground=[("readonly", self.shadow_light), ("focus", self.shadow_light)])
        
        style.configure("TNotebook", background=self.bg_color, borderwidth=2, 
                        lightcolor=self.shadow_light, darkcolor=self.shadow_dark)
        
        style.configure("TNotebook.Tab", 
                        background=self.bg_secondary, foreground=self.fg_color, font=self.font_main, 
                        padding=[15, 5], borderwidth=2,
                        lightcolor=self.shadow_light, darkcolor=self.shadow_dark,
                        focuscolor="", focusthickness=0)
        
        style.map("TNotebook.Tab", 
                  background=[("selected", self.bg_color)], 
                  foreground=[("selected", self.accent_color)],
                  expand=[("selected", [1, 1, 1, 0])]) 

        self.top_frame = tk.Frame(self.root, bg=self.bg_color, padx=30, pady=20)
        self.top_frame.pack(fill="x")

        tk.Label(self.top_frame, text="ORTALAMA HESAPLAMA", font=self.font_bold, fg=self.fg_color, bg=self.bg_color).pack(anchor="w")
        tk.Label(self.top_frame, text="Hesaplanacak sayıları girin:", font=self.font_main, fg=self.text_secondary, bg=self.bg_color).pack(anchor="w", pady=(2, 8))
        
        input_frame = tk.Frame(self.top_frame, bg=self.bg_color)
        input_frame.pack(fill="x")

        text_wrapper = tk.Frame(input_frame, bg=self.bg_color)
        text_wrapper.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.char_count_lbl = tk.Label(text_wrapper, text="0 / 5.000", font=(self.font_main[0], 8), fg=self.text_disabled, bg=self.bg_color)
        self.char_count_lbl.pack(side="bottom", anchor="e")

        scrollbar = tk.Scrollbar(text_wrapper)
        scrollbar.pack(side="right", fill="y")
        
        self.text_input = tk.Text(text_wrapper, height=4, width=10, font=self.font_main, bg=self.shadow_light, fg=self.text_placeholder, bd=2, relief="sunken", wrap="word", yscrollcommand=scrollbar.set, selectbackground=self.accent_light, selectforeground=self.shadow_light)
        self.text_input.insert("1.0", self.placeholder_text)
        self.text_input.pack(side="left", fill="both", expand=True)
        self.text_input.tag_configure("detected_number", font=self.font_bold, foreground=self.accent_color)
        scrollbar.config(command=self.text_input.yview)
        self.text_input.focus()
        
        self.text_input.bind('<KeyPress>', self.clear_placeholder)
        self.text_input.bind('<Button-1>', self.clear_placeholder)
        self.text_input.bind('<FocusIn>', self.clear_placeholder)
        self.text_input.bind('<FocusOut>', self.add_placeholder)
        self.text_input.bind('<KeyRelease>', self.update_char_count)

        btn_frame = tk.Frame(input_frame, bg=self.bg_color)
        btn_frame.pack(side="right", fill="y")

        calc_btn = tk.Button(btn_frame, text="HESAPLA", font=self.font_bold, bg=self.accent_color, fg=self.shadow_light, 
                             bd=2, relief="raised", activebackground=self.accent_hover, activeforeground=self.shadow_light, cursor="hand2", command=self.process_input)
        calc_btn.pack(side="top", fill="x", ipadx=10, ipady=4, pady=(0, 4))
        
        clear_btn = tk.Button(btn_frame, text="Temizle", font=(self.font_main[0], 8), bg=self.bg_secondary, fg=self.text_secondary, 
                              bd=1, relief="raised", activebackground=self.border_color, cursor="hand2", command=self.clear_all)
        clear_btn.pack(side="top", fill="x", ipadx=10, ipady=2)

        # --- INSTANTIATE TABS (COMPONENT ARCHITECTURE) ---
        self.tabs = ttk.Notebook(self.root)
        
        self.tab_dashboard = DashboardTab(self.tabs, self)
        self.tab_history = HistoryTab(self.tabs, self)
        self.tab_tools = ToolsTab(self.tabs, self)
        
        self.tabs.add(self.tab_dashboard, text="Hesaplanan")
        self.tabs.add(self.tab_history, text="Geçmiş")
        self.tabs.add(self.tab_tools, text="Araçlar")
        self.tabs.pack(expand=True, fill="both")

        self.root.bind('<Return>', self.process_input)
        self.text_input.bind('<Return>', self.process_input)
        self.tabs.bind('<<NotebookTabChanged>>', self.handle_tab_change)

    def clear_placeholder(self, event=None):
        if self.text_input.get("1.0", "end-1c") == self.placeholder_text:
            self.text_input.delete("1.0", tk.END)
            self.text_input.config(fg=self.fg_color)
        self.root.after(10, self.update_char_count)

    def add_placeholder(self, event=None):
        if getattr(self, 'context_menu_open', False):
            return
        if not self.text_input.get("1.0", tk.END).strip():
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert("1.0", self.placeholder_text)
            self.text_input.config(fg=self.text_placeholder)
        self.update_char_count()

    def update_char_count(self, event=None):
        text = self.text_input.get("1.0", "end-1c")
        count = 0 if text == self.placeholder_text else len(text)
        
        color = self.error_color if count > 5000 else self.text_disabled
        formatted_count = f"{count:,}".replace(",", ".")
        self.char_count_lbl.config(text=f"{formatted_count} / 5.000", fg=color)

    def handle_tab_change(self, event=None):
        selected_tab = self.tabs.tab(self.tabs.select(), "text")
        if selected_tab == "Araçlar":
            self.top_frame.pack_forget()
        else:
            self.top_frame.pack(fill="x", before=self.tabs)

    def process_input(self, event=None):
        full_text = self.text_input.get("1.0", "end-1c")
        if full_text == self.placeholder_text:
            full_text = ""
            
        raw_input = full_text.strip()
        # 80/20 Optimizasyonu: Kullanıcıların %80'inin ihtiyacını karşılayacak güvenli sınır
        maks_karakter = 5000
        if len(raw_input) > maks_karakter:
            self.tab_dashboard.clear_data()
            self.tab_dashboard.info_lbl.config(text=f"Limit aşıldı! En fazla {maks_karakter:,} karakter girilebilir.", fg=self.error_color)
            return "break"

        numbers = MatematikMotoru.metinden_sayilari_ayikla(raw_input)
        analysis = MatematikMotoru.detayli_analiz_yap(numbers)

        if analysis:
            self.tab_dashboard.update_data(analysis)
            
            summary_text = f"Ort: {analysis['ortalama']} ({analysis['adet']} veri)"
            self.history.append({"girdi": raw_input, "analiz": analysis})
            
            # Bellek Yönetimi: En fazla 100 işlem geçmişi tutulur.
            if len(self.history) > 100:
                self.history.pop(0)
                if hasattr(self.tab_history, 'listbox'):
                    self.tab_history.listbox.delete(0)
                    
            self.tab_history.add_entry(summary_text)
            
            self.text_input.tag_remove("detected_number", "1.0", tk.END)
            for match in re.finditer(MatematikMotoru.SAYI_PATERNI, full_text):
                start_pos = f"1.0 + {match.start()} chars"
                end_pos = f"1.0 + {match.end()} chars"
                self.text_input.tag_add("detected_number", start_pos, end_pos)
        else:
            self.tab_dashboard.clear_data()
            self.tab_dashboard.info_lbl.config(text="Geçersiz giriş!", fg=self.error_color)
            
        return "break"

    def load_from_history(self, event=None):
        selected = self.tab_history.listbox.curselection()
        if not selected: return
        
        index = selected[0]
        record = self.history[index]
        analysis = record["analiz"]

        self.text_input.delete("1.0", tk.END)
        self.text_input.config(fg=self.fg_color)
        self.text_input.insert("1.0", record["girdi"])
        
        self.text_input.tag_remove("detected_number", "1.0", tk.END)
        for match in re.finditer(MatematikMotoru.SAYI_PATERNI, record["girdi"]):
            start_pos = f"1.0 + {match.start()} chars"
            end_pos = f"1.0 + {match.end()} chars"
            self.text_input.tag_add("detected_number", start_pos, end_pos)

        self.tab_dashboard.update_data(analysis)
        self.tab_dashboard.info_lbl.config(text=f"Geçmişten yüklendi • Kopyalamak için sonuca tıklayın", fg=self.accent_color)
        self.tabs.select(self.tab_dashboard) 
        self.update_char_count()

    def clear_all(self):
        self.text_input.delete("1.0", tk.END)
        self.add_placeholder()
        self.history.clear()
        self.tab_dashboard.clear_data()
        self.tab_tools.clear_data()
        self.tab_history.clear_data()

    def _create_centered_modal(self, title, width, height):
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

    def show_about(self):
        about_win = self._create_centered_modal("Hakkında: Ortalama Hesaplama", 350, 220)

        tk.Label(about_win, text="ORTALAMA HESAPLAMA", font=self.font_bold, fg=self.fg_color, bg=self.bg_color).pack(pady=(25, 5))
        tk.Label(about_win, text="Sürüm 1.0.0 (Build 2026)", font=self.font_main, fg=self.fg_color, bg=self.bg_color).pack()
        
        copyright_text = "Telif Hakkı © 2026 | MIT Lisansı ile açık kaynaktır."
        tk.Label(about_win, text=copyright_text, font=(self.font_main[0], 8), fg=self.text_secondary, bg=self.bg_color).pack(pady=(20, 15))

        close_btn = tk.Button(about_win, text="TAMAM", font=self.font_bold, bg=self.accent_color, fg=self.shadow_light, 
                              bd=2, relief="raised", activebackground=self.accent_hover, activeforeground=self.shadow_light, cursor="hand2", command=about_win.destroy)
        close_btn.pack(pady=(0, 20), ipadx=15, ipady=3)
        
        about_win.deiconify()

    def show_guide(self):
        guide_win = self._create_centered_modal("Kullanma Rehberi", 460, 440)

        guide_title = "KULLANMA REHBERİ:"
        tk.Label(guide_win, text=guide_title, font=self.font_bold, fg=self.fg_color, bg=self.bg_color).pack(anchor="w", padx=30, pady=(25, 5))

        guide_note = (
            "• ANA EKRAN\n"
            "  - Veri Girişi (Maks: 5.000 Karakter):\n"
            "    Sayıları yazın veya liste yapıştırın. Program,\n"
            "    içindeki sayıları format fark etmeksizin\n"
            "    (1.500,50 veya 1,500.50) otomatik ayıklar.\n"
            "  - Hesaplama ve Kopyalama:\n"
            "    İşlem için [Enter] tuşuna veya \"HESAPLA\"\n"
            "    butonuna basın. Çıkan sonuçlara tıklayarak\n"
            "    panoya kopyalayabilirsiniz.\n\n"
            "• ARAÇLAR SEKMESİ & MENÜSÜ\n"
            "  - Hızlı Erişim: Üst menüdeki \"Araçlar\"\n"
            "    sekmesinden istediğiniz araca (KDV, Yaş,\n"
            "    Orantı vb.) anında geçiş yapabilirsiniz.\n\n"
            "• GENEL KULLANIM & KISAYOLLAR\n"
            "  - Düzenleme: Metin kutuları standart sağ tık\n"
            "    menüsünü (Kes, Kopyala, Yapıştır) destekler.\n"
            "  - Her Zaman Üstte: \"Görünüş\" menüsünden bu\n"
            "    özelliği açarak pencereyi sabitleyebilirsiniz."
        )
        tk.Label(guide_win, text=guide_note, font=self.font_main, fg=self.text_secondary, bg=self.bg_color, justify="left").pack(anchor="w", padx=30, pady=5)
        
        close_btn = tk.Button(guide_win, text="TAMAM", font=self.font_bold, bg=self.accent_color, fg=self.shadow_light, 
                              bd=2, relief="raised", activebackground=self.accent_hover, activeforeground=self.shadow_light, cursor="hand2", command=guide_win.destroy)
        close_btn.pack(pady=(15, 20), ipadx=15, ipady=3)
        
        guide_win.deiconify()