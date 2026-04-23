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
        super().__init__(parent, bg=ui.bg_color, padx=30, pady=20)
        self.ui = ui
        self.build_ui()

    def build_ui(self) -> None:
        header_frame = tk.Frame(self, bg=self.ui.bg_color)
        header_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(header_frame, text="İŞLEM TİPİ SEÇİN:", font=self.ui.font_bold, fg=self.ui.fg_color, bg=self.ui.bg_color).pack(side="left")
        
        self.tool_var = tk.StringVar()
        self.tool_selector = ttk.Combobox(header_frame, textvariable=self.tool_var, state="readonly", font=self.ui.font_main, width=22)
        self.tool_selector.pack(side="right", fill="x", expand=True, padx=(15, 0))
        self.tool_selector.bind("<<ComboboxSelected>>", self.on_tool_change)
        
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=(0, 15))

        self.container = tk.Frame(self, bg=self.ui.bg_color)
        self.container.pack(fill="both", expand=True)
        
        # --- PLUGIN REGISTRY (Bileşen Kaydı) ---
        tools_list = [
            ChangeToolWidget(self.container, self.ui, self),
            AverageToolWidget(self.container, self.ui, self),
            TaxToolWidget(self.container, self.ui, self),
            DiscountToolWidget(self.container, self.ui, self),
            ProportionToolWidget(self.container, self.ui, self),
            AgeToolWidget(self.container, self.ui, self)
        ]
        
        self.frames = {tool.get_name(): tool for tool in tools_list}
        self.tool_selector['values'] = tuple(self.frames.keys())
        
        total_tools = len(tools_list)
        for i, tool in enumerate(tools_list, start=1):
            if hasattr(tool, 'set_page_badge'):
                tool.set_page_badge(i, total_tools)
        
        # Başlangıç Aracı dinamik olarak (kayıtlı ilk araç) belirlenir
        default_tool = list(self.frames.keys())[0]
        self.tool_var.set(default_tool)
        self.current_frame = self.frames[default_tool]
        self.current_frame.pack(fill="both", expand=True)
        self.ui.root.after(100, self._focus_active_tool)

    def _focus_active_tool(self) -> None:
        tool = self.frames.get(self.tool_var.get())
        if tool and tool.primary_input:
            tool.primary_input.focus_set()

    def cycle_tools(self, event: Optional[tk.Event] = None) -> Optional[str]:
        tools = self.tool_selector['values']
        current_tool = self.tool_var.get()
        current_idx = tools.index(current_tool) if current_tool in tools else -1
        next_idx = (current_idx + 1) % len(tools)
        self.tool_var.set(tools[next_idx])
        self.on_tool_change()
        return "break"

    def on_tool_change(self, event: Optional[tk.Event] = None) -> None:
        self.current_frame.pack_forget()
        self.current_frame = self.frames[self.tool_var.get()]
        self.current_frame.pack(fill="both", expand=True)
        if hasattr(self.ui, 'active_tool_var'):
            self.ui.active_tool_var.set(self.tool_var.get())
        self._focus_active_tool()

    def clear_data(self) -> None:
        active_tool = self.frames.get(self.tool_var.get())
        if active_tool:
            active_tool.clear_data()
        self._focus_active_tool()