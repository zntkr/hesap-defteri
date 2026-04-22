import tkinter as tk

class HistoryTab(tk.Frame):
    """Component class for the History (Geçmiş) tab."""
    def __init__(self, parent, ui):
        super().__init__(parent, bg=ui.bg_color, padx=20, pady=15)
        self.ui = ui
        self.build_ui()

    def build_ui(self):
        self.info_lbl = tk.Label(self, text="Tekrar yüklemek için bir işleme çift tıklayın", font=self.ui.font_main, fg="#888888", bg=self.ui.bg_color)
        self.info_lbl.pack(side="bottom", pady=(10, 0))

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side="right", fill="y")
        self.listbox = tk.Listbox(self, yscrollcommand=scrollbar.set, font=self.ui.font_main, fg=self.ui.fg_color, bg="#FFFFFF", 
                                  bd=2, relief="sunken", selectbackground=self.ui.accent_color, selectforeground="#FFFFFF")
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)
        self.listbox.bind('<Double-Button-1>', self.ui.load_from_history)

    def add_entry(self, text):
        self.listbox.insert(tk.END, text)
        self.listbox.yview(tk.END)

    def clear_data(self):
        self.listbox.delete(0, tk.END)