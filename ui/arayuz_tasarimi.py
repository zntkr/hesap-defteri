import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import os
import sys
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
        
        self.build_menu()
        self.build_ui()

    def build_menu(self):
        menubar = tk.Menu(self.root, font=self.font_main, bg=self.bg_color, fg=self.fg_color)
        
        file_menu = tk.Menu(menubar, tearoff=0, font=self.font_main, bg=self.bg_color, fg=self.fg_color)
        file_menu.add_command(label="Temizle", command=self.clear_all)
        file_menu.add_separator()
        file_menu.add_command(label="Çıkış", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0, font=self.font_main, bg=self.bg_color, fg=self.fg_color)
        help_menu.add_command(label="Kullanma Rehberi", command=self.show_guide)
        help_menu.add_separator()
        help_menu.add_command(label="Hakkında", command=self.show_about)
        
        menubar.add_cascade(label="Dosya", menu=file_menu)
        menubar.add_cascade(label="Yardım", menu=help_menu)
        self.root.config(menu=menubar)

    def build_ui(self):
        style = ttk.Style()
        style.theme_use('classic') 
        
        style.configure("TNotebook", background=self.bg_color, borderwidth=2, 
                        lightcolor=self.shadow_light, darkcolor=self.shadow_dark)
        
        style.configure("TNotebook.Tab", 
                        background="#EFEBE6", foreground=self.fg_color, font=self.font_main, 
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
        tk.Label(self.top_frame, text="Hesaplanacak sayıları girin:", font=self.font_main, fg="#888888", bg=self.bg_color).pack(anchor="w", pady=(2, 8))
        
        input_frame = tk.Frame(self.top_frame, bg=self.bg_color)
        input_frame.pack(fill="x")

        text_wrapper = tk.Frame(input_frame, bg=self.bg_color)
        text_wrapper.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.char_count_lbl = tk.Label(text_wrapper, text="0 / 5.000", font=(self.font_main[0], 8), fg="#B0B0B0", bg=self.bg_color)
        self.char_count_lbl.pack(side="bottom", anchor="e")

        scrollbar = tk.Scrollbar(text_wrapper)
        scrollbar.pack(side="right", fill="y")
        
        self.text_input = tk.Text(text_wrapper, height=4, width=10, font=self.font_main, bg="#FFFFFF", fg="#888888", bd=2, relief="sunken", wrap="word", yscrollcommand=scrollbar.set, selectbackground=self.accent_light, selectforeground="#FFFFFF")
        self.text_input.insert("1.0", self.placeholder_text)
        self.text_input.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.text_input.yview)
        self.text_input.focus()
        
        self.text_input.bind('<KeyPress>', self.clear_placeholder)
        self.text_input.bind('<Button-1>', self.clear_placeholder)
        self.text_input.bind('<FocusOut>', self.add_placeholder)
        self.text_input.bind('<KeyRelease>', self.update_char_count)

        btn_frame = tk.Frame(input_frame, bg=self.bg_color)
        btn_frame.pack(side="right", fill="y")

        calc_btn = tk.Button(btn_frame, text="HESAPLA", font=self.font_bold, bg=self.accent_color, fg="#FFFFFF", 
                             bd=2, relief="raised", activebackground=self.accent_hover, activeforeground="#FFFFFF", cursor="hand2", command=self.process_input)
        calc_btn.pack(side="top", fill="x", ipadx=10, ipady=4, pady=(0, 4))
        
        clear_btn = tk.Button(btn_frame, text="Temizle", font=(self.font_main[0], 8), bg="#EFEBE6", fg="#888888", 
                              bd=1, relief="raised", activebackground="#E0DCE3", cursor="hand2", command=self.clear_all)
        clear_btn.pack(side="top", fill="x", ipadx=10, ipady=2)

        # --- INSTANTIATE TABS (COMPONENT ARCHITECTURE) ---
        self.tabs = ttk.Notebook(self.root)
        
        self.tab_dashboard = DashboardTab(self.tabs, self)
        self.tab_history = HistoryTab(self.tabs, self)
        self.tab_tools = ToolsTab(self.tabs, self)
        
        self.tabs.add(self.tab_dashboard, text="Sonuçlar")
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
        if not self.text_input.get("1.0", tk.END).strip():
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert("1.0", self.placeholder_text)
            self.text_input.config(fg="#888888")
        self.update_char_count()

    def update_char_count(self, event=None):
        text = self.text_input.get("1.0", "end-1c")
        count = 0 if text == self.placeholder_text else len(text)
        
        color = "#D32F2F" if count > 5000 else "#B0B0B0"
        formatted_count = f"{count:,}".replace(",", ".")
        self.char_count_lbl.config(text=f"{formatted_count} / 5.000", fg=color)

    def handle_tab_change(self, event=None):
        selected_tab = self.tabs.tab(self.tabs.select(), "text")
        if selected_tab == "Araçlar":
            self.top_frame.pack_forget()
        else:
            self.top_frame.pack(fill="x", before=self.tabs)

    def process_input(self, event=None):
        raw_input = self.text_input.get("1.0", tk.END).strip()
        if raw_input == self.placeholder_text:
            raw_input = ""
            
        # 80/20 Optimizasyonu: Kullanıcıların %80'inin ihtiyacını karşılayacak güvenli sınır
        maks_karakter = 5000
        if len(raw_input) > maks_karakter:
            self.tab_dashboard.clear_data()
            self.tab_dashboard.info_lbl.config(text=f"Limit aşıldı! En fazla {maks_karakter:,} karakter girilebilir.", fg="#D32F2F")
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
            
            self.text_input.tag_add("sel", "1.0", tk.END)
        else:
            self.tab_dashboard.clear_data()
            self.tab_dashboard.info_lbl.config(text="Geçersiz giriş!", fg="#D32F2F")
            
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
        tk.Label(about_win, text=copyright_text, font=(self.font_main[0], 8), fg="#888888", bg=self.bg_color).pack(pady=(20, 15))

        close_btn = tk.Button(about_win, text="TAMAM", font=self.font_bold, bg=self.accent_color, fg="#FFFFFF", 
                              bd=2, relief="raised", activebackground=self.accent_hover, activeforeground="#FFFFFF", cursor="hand2", command=about_win.destroy)
        close_btn.pack(pady=(0, 20), ipadx=15, ipady=3)
        
        about_win.deiconify()

    def show_guide(self):
        guide_win = self._create_centered_modal("Kullanma Rehberi", 460, 320)

        guide_title = "KULLANMA REHBERİ:"
        tk.Label(guide_win, text=guide_title, font=self.font_bold, fg=self.fg_color, bg=self.bg_color).pack(anchor="w", padx=30, pady=(25, 5))

        guide_note = (
            "• Veri Girişi (Maks: 5.000 Karakter):\n"
            "  Sayıları, listeleri veya hesap dökümlerini doğrudan\n"
            "  yapıştırın. Nokta ve virgül ayrımı otomatiktir.\n\n"
            "• Geçmiş ve Kopyalama:\n"
            "  Eski bir işleme çift tıklayarak ana ekrana yükleyin.\n"
            "  Sonuçlara tıklayarak değerleri panoya kopyalayabilirsiniz.\n\n"
            "• Kısayollar:\n"
            "  Hesaplamak için klavyeden [Enter] tuşunu kullanın."
        )
        tk.Label(guide_win, text=guide_note, font=self.font_main, fg="#888888", bg=self.bg_color, justify="left").pack(anchor="w", padx=30, pady=5)
        
        close_btn = tk.Button(guide_win, text="TAMAM", font=self.font_bold, bg=self.accent_color, fg="#FFFFFF", 
                              bd=2, relief="raised", activebackground=self.accent_hover, activeforeground="#FFFFFF", cursor="hand2", command=guide_win.destroy)
        close_btn.pack(pady=(15, 20), ipadx=15, ipady=3)
        
        guide_win.deiconify()