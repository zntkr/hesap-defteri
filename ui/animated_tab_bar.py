import tkinter as tk
from typing import Callable, List, Optional, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ui.arayuz_tasarimi import MainUI


class AnimatedTabBar(tk.Canvas):
    """
    Windows 98 tarzı kırpık köşeli sekme çubuğu.

    Tek Canvas üzerinde tüm sekmeler çizilir. Aktif sekmenin alt kenarı yoktur —
    içerik alanıyla görsel olarak birleşir. Renk geçişleri ease-out cubic ile
    interpolasyonlanır; animasyon rapid tıklamalarda mevcut progress'ten devam eder.
    """

    _STEPS: int = 8
    _INTERVAL_MS: int = 16   # ~62 fps → toplam ~130 ms geçiş

    def __init__(
        self,
        parent: tk.Misc,
        ui: "MainUI",
        labels: List[str],
        on_change: Callable[[int], None],
    ) -> None:
        self.ui = ui
        self._H: int = self.ui.s(21)
        self._CLIP: int = self.ui.s(4)
        super().__init__(
            parent,
            height=self._H,
            bg=ui.bg_color,
            highlightthickness=0,
            bd=0,
            cursor="hand2",
        )
        self.labels = labels
        self.on_change = on_change
        self._current_idx: int = 0
        self._anim_job: Optional[str] = None
        # Sekme 0 başlangıçta aktif; after() gecikme olmadan ilk <Configure>'da doğru çizilir
        self._progress: List[float] = [1.0 if i == 0 else 0.0 for i in range(len(labels))]
        self._tab_items: List[Dict[str, Any]] = []
        self._shelf_lines: List[int] = []
        self._last_width: int = 0

        self.bind("<Configure>", lambda e: self._redraw())
        self.bind("<Button-1>", self._on_click)

    @staticmethod
    def _lerp_color(c1: str, c2: str, t: float) -> str:
        """İki hex renk arasında doğrusal interpolasyon."""
        r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
        r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
        r = min(255, max(0, round(r1 + (r2 - r1) * t)))
        g = min(255, max(0, round(g1 + (g2 - g1) * t)))
        b = min(255, max(0, round(b1 + (b2 - b1) * t)))
        return f"#{r:02x}{g:02x}{b:02x}"

    def _tab_w(self) -> float:
        return self.winfo_width() / max(len(self.labels), 1)

    def _on_click(self, event: tk.Event) -> None:
        tw = self._tab_w()
        if tw > 0:
            idx = int(event.x / tw)
            if 0 <= idx < len(self.labels):
                self.select(idx)

    def destroy(self) -> None:
        if self._anim_job:
            self.after_cancel(self._anim_job)
            self._anim_job = None
        super().destroy()

    def select(self, idx: int, animate: bool = True) -> None:
        """Sekmeyi seç; gerekirse renk geçiş animasyonu başlat."""
        if self._anim_job:
            self.after_cancel(self._anim_job)
            self._anim_job = None

        prev_idx = self._current_idx

        if animate and prev_idx != idx:
            self._step(prev_idx, idx, 0)
        else:
            self._progress = [1.0 if i == idx else 0.0 for i in range(len(self.labels))]
            self._redraw()

        if prev_idx != idx:
            self.on_change(idx)
        self._current_idx = idx

    def _step(self, from_idx: int, to_idx: int, n: int) -> None:
        t = n / self._STEPS
        ease = 1.0 - (1.0 - t) ** 3   # ease-out cubic
        self._progress[to_idx] = ease
        self._progress[from_idx] = 1.0 - ease
        self._redraw()

        if n < self._STEPS:
            self._anim_job = self.after(
                self._INTERVAL_MS,
                lambda: self._step(from_idx, to_idx, n + 1),
            )

    def _build_items(self, n: int) -> None:
        """Tuval objelerini (polygon, line, text) bir kereliğine yaratır."""
        self.delete("all")
        self._tab_items = []
        for _ in range(n):
            poly = self.create_polygon([0, 0, 0, 0, 0, 0], outline="")
            # Her sekme için 10 adet kenar/gölge/vurgu çizgisi
            lines = [self.create_line(0, 0, 0, 0) for _ in range(10)]
            text = self.create_text(0, 0, text="")
            self._tab_items.append({'poly': poly, 'lines': lines, 'text': text})
        
        # 4 adet raf çizgisi (left_sh, left_hl, right_sh, right_hl)
        self._shelf_lines = [self.create_line(0, 0, 0, 0) for _ in range(4)]

    def _redraw(self) -> None:
        n = len(self.labels)
        w = self.winfo_width()
        h = self._H
        if w <= 1 or n == 0:
            return
            
        # Sadece ekran genişliği değiştiğinde veya ilk açılışta objeleri yarat
        if w != self._last_width or len(self._tab_items) != n:
            self._build_items(n)
            self._last_width = w
            
        tab_w = w / n

        for i, label in enumerate(self.labels):
            self._update_tab(i, i * tab_w, tab_w, h, label, self._progress[i])

        # Raf çizgisi: sekme çubuğunu içerik alanından ayırır, aktif sekme altında kesilir.
        ax1 = round(self._current_idx * tab_w)
        ax2 = round((self._current_idx + 1) * tab_w)
        hl, sh = self.ui.shadow_light, self.ui.shadow_dark

        # Sol segment
        self.coords(self._shelf_lines[0], 0, h - 2, ax1, h - 2)
        self.itemconfig(self._shelf_lines[0], fill=sh if ax1 > 0 else "")
        self.coords(self._shelf_lines[1], 0, h - 1, ax1, h - 1)
        self.itemconfig(self._shelf_lines[1], fill=hl if ax1 > 0 else "")
        
        # Sağ segment
        self.coords(self._shelf_lines[2], ax2, h - 2, w, h - 2)
        self.itemconfig(self._shelf_lines[2], fill=sh if ax2 < w else "")
        self.coords(self._shelf_lines[3], ax2, h - 1, w, h - 1)
        self.itemconfig(self._shelf_lines[3], fill=hl if ax2 < w else "")

    def _update_tab(self, idx: int, x: float, w: float, h: int, label: str, activity: float) -> None:
        c = self._CLIP
        bg = self._lerp_color(self.ui.tab_inactive_bg, self.ui.bg_secondary, activity)
        fg = self._lerp_color(self.ui.text_secondary, self.ui.accent_color, activity)
        hl = self.ui.shadow_light    # highlight — üst/sol kenar (parlak)
        sh = self.ui.shadow_dark     # shadow — alt/sağ kenar (koyu)

        x1, y1 = round(x), 0
        x2, y2 = round(x + w) - 1, h

        # Kırpık köşeli sekme gövdesi (altıgen polygon)
        pts = [
            x1 + c, y1,
            x2 - c, y1,
            x2,     y1 + c,
            x2,     y2,
            x1,     y2,
            x1,     y1 + c,
        ]
        items = self._tab_items[idx]
        self.coords(items['poly'], *pts)
        self.itemconfig(items['poly'], fill=bg)

        lines = items['lines']
        # Highlight çizgileri
        self.coords(lines[0], x1 + c, y1, x2 - c, y1)
        self.itemconfig(lines[0], fill=hl)
        self.coords(lines[1], x1 + c, y1 + 1, x2 - c, y1 + 1)
        self.itemconfig(lines[1], fill=hl)
        self.coords(lines[2], x1, y1 + c, x1 + c, y1)
        self.itemconfig(lines[2], fill=hl)
        self.coords(lines[3], x1 + 1, y1 + c, x1 + c, y1 + 1)
        self.itemconfig(lines[3], fill=hl)
        self.coords(lines[4], x1, y1 + c, x1, y2)
        self.itemconfig(lines[4], fill=hl)
        self.coords(lines[5], x1 + 1, y1 + c, x1 + 1, y2)
        self.itemconfig(lines[5], fill=hl)

        # Shadow çizgileri
        self.coords(lines[6], x2 - c, y1, x2, y1 + c)
        self.itemconfig(lines[6], fill=sh)
        self.coords(lines[7], x2 - c, y1 + 1, x2 - 1, y1 + c)
        self.itemconfig(lines[7], fill=sh)
        self.coords(lines[8], x2, y1 + c, x2, y2)
        self.itemconfig(lines[8], fill=self.ui.bg_color)
        self.coords(lines[9], x2 - 1, y1 + c, x2 - 1, y2)
        self.itemconfig(lines[9], fill=sh)

        font = (
            (self.ui.font_main[0], 8, "bold")
            if activity > 0.5
            else self.ui.font_small
        )
        self.coords(items['text'], x + w / 2, h / 2)
        self.itemconfig(items['text'], text=label, fill=fg, font=font)
