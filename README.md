# Hesap Defteri

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.md)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://python.org)
[![Dependencies](https://img.shields.io/badge/runtime%20dependencies-zero-brightgreen.svg)](requirements.txt)

Türk ofis çalışanları için tasarlanmış finansal ve istatistiksel masaüstü hesap makinesi. Standart Python kütüphanesi dışında hiçbir bağımlılık yok — yalnızca `tkinter`, mühendislik sınırlarına kadar zorlunmuş.

---

## Teknik açıdan ilginç olan ne?

**Özel animasyonlu sekme çubuğu** — Sekme navigasyonu sıfırdan inşa edildi: `tk.Button` dizisi ve `tk.Canvas` üzerinde ease-out cubic interpolasyonla kayan bir gösterge çizgisi. `after()` döngüsü, rapid tıklamalarda o anki görsel konumdan başlayarak animasyonu kesmeden sürdürür.

**Agnostik sayı ayrıştırma** — Tek bir regex deseni, Türkçe (`1.500,50`) ve Amerikan (`1,500.50`) binlik ayırıcı formatlarını eş zamanlı tanır. Fatura, e-posta veya tablo içeriğini yapıştırın — motor format konfigürasyonu beklemeden sayıları çıkarır.

**Decimal hassasiyetiyle finans** — Tüm finansal hesaplamalar Python'un `Decimal` sınıfıyla yapılır. Float'ın IEEE 754 birikimli yuvarlama hatası KDV zincirlerinde önemlidir.

**8-point design grid** — Her dolgu, kenar boşluğu ve pencere boyutu 4 veya 8'in katıdır. Sistem bunu kodda zorunlu kılar; bu da görsel ritmi tutarlı yapar.

**Üç katmanlı mimari** — `core/` modülü tkinter'dan tamamen izole saf fonksiyonlardan oluşur. Aynı dosyalar bir Flask API'sine veya CLI aracına olduğu gibi taşınabilir.

---

## Araçlar

| # | Sekme | Açıklama |
|---|-------|----------|
| 1 | DEĞİŞİM | İki değer arasındaki yüzdelik değişim |
| 2 | ORTALAMA | Ham metinden istatistiksel analiz (ortalama, medyan, std. sapma, açıklık, adet) |
| 3 | KDV | KDV hesaplama — brüt veya netten matrah ve KDV tutarı |
| 4 | İNDİRİM | İndirim hesaplama |
| 5 | ORAN | Oran / içler-dışlar orantısı |
| 6 | YAŞ | Detaylı yaş raporu: tam yaş, doğum günü, yaşanılan gün sayısı, sonraki doğum günü |

Tüm sonuçlar tıklanabilir — bir tıkla değer panoya kopyalanır.

---

## Hızlı başlangıç

```bash
git clone https://github.com/zntkr/hesapdefteri.git
cd hesapdefteri
python main.py
```

`pip install` yok. Sanal ortam kurulumu yok. Python 3.8+ yeterli.

### Windows için bağımsız .exe oluşturma

```
build.bat
```

`build.bat`'a çift tıklayın. PyInstaller yoksa otomatik kurar. Çıktı: `dist/HesapDefteri.exe` — kurulum gerektirmeyen tek taşınabilir dosya.

---

## Klavye kısayolları

| Kısayol | Eylem |
|---------|-------|
| `Ctrl+1` … `Ctrl+6` | Araca doğrudan geç |
| `Ctrl+Tab` | Araçlar arasında sırayla dön |
| `Enter` | Aktif araçta hesapla |
| `Esc` | Aktif aracı temizle |
| `Ctrl+H` | Hesap şeridini aç / kapat |
| `F1` | Kullanma rehberini aç |

---

## Mimari

```
hesapdefteri/
├── main.py                    # Boot: pencere başlatma, flicker önleme, kaynak yolları
├── core/
│   ├── matematik_motoru.py    # Durumsuz: sayı çıkarma + istatistik (4 ondalık, float)
│   └── finans_motoru.py       # Durumsuz: KDV, indirim, yaş, oran (Decimal, 2 ondalık)
└── ui/
    ├── arayuz_tasarimi.py     # MainUI: tema, menüler, klavye kısayolları
    ├── tools_tab.py           # ToolsTab: çerçeve yönetimi + klavye yönlendirme
    ├── animated_tab_bar.py    # AnimatedTabBar: özel kaydırmalı gösterge
    ├── base_tool.py           # BaseToolWidget: ortak UI desenleri + pano
    ├── average_tool.py        # Ortalama Hesaplayıcı
    ├── tax_tool.py            # KDV Hesaplayıcı
    ├── discount_tool.py       # İndirim Hesaplayıcı
    ├── change_tool.py         # Değişiklik Hesaplayıcı
    ├── proportion_tool.py     # Oran Hesaplayıcı
    └── age_tool.py            # Yaş Hesaplayıcı
```

**Katman kuralları:**
- `core/` → sıfır tkinter importu, saf hesaplama
- `ui/` → sıfır iş mantığı, yalnızca sunum ve girdi
- `main.py` → yalnızca pencere başlatma ve event loop

---

## Tasarım sistemi

| Değişken | Renk | Rol |
|----------|------|-----|
| `bg_color` | `#4A423A` | Masa yüzeyi (koyu ceviz) |
| `bg_secondary` | `#EFEBE6` | Kağıt yüzeyi |
| `input_bg` | `#F9F8F6` | Giriş alanları |
| `accent_color` | `#C85A47` | Kiremit — birincil eylem |
| `fg_color` | `#2D2D2D` | Gövde metni |
| `tape_bg` | `#F4F1EA` | Hesap şeridi (saman sarısı kağıt) |

**Tipografi** — IBM Plex Mono → Consolas → Courier New → Courier (monospace basamağı)

**Skeuomorfizm** — Kağıt sayfalar fiziksel 3D kenarlara sahip (`#FFFFFF` highlight / `#D3CFC8` gölge). 45° masa gölgesi kaydırılmış koyu çerçevelerle simüle edilir. Sol kenara cilt delikleri açılmıştır.

---

## Testler

```bash
# Tüm testler
python -m unittest discover

# Tek modül
python -m unittest test.test_matematik_motoru

# Kapsam raporu (core/ için)
python run_coverage.py
```

`core/` katmanı tam sınır testi kapsamına sahiptir: IEEE 754 hassasiyeti, artık yıl yaş hesaplaması (29 Şubat doğum tarihleri), TR/US format ayrımı, sıfıra bölme koruması.

---

> *"İşini yapar ve sistem kaynaklarını serbest bırakır."*
