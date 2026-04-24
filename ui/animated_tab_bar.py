import tkinter as tk
from typing import Callable, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ui.arayuz_tasarimi import MainUI


class AnimatedTabBar(tk.Canvas):
    """
    Windows 98 tarzı kırpık köşeli sekme çubuğu.

    Tek Canvas üzerinde tüm sekmeler çizilir. Aktif sekmenin alt kenarı yoktur —
    içerik alanıyla görsel olarak birleşir. Renk geçişleri ease-out cubic ile
    interpolasyonlanır; animasyon rapid tıklamalarda mevcut progress'ten devam eder.
    """

    _H: int = 24        # sekme yüksekliği (px)
    _CLIP: int = 5      # üst köşe kırpma (px)
    _STEPS: int = 8
    _INTERVAL_MS: int = 16   # ~62 fps → toplam ~130 ms geçiş

    def __init__(
        self,
        parent: tk.Misc,
        ui: "MainUI",
        labels: List[str],
        on_change: Callable[[int], None],
    ) -> None:
        super().__init__(
            parent,
            height=self._H,
            bg=ui.bg_color,
            highlightthickness=0,
            bd=0,
            cursor="hand2",
        )
        self.ui = ui
        self.labels = labels
        self.on_change = on_change
        self._current_idx: int = 0
        self._anim_job: Optional[str] = None
        # Her sekme için activity seviyesi: 0.0 = tam pasif, 1.0 = tam aktif
        self._progress: List[float] = [0.0] * len(labels)

        self.bind("<Configure>", lambda e: self._redraw())
        self.bind("<Button-1>", self._on_click)
        self.after(60, lambda: self.select(0, animate=False))

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

    def _redraw(self) -> None:
        self.delete("all")
        n = len(self.labels)
        w = self.winfo_width()
        h = self._H
        if w <= 1 or n == 0:
            return
        tab_w = w / n

        for i, label in enumerate(self.labels):
            self._draw_tab(i * tab_w, tab_w, h, label, self._progress[i])

        # Raf çizgisi: sekme çubuğunu içerik alanından ayırır, aktif sekme altında kesilir.
        # Tablar çizildikten SONRA çizilir → pasif sekmelerin alt bevel çizgilerinin üzerine gelir.
        ax1 = round(self._current_idx * tab_w)
        ax2 = round((self._current_idx + 1) * tab_w)
        hl, sh = self.ui.shadow_light, self.ui.shadow_dark

        if ax1 > 0:                                          # sol segment
            self.create_line(0,   h - 2, ax1, h - 2, fill=sh)
            self.create_line(0,   h - 1, ax1, h - 1, fill=hl)
        if ax2 < w:                                          # sağ segment
            self.create_line(ax2, h - 2, w,   h - 2, fill=sh)
            self.create_line(ax2, h - 1, w,   h - 1, fill=hl)

    def _draw_tab(
        self, x: float, w: float, h: int, label: str, activity: float
    ) -> None:
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
        self.create_polygon(pts, fill=bg, outline="")

        # Highlight çizgileri (üst ve sol kenar — parlak)
        self.create_line(x1 + c, y1, x2 - c, y1, fill=hl)           # üst düz (dış)
        self.create_line(x1 + c, y1 + 1, x2 - c, y1 + 1, fill=hl)   # üst düz (iç)
        self.create_line(x1, y1 + c, x1 + c, y1, fill=hl)           # üst-sol diagonal (dış)
        self.create_line(x1 + 1, y1 + c, x1 + c, y1 + 1, fill=hl)   # üst-sol diagonal (iç)
        self.create_line(x1, y1 + c, x1, y2, fill=hl)               # sol kenar (dış)
        self.create_line(x1 + 1, y1 + c, x1 + 1, y2, fill=hl)       # sol kenar (iç)

        # Shadow çizgileri (sağ kenar — koyu)
        self.create_line(x2 - c, y1, x2, y1 + c, fill=sh)           # üst-sağ diagonal (dış)
        self.create_line(x2 - c, y1 + 1, x2 - 1, y1 + c, fill=sh)   # üst-sağ diagonal (iç)
        self.create_line(x2, y1 + c, x2, y2, fill=self.ui.bg_color) # sağ kenar (dış) - Masayı gösteren fiziksel kesik
        self.create_line(x2 - 1, y1 + c, x2 - 1, y2, fill=sh)       # sağ kenar (iç)

        # Alt kenar _draw_tab'dan kaldırıldı — raf çizgisi _redraw'da toplu çizilir.

        # Sekme etiketi
        font = (
            (self.ui.font_main[0], 9, "bold")
            if activity > 0.5
            else (self.ui.font_main[0], 9)
        )
        self.create_text(x + w / 2, h / 2, text=label, fill=fg, font=font)
