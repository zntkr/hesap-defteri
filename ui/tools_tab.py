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


class PaperShadowCanvas(tk.Canvas):
    """
    Skeuomorfik 45 derece ışık açısını simüle etmek için özel çizim.
    Frame tabanlı sert (hard-edge) gölgelerin köşelerde yarattığı 
    üst üste binmeyi (overlapping) ve 90 derecelik kesintileri önlemek 
    amacıyla tek bir tam boyutlu polygon olarak inşa edilmiştir.
    """
    def __init__(self, parent: tk.Misc, ui: "MainUI", offset: int, top_diagonal: bool = True, **kwargs) -> None:
        super().__init__(parent, bg=ui.bg_color, highlightthickness=0, bd=0, **kwargs)
        self.ui = ui
        self.offset = offset
        self.top_diagonal = top_diagonal
        self._shadow_poly = self.create_polygon(0, 0, 0, 0, fill=self.ui.bg_shadow, outline="")
        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, event: tk.Event) -> None:
        w, h = event.width, event.height
        o = self.offset
        if w <= o or h <= o:
            return
        
        if self.top_diagonal:
            # Hesap şeridi (Tape) gibi bağımsız nesneler için tam silüet (Yüzen kağıt / Neo-Brutalizm)
            # 45 derecelik bağlar kaldırılarak nesnenin masadan koptuğu illüzyonu yaratıldı.
            pts = [
                o, o,
                w, o,
                w, h,
                o, h
            ]
        else:
            # Ana defter için (Üstünde sekme gölgesiyle birleşeceği için üst kısım y=0'dan başlar)
            pts = [
                o, 0,
                w, 0,
                w, h,
                o, h,
            ]
        self.coords(self._shadow_poly, *pts)


class TabShadowCanvas(tk.Canvas):
    """
    Sekme çubuğunun sağ kenarındaki silüet gölgesini (45 derece ışıkla) çizer.
    Altındaki PaperShadowCanvas ile kusursuz birleşir.
    """
    def __init__(self, parent: tk.Misc, ui: "MainUI", offset: int, **kwargs) -> None:
        super().__init__(parent, bg=ui.bg_color, highlightthickness=0, bd=0, **kwargs)
        self.ui = ui
        self.offset = offset
        self._shadow_poly = self.create_polygon(0, 0, 0, 0, fill=self.ui.bg_shadow, outline="")
        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, event: tk.Event) -> None:
        w, h = event.width, event.height
        o = self.offset
        c = self.ui.s(4)  # Sekmelerdeki kırpık köşe yarıçapı
        if w <= 0 or h <= 0:
            return
        
        # Işık sol üstten (top-left) vuruyor. Sekme üstten (y=0) başlıyor, 
        # silüeti ise aşağıya (y=o) kadar kayarak masaya düşüyor.
        pts = [
            0, o,             # Gölge sekmenin arkasından y=o noktasında belirir
            o - c, o,         # Sekmenin düz üst kenarının gölgesi biter
            o, o + c,         # Kırpık köşenin (clip) 45 derecelik gölgesi
            o, h,             # Kağıt gölgesiyle birleşmek üzere dümdüz aşağı iner
            0, h              # Sola dönerek sekmenin arkasına girer
        ]
        self.coords(self._shadow_poly, *pts)


class ToolsTab(tk.Frame):
    """Tüm bağımsız araç bileşenlerini yöneten Orkestratör Sınıf."""

    def __init__(self, parent: tk.Misc, ui: "MainUI") -> None:
        super().__init__(parent, bg=ui.bg_color)
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
        self.tab_bar.pack(fill="x", padx=(self.ui.s(16), self.ui.s(24)), pady=(self.ui.s(16), 0))
        self.content_host.pack(fill="both", expand=True, padx=(self.ui.s(16), self.ui.s(16)), pady=(0, self.ui.s(16)))

        # Sekme çubuğu hizasında sağ gölge şeridi — sekmenin 45 derecelik silüet gölgesi
        tab_shadow = TabShadowCanvas(self, self.ui, offset=self.ui.s(8))
        tab_shadow.place(relx=1.0, x=-self.ui.s(24), y=self.ui.s(16),
                         width=self.ui.s(8), height=self.ui.s(21))

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
        offset = self.ui.s(8)

        # 1. Katman: Kusursuz gölge çizimi (Tüm alanı kaplar, üst sekme gölgesiyle birleşir)
        shadow_canvas = PaperShadowCanvas(paper_wrapper, self.ui, offset=offset, top_diagonal=False)
        shadow_canvas.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)

        # 2. Katman: Fiziksel defter sayfası 
        # (pack padding'i sağdan ve alttan boşluk bırakarak Canvas gölgesini açıkta bırakır)
        paper = tk.Frame(paper_wrapper, bg=self.ui.bg_secondary, bd=0)
        paper.pack(side="top", fill="both", expand=True, padx=(0, offset), pady=(0, offset))

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

        # Easter Egg: Sol alt köşedeki gizli buton (Hesap Şeridini tetikler)
        easter_egg = tk.Frame(left_margin, bg=self.ui.bg_secondary, height=self.ui.s(40), cursor="hand2")
        easter_egg.pack(side="bottom", fill="x")
        easter_egg.bind("<Button-1>", lambda e: self.ui.toggle_tape(e))

        tk.Frame(content_frame, bg=self.ui.accent_color, width=3).pack(side="left", fill="y")

        container = tk.Frame(content_frame, bg=self.ui.bg_secondary)
        container.pack(side="left", fill="both", expand=True, padx=(self.ui.s(8), 0))

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

    def clear_data(self, from_keyboard: bool = False) -> None:
        tool = self.frames.get(self.tool_var.get())
        if tool:
            tool.clear_data(from_keyboard=from_keyboard)
        self._focus_active()
