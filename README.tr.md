<div align="center">
  <h1>Hesap Defteri</h1>
  <p>Yapıştır, hesapla.</p>

  [![Lisans: MIT](https://img.shields.io/badge/Lisans-MIT-blue.svg)](LICENSE.md)
  [![Sürüm](https://img.shields.io/github/v/release/zntkr/hesap-defteri)](https://github.com/zntkr/hesap-defteri/releases/latest)
  [![Platform](https://img.shields.io/badge/Platform-Windows-0078d7.svg?logo=windows)](https://microsoft.com/windows)
</div>

---

Fatura satırı, tablo verisi, e-postaya gömülü rakam — ne yapıştırırsan yapıştır, Hesap Defteri okur. Türk (`1.500,50`) ve ABD (`1,500.50`) formatlarını aynı anda tanır, ayar gerektirmez.

Günlük masaüstü hesapları için altı araç: değişim oranı, istatistik, KDV, indirim, orantı, yaş. Tüm sonuçlar tıkla-kopyala. Kurulum yok, bulut yok, hiçbir veri saklanmaz.

## Kurulum

`HesapDefteri.exe` dosyasını [Releases](https://github.com/zntkr/hesap-defteri/releases/latest) sayfasından indir, çift tıkla, hazır. Runtime gerekmez.

**Kaynak koddan çalıştırmak için:**

```bash
git clone https://github.com/zntkr/hesap-defteri.git
cd hesap-defteri
python main.py
```

`pip install` gerekmez. Python 3.8+ yeterli.

## Araçlar

| # | Araç | Ne yapar |
|---|------|----------|
| 1 | DEĞİŞİM | İki değer arasındaki yüzde değişimi |
| 2 | ORTALAMA | Serbest metinden ortalama, medyan, std sapma, aralık, adet |
| 3 | KDV | KDV dahil / hariç hesaplama |
| 4 | İNDİRİM | İndirim / net fiyat |
| 5 | ORAN | Çapraz çarpım / orantı |
| 6 | YAŞ | Tam yaş, yaşanan gün sayısı, sonraki doğum günü |

Türkçe ve İngilizce arayüz (`Görünüm → Dil`). Tercih kalıcı olarak kaydedilir.

## Teknik olarak ilginç olan

Sekme çubuğu standart bir widget değil, elle çizilmiş `tk.Canvas` — sekmeler arası geçişler o anki konumdan devam eder, hızlı tıklamada animasyon başa sarılmaz. Uygulama ilk karede tam boyutuyla açılır, titreme olmaz. Finansal hesaplamalar baştan sona `Decimal` kullanır; kayan nokta hatasının KDV zincirlerinde birikmesi önemsiz değildir. Ayarlar atomik yazılır, bozuk dosyada sessizce varsayılana döner.

## Ne yapmaz

- Veri saklamaz — hiçbir şey loglanmaz, oturumlar arası veri kalmaz
- Elektronik tablo yerine geçmez — formül veya geçmiş yok
- Mobil veya web sürümü yok — tasarım gereği yalnızca Windows masaüstü

## Klavye kısayolları

| Kısayol | İşlev |
|---------|-------|
| `Ctrl+1` … `Ctrl+6` | Araçlar arası geç |
| `Ctrl+Tab` | Sıradaki araç |
| `Enter` | Hesapla |
| `Esc` | Temizle |
| `F1` | Kullanım kılavuzu |

## Testler

```bash
python -m unittest discover
```

IEEE 754 hassasiyet sınır durumları, artık yıl yaş hesabı (29 Şubat doğumlular), TR/ABD format belirsizliği, sıfıra bölme, bozuk ayar dosyası dahil.

---

[English README](README.md)

---

<sub>Saf Python · tkinter · sıfır runtime bağımlılığı</sub>
