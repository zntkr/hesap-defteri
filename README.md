<div align="center">
  <img src="assets/app_icon.png" alt="Hesap Defteri" width="80">
  <h1>Hesap Defteri</h1>
  <p>Paste any number. Get your answer.</p>

  [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE.md)
  [![Release](https://img.shields.io/github/v/release/zntkr/hesap-defteri)](https://github.com/zntkr/hesap-defteri/releases/latest)
  [![Platform](https://img.shields.io/badge/Platform-Windows-0078d7.svg?logo=windows)](https://microsoft.com/windows)
</div>

---

Most calculators make you format your input. Hesap Defteri works with whatever you paste — a line from an invoice, a row from a spreadsheet, a number buried in an e-mail. It reads Turkish (`1.500,50`) and US (`1,500.50`) formats simultaneously, without configuration.

Six tools covering the calculations that actually come up at a desk: percentage change, statistical analysis, VAT, discount, proportion, and age. Results are click-to-copy. No install, no cloud, no data stored anywhere.

## Install

Download `HesapDefteri.exe` from [Releases](https://github.com/zntkr/hesap-defteri/releases/latest), double-click, done. No runtime required.

**Or build from source:**

```bash
git clone https://github.com/zntkr/hesap-defteri.git
cd hesap-defteri
python main.py
```

No `pip install`. Python 3.8+ is sufficient.

## Tools

| # | Tool | What it does |
|---|------|--------------|
| 1 | CHANGE | Percentage change between two values |
| 2 | AVERAGE | Mean, median, std dev, range, count — from raw text |
| 3 | VAT | Gross-up or net-down |
| 4 | DISCOUNT | Discount / net price |
| 5 | RATIO | Cross-multiplication / proportion |
| 6 | AGE | Exact age, days lived, next birthday countdown |

Turkish and English UI (`View → Language`). Preference is persisted.

## What makes it interesting

The tab bar is a hand-drawn `tk.Canvas`, not a widget — tab transitions animate from their current interpolated position, so rapid switching never resets mid-motion. The window appears at full size on the first frame, no flicker. Financial calculations use `Decimal` throughout; float's IEEE 754 accumulation error is non-trivial in VAT chains. Settings survive crashes — written atomically, falls back silently on corruption.

## What it doesn't do

- Store your data — nothing is logged, nothing persists between sessions
- Replace a spreadsheet — no formulas, no history
- Run on mobile or web — desktop Windows only, by design

## Keyboard shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+1` … `Ctrl+6` | Jump to tool |
| `Ctrl+Tab` | Cycle tools |
| `Enter` | Calculate |
| `Esc` | Clear |
| `F1` | Usage guide |

## Tests

```bash
python -m unittest discover
```

Covers IEEE 754 precision edge cases, leap-year age (Feb 29 birthdays), TR/US format ambiguity, division by zero, corrupt settings file.

---

[Türkçe README](README.tr.md)

---

<sub>Built with pure Python · tkinter · zero runtime dependencies</sub>
