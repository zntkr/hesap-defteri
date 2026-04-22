import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import os
from core.matematik_motoru import MatematikMotoru
from ui.summary_tab import SummaryTab
from ui.statistics_tab import StatisticsTab
from ui.history_tab import HistoryTab
from ui.tools_tab import ToolsTab

class MainUI:
    """
    Main Orchestrator class for the UI (Presentation Layer).
    Manages the application state, menus, and tab component instantiation.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Hesaplayıcı v1.0.0")
        self.root.geometry("440x620") 
        self.root.resizable(False, False)
        
        # --- NEO-RETRO THEME VARIABLES ---
        self.bg_color = "#F9F8F6"
        self.fg_color = "#2D2D2D"
        self.accent_color = "#C85A47"
        self.accent_hover = "#A84534"
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

        tk.Label(self.top_frame, text="HESAPLAYICI", font=self.font_bold, fg=self.fg_color, bg=self.bg_color).pack(anchor="w")
        tk.Label(self.top_frame, text="Ortalaması alınacak sayıları yapıştırın:", font=self.font_main, fg="#888888", bg=self.bg_color).pack(anchor="w", pady=(2, 8))
        
        input_frame = tk.Frame(self.top_frame, bg=self.bg_color)
        input_frame.pack(fill="x")

        self.entry = tk.Entry(input_frame, font=self.font_main, bg="#FFFFFF", fg="#888888", bd=2, relief="sunken")
        self.entry.insert(0, "yazınız")
        self.entry.pack(side="left", fill="x", expand=True, ipady=4, padx=(0, 10))
        self.entry.focus()
        
        self.entry.bind('<KeyPress>', self.clear_placeholder)
        self.entry.bind('<Button-1>', self.clear_placeholder)
        self.entry.bind('<FocusOut>', self.add_placeholder)

        calc_btn = tk.Button(input_frame, text="HESAPLA", font=self.font_bold, bg=self.accent_color, fg="#FFFFFF", 
                             bd=2, relief="raised", activebackground=self.accent_hover, activeforeground="#FFFFFF", cursor="hand2", command=self.process_input)
        calc_btn.pack(side="right", ipadx=10, ipady=2)

        # --- INSTANTIATE TABS (COMPONENT ARCHITECTURE) ---
        self.tabs = ttk.Notebook(self.root)
        
        self.tab_summary = SummaryTab(self.tabs, self)
        self.tab_statistics = StatisticsTab(self.tabs, self)
        self.tab_history = HistoryTab(self.tabs, self)
        self.tab_tools = ToolsTab(self.tabs, self)
        
        self.tabs.add(self.tab_summary, text="Özet")
        self.tabs.add(self.tab_statistics, text="İstatistik")
        self.tabs.add(self.tab_history, text="Geçmiş")
        self.tabs.add(self.tab_tools, text="Araçlar")
        self.tabs.pack(expand=True, fill="both")

        self.root.bind('<Return>', self.process_input)
        self.tabs.bind('<<NotebookTabChanged>>', self.handle_tab_change)

    def clear_placeholder(self, event=None):
        if self.entry.get() == "yazınız":
            self.entry.delete(0, tk.END)
            self.entry.config(fg=self.fg_color)

    def add_placeholder(self, event=None):
        if not self.entry.get().strip():
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "yazınız")
            self.entry.config(fg="#888888")

    def handle_tab_change(self, event=None):
        selected_tab = self.tabs.tab(self.tabs.select(), "text")
        if selected_tab == "Araçlar":
            self.top_frame.pack_forget()
        else:
            self.top_frame.pack(fill="x", before=self.tabs)

    def process_input(self, event=None):
        raw_input = self.entry.get().strip()
        if raw_input == "yazınız":
            raw_input = ""
            
        numbers = MatematikMotoru.metinden_sayilari_ayikla(raw_input)
        analysis = MatematikMotoru.detayli_analiz_yap(numbers)

        if analysis:
            self.tab_summary.update_data(analysis)
            self.tab_statistics.update_data(analysis)
            
            summary_text = f"Ort: {analysis['ortalama']} ({analysis['adet']} veri)"
            self.history.append({"girdi": raw_input, "analiz": analysis})
            self.tab_history.add_entry(summary_text)
            
            self.entry.select_range(0, tk.END)
        else:
            self.tab_summary.info_lbl.config(text="Geçersiz giriş!", fg="#D32F2F")

    def load_from_history(self, event=None):
        selected = self.tab_history.listbox.curselection()
        if not selected: return
        
        index = selected[0]
        record = self.history[index]
        analysis = record["analiz"]

        self.entry.delete(0, tk.END)
        self.entry.config(fg=self.fg_color)
        self.entry.insert(0, record["girdi"])
        
        self.tab_summary.update_data(analysis)
        self.tab_summary.info_lbl.config(text=f"Geçmişten yüklendi • Kopyalamak için sonuca tıklayın", fg=self.accent_color)
        self.tab_statistics.update_data(analysis)
        self.tabs.select(self.tab_summary) 

    def clear_all(self):
        self.entry.delete(0, tk.END)
        self.add_placeholder()
        self.tab_summary.clear_data()
        self.tab_statistics.clear_data()
        self.tab_tools.clear_data()

    def show_about(self):
        about_win = tk.Toplevel(self.root)
        about_win.withdraw()
        
        if os.path.exists("app_icon.ico"):
            about_win.iconbitmap("app_icon.ico")
            
        about_win.title("Hakkında: Hesaplayıcı")
        about_win.resizable(False, False)
        about_win.config(bg=self.bg_color)
        
        self.root.update_idletasks()
        width, height = 480, 520
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (width // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (height // 2)
        about_win.geometry(f"{width}x{height}+{x}+{y}")
        
        about_win.transient(self.root)
        about_win.grab_set()
        about_win.focus_set()

        tk.Label(about_win, text="HESAPLAYICI", font=self.font_bold, fg=self.fg_color, bg=self.bg_color).pack(pady=(20, 5))
        tk.Label(about_win, text="Sürüm 1.0.0 (Build 2026)", font=self.font_main, fg=self.fg_color, bg=self.bg_color).pack()
        
        guide_title = "SİSTEM YETENEKLERİ VE KULLANIMI:"
        tk.Label(about_win, text=guide_title, font=self.font_bold, fg=self.fg_color, bg=self.bg_color).pack(anchor="w", padx=30, pady=(15, 5))

        guide_note = (
            "• Agnostik Veri Girişi:\n"
            "  Sistem, girdi içindeki sayıları karakter ayrımı yapmadan\n"
            "  (virgül, boşluk, harf vb.) Regex ile ayıklar.\n\n"
            "• İstatistiki Kapsam:\n"
            "  Aritmetik ortalamanın yanı sıra uç değerler (min/max)\n"
            "  ve merkez değer (medyan) eş zamanlı hesaplanır.\n\n"
            "• Oturum Belleği:\n"
            "  Hesaplamalar geçmiş sekmesinde tutulur. Çift tıklama\n"
            "  ile eski veri setleri işleme geri çağrılabilir.\n\n"
            "• Operasyonel Kısayollar:\n"
            "  [Enter] hesaplamayı tetikler. Sonuca tıklanması\n"
            "  durumunda değer sistem panosuna kopyalanır."
        )
        tk.Label(about_win, text=guide_note, font=self.font_main, fg="#888888", bg=self.bg_color, justify="left").pack(anchor="w", padx=30, pady=5)
        
        copyright_text = "Telif Hakkı © 2026 | MIT Lisansı ile açık kaynaktır."
        tk.Label(about_win, text=copyright_text, font=(self.font_main[0], 8), fg="#888888", bg=self.bg_color).pack(pady=(15, 5))

        close_btn = tk.Button(about_win, text="TAMAM", font=self.font_bold, bg=self.accent_color, fg="#FFFFFF", 
                              bd=2, relief="raised", activebackground=self.accent_hover, activeforeground="#FFFFFF", cursor="hand2", command=about_win.destroy)
        close_btn.pack(pady=(0, 20), ipadx=15, ipady=3)
        
        about_win.deiconify()