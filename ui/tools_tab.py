import tkinter as tk
from tkinter import ttk
import sys
import os

# Proje kök dizinini Python yoluna ekle (Pylance import hatalarını önlemek için)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Optional, TYPE_CHECKING
from ui.change_tool import ChangeToolWidget
from ui.average_tool import AverageToolWidget
from ui.tax_tool import TaxToolWidget
from ui.discount_tool import DiscountToolWidget
from ui.proportion_tool import ProportionToolWidget
from ui.age_tool import AgeToolWidget

if TYPE_CHECKING:
    from ui.arayuz_tasarimi import MainUI

class ToolsTab(tk.Frame):
    """Tüm bağımsız araç bileşenlerini yöneten Orkestratör Sınıf."""
    def __init__(self, parent: tk.Misc, ui: 'MainUI') -> None:
        super().__init__(parent, bg=ui.bg_color, padx=15, pady=15)
        self.ui = ui
        self.build_ui()

    def build_ui(self) -> None:
        self.tool_var = tk.StringVar()
        
        style = ttk.Style()
        style.configure("TNotebook", background=self.ui.bg_color)
        style.configure("TNotebook.Tab", font=(self.ui.font_main[0], 9), padding=[8, 2], background=self.ui.shadow_dark, foreground=self.ui.text_secondary, width=11, anchor="center")
        style.map("TNotebook.Tab", background=[("selected", self.ui.bg_secondary)], foreground=[("selected", self.ui.accent_color)])
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=(5, 5), pady=(0, 5))
        self.notebook.bind("<<NotebookTabChanged>>", self.on_notebook_tab_changed)
        
        self.frames = {}
        self.tabs_list = []
        
        tool_classes = [
            ChangeToolWidget, AverageToolWidget, TaxToolWidget, 
            DiscountToolWidget, ProportionToolWidget, AgeToolWidget
        ]
        
        total_tools = len(tool_classes)
        for i, tool_cls in enumerate(tool_classes, start=1):
            paper_wrapper = tk.Frame(self.notebook, bg=self.ui.bg_secondary)
            
            left_margin = tk.Frame(paper_wrapper, bg=self.ui.bg_secondary, width=25)
            left_margin.pack(side="left", fill="y")
            left_margin.pack_propagate(False)
            
            red_line = tk.Frame(paper_wrapper, bg=self.ui.accent_color, width=2)
            red_line.pack(side="left", fill="y")
            
            container = tk.Frame(paper_wrapper, bg=self.ui.bg_secondary)
            container.pack(side="left", fill="both", expand=True)
            
            tool_instance = tool_cls(container, self.ui, self)
            tool_instance.pack(fill="both", expand=True)
            
            if hasattr(tool_instance, 'set_page_badge'):
                tool_instance.set_page_badge(i, total_tools)
                
            self.notebook.add(paper_wrapper, text=tool_instance.get_short_name())
            self.frames[tool_instance.get_name()] = tool_instance
            self.tabs_list.append(tool_instance.get_name())
            
        default_tool = self.tabs_list[0]
        self.tool_var.set(default_tool)
        self.ui.root.after(100, self._focus_active_tool)

    def _focus_active_tool(self) -> None:
        tool = self.frames.get(self.tool_var.get())
        if tool and tool.primary_input:
            tool.primary_input.focus_set()

    def cycle_tools(self, event: Optional[tk.Event] = None) -> Optional[str]:
        current_idx = self.notebook.index(self.notebook.select())
        next_idx = (current_idx + 1) % len(self.tabs_list)
        self.notebook.select(next_idx)
        return "break"

    def select_tab(self, tool_name: str) -> None:
        if tool_name in self.tabs_list:
            idx = self.tabs_list.index(tool_name)
            self.notebook.select(idx)

    def on_notebook_tab_changed(self, event: Optional[tk.Event] = None) -> None:
        current_idx = self.notebook.index(self.notebook.select())
        active_tool = self.tabs_list[current_idx]
        self.tool_var.set(active_tool)
        
        if hasattr(self.ui, 'active_tool_var'):
            self.ui.active_tool_var.set(active_tool)
        self._focus_active_tool()

    def on_tool_change(self, event: Optional[tk.Event] = None) -> None:
        """Klavye kısayolları ve ana menü radyolarından tetiklendiğinde senkronize eder."""
        self.select_tab(self.tool_var.get())

    def clear_data(self) -> None:
        active_tool = self.frames.get(self.tool_var.get())
        if active_tool:
            active_tool.clear_data()
        self._focus_active_tool()