import tkinter as tk
import sys
import os
from typing import Optional, List, Dict, TYPE_CHECKING

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui.animated_tab_bar import AnimatedTabBar
from ui.change_tool import ChangeToolWidget
from ui.average_tool import AverageToolWidget
from ui.tax_tool import TaxToolWidget
from ui.discount_tool import DiscountToolWidget
from ui.proportion_tool import ProportionToolWidget
from ui.age_tool import AgeToolWidget

if TYPE_CHECKING:
    from ui.arayuz_tasarimi import MainUI
    from ui.base_tool import BaseToolWidget


class ToolsTab(tk.Frame):
    """Tüm bağımsız araç bileşenlerini yöneten Orkestratör Sınıf."""

    def __init__(self, parent: tk.Misc, ui: "MainUI") -> None:
        super().__init__(parent, bg=ui.bg_color, padx=16, pady=16)
        self.ui = ui
        self._active_idx: int = 0
        self.frames: Dict[str, "BaseToolWidget"] = {}
        self.tabs_list: List[str] = []
        self._paper_wrappers: List[tk.Frame] = []
        self.tool_var = tk.StringVar()
        self.build_ui()

    def build_ui(self) -> None:
        tool_classes = [
            ChangeToolWidget, AverageToolWidget, TaxToolWidget,
            DiscountToolWidget, ProportionToolWidget, AgeToolWidget,
        ]
        total = len(tool_classes)

        # İçerik çerçevesi: sekme çubuğundan önce oluştur, sonra paketle
        self.content_host = tk.Frame(self, bg=self.ui.bg_color)
        self.content_host.grid_rowconfigure(0, weight=1)
        self.content_host.grid_columnconfigure(0, weight=1)

        for i, cls in enumerate(tool_classes, start=1):
            paper = self._build_paper(self.content_host, i, total, cls)
            self._paper_wrappers.append(paper)
            paper.grid(row=0, column=0, sticky="nsew")

        short_labels = [self.frames[name].get_short_name() for name in self.tabs_list]

        self.tab_bar = AnimatedTabBar(self, self.ui, short_labels, self._on_tab_change)
        self.tab_bar.pack(fill="x", padx=(0, 8))
        self.content_host.pack(fill="both", expand=True)

        self._show(0)
        self.tool_var.set(self.tabs_list[0])

        self.ui.root.bind("<Escape>", self.ui.clear_all)
        self.ui.root.bind("<Control-Tab>", lambda e: self.cycle_tools(e))
        self._focus_job: Optional[str] = self.ui.root.after(100, self._focus_active)

    def destroy(self) -> None:
        if hasattr(self, "_focus_job") and self._focus_job:
            self.ui.root.after_cancel(self._focus_job)
            self._focus_job = None
        super().destroy()

    def _build_paper(self, host: tk.Frame, i: int, total: int, cls: type) -> tk.Frame:
        """Defter sayfası görünümündeki sarmalayıcı çerçeveyi ve araç widget'ını oluşturur."""
        paper_wrapper = tk.Frame(host, bg=self.ui.bg_color, bd=0)

        # 45° gölge efekti: alt ve sağ kenar
        tk.Frame(paper_wrapper, bg=self.ui.bg_shadow, height=8).pack(
            side="bottom", fill="x", padx=(8, 0)
        )
        middle = tk.Frame(paper_wrapper, bg=self.ui.bg_color, bd=0)
        middle.pack(side="top", fill="both", expand=True)
        tk.Frame(middle, bg=self.ui.bg_shadow, width=8).pack(
            side="right", fill="y", pady=(8, 0)
        )

        paper = tk.Frame(middle, bg=self.ui.bg_secondary, bd=0)
        paper.pack(side="left", fill="both", expand=True)

        # Fiziksel kağıt kenarları (3D highlight/shadow)
        tk.Frame(paper, bg=self.ui.shadow_dark, height=2).pack(side="bottom", fill="x")
        tk.Frame(paper, bg=self.ui.shadow_light, width=2).pack(side="left", fill="y")
        tk.Frame(paper, bg=self.ui.shadow_dark, width=2).pack(side="right", fill="y")

        content_frame = tk.Frame(paper, bg=self.ui.bg_secondary)
        content_frame.pack(fill="both", expand=True)

        # Sol kenar boşluğu — kırmızı çizgi skeuomorfizmi
        left_margin = tk.Frame(content_frame, bg=self.ui.bg_secondary, width=self.ui.s(40))
        left_margin.pack(side="left", fill="y")
        left_margin.pack_propagate(False)

        tk.Frame(content_frame, bg=self.ui.accent_color, width=3).pack(side="left", fill="y")

        container = tk.Frame(content_frame, bg=self.ui.bg_secondary)
        container.pack(side="left", fill="both", expand=True, padx=(8, 0))

        tool = cls(container, self.ui, self)
        tool.pack(fill="both", expand=True)

        if hasattr(tool, "set_page_badge"):
            tool.set_page_badge(i, total)

        self.frames[tool.get_name()] = tool
        self.tabs_list.append(tool.get_name())
        return paper_wrapper

    def _show(self, idx: int) -> None:
        """Yalnızca belirtilen sekmenin içerik çerçevesini gösterir."""
        # Tüm sekmeler halihazırda grid üzerinde üst üste (stack) duruyor.
        # Sadece istenen sekmeyi Z-ekseninde en üste alıyoruz (tkraise).
        # Böylece unmap/map kaynaklı anlık siyahlık/titreme (%100) yok edilir.
        self._paper_wrappers[idx].tkraise()

    def _on_tab_change(self, idx: int) -> None:
        self._show(idx)
        self._active_idx = idx
        name = self.tabs_list[idx]
        self.tool_var.set(name)
        if hasattr(self.ui, "active_tool_var"):
            self.ui.active_tool_var.set(name)
        self._focus_active()

    def _focus_active(self) -> None:
        tool = self.frames.get(self.tool_var.get())
        if tool and tool.primary_input:
            tool.primary_input.focus_set()

    # --- Public API ---

    def cycle_tools(self, event: Optional[tk.Event] = None) -> Optional[str]:
        next_idx = (self._active_idx + 1) % len(self.tabs_list)
        self.tab_bar.select(next_idx)
        return "break"

    def select_tab(self, tool_name: str) -> None:
        if tool_name in self.tabs_list:
            self.tab_bar.select(self.tabs_list.index(tool_name))

    def on_tool_change(self) -> None:
        """Klavye kısayolları ve ana menü radyolarından tetiklendiğinde senkronize eder."""
        self.select_tab(self.tool_var.get())

    def clear_data(self) -> None:
        tool = self.frames.get(self.tool_var.get())
        if tool:
            tool.clear_data()
        self._focus_active()
