# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/). Versiyon: [Semantic Versioning](https://semver.org/).

## [1.1.0] — 2026-04-25

### Eklendi
- Çoklu dil desteği (Türkçe / İngilizce), menüden anlık geçiş
- Dil tercihi kalıcılığı: `core/ayarlar.py` — atomik yazma, whitelist doğrulama, graceful degradation
- `core/ayarlar.py` için 15 birim testi (eksik dosya, bozuk JSON, geçersiz değer, OSError senaryoları)

### İyileştirildi
- `AnimatedTabBar`: Win98 çift katmanlı bevel kenarları (dış + iç highlight/shadow çizgisi), kırpık köşelerin arkasında Canvas arka planı görünmez
- Pasif sekme rengi `bg_secondary`'den 15 birim karanlık — gerçek "bir ton koyusu" yerine shadow rengiyle özdeş değer kullanılıyordu
- Windows 11 yuvarlak köşe efekti DWM API ile devre dışı bırakıldı (`DWMWA_WINDOW_CORNER_PREFERENCE`)

## [1.0.0] — 2026-04-25

### Eklendi
- Özel animasyonlu sekme çubuğu (`AnimatedTabBar`): ease-out cubic eğrisiyle kaydırmalı gösterge, ttk.Notebook navigasyonunun yerini aldı
- Altı araç: Değişim, Ortalama, KDV, İndirim, Oran, Yaş
- Agnostik sayı ayrıştırma: TR (`1.500,50`) ve US (`1,500.50`) formatlarını eş zamanlı tanır
- Hesap şeridi paneli (açılıp kapanabilir, `Ctrl+H`)
- `Decimal` tabanlı finansal hassasiyet
- Tüm sonuç label'larında tıkla-kopyala
- Klavye öncelikli navigasyon (`Ctrl+1–6`, `Tab`, `Enter`, `Esc`, `F1`)
- 8-point design grid (her boyut 4 veya 8'in katı)
- Neo-retro warm brutalism tasarım sistemi
- Windows için bağımsız .exe derleme (`build.bat`)
- `core/` katmanı için kapsamlı birim testi (IEEE 754, artık yıl, sıfıra bölme sınır vakaları)
