# Hesaplayıcı v1.0.0 🧮

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

Sistem Anayasasına uygun olarak geliştirilmiş, **stateless (durumsuz)** ve **agnostik** bir veri analiz ve hesaplama aracıdır. Sıfır bloatware, sıfır telemetri ve maksimum odak prensibiyle, tamamen standart Python kütüphaneleri kullanılarak inşa edilmiştir.

## 🚀 Öne Çıkan Özellikler

* **Agnostik Veri Girişi:** Kopyaladığınız metnin içinde harfler, semboller veya boşluklar olması fark etmez. Akıllı Regex motoru, metin içindeki sayıları (Binlik ayırıcılar dahil - US ve TR formatlarını otomatik tanıyarak) kusursuzca ayıklar.
* **Gelişmiş İstatistikler:** Sadece aritmetik ortalama almaz; girilen verinin En Büyük, En Küçük, Medyan, Varyans ve Standart Sapma değerlerini eş zamanlı olarak hesaplar.
* **Oturum Belleği (Geçmiş):** Yaptığınız tüm işlemler arka planda tutulur. Eski bir sonuca çift tıklayarak veri setini tekrar ana ekrana yükleyebilirsiniz.
* **Neo-Retro (Warm Brutalism) Arayüz:** Göz yormayan sıcak krem arka plan, daktilo mürekkebi metinler ve kiremit rengi vurgularla "IBM Plex Mono" tipografisini birleştiren elit masaüstü tasarımı.
* **Operasyonel Kısayollar:** Klavye öncelikli (Keyboard-first) tasarlanmıştır. Çıkan sonuca tıklanması durumunda değer otomatik olarak sistem panosuna kopyalanır.

## 🏗️ Mimari Yapı (Modular Monolith)

Proje "Separation of Concerns" (Sorumlulukların Ayrıştırılması) prensibine göre tasarlanmıştır:

* **`core/matematik_motoru.py` (Logic Layer):** Tamamen durumsuz (stateless) matematiksel işlemler ve regex veri ayıklama motoru. Arayüzden tamamen izoledir ve bu sayede API veya CLI araçlarına kolayca entegre edilebilir.
* **`ui/arayuz_tasarimi.py` (Presentation Layer):** Durum yönetimi (State) ve arayüz çizimlerinden sorumlu UI katmanı.
* **`main.py` (Boot):** Sistemin başlatıcı (Entry Point) dosyası. İşletim sistemi kaynaklı pencere zıplamalarını (flicker/FOUC) engelleyen "Perde Arkası" çizim mantığını yönetir.

## 🛠️ Kurulum ve Kullanım

### 1. Kaynak Koddan Çalıştırma
Bilgisayarınızda Python yüklü olduğundan emin olun. Hiçbir harici kütüphane (dependency) kurmanıza gerek yoktur. Terminalden proje dizinine giderek şu komutu çalıştırın:
```bash
python main.py
```

### 2. Tek Dosya Halinde Derleme (.exe)
Windows kullanıcıları için projeyi bağımsız, taşınabilir ve kurulum gerektirmeyen tek bir çalıştırılabilir dosya haline getirmek çok kolaydır:
1. Proje dizinindeki `build.bat` dosyasına çift tıklayın. (Eğer sisteminizde PyInstaller yoksa otomatik kuracaktır).
2. Tam karantina kurallarıyla derlenen `Hesaplayici.exe` dosyanız, işlem bittiğinde `dist/` klasörü içinde hazır olacaktır.

## 🧪 Testleri Çalıştırma

Projenin kalbi olan `MatematikMotoru`, sınır değerleri (Edge cases), IEEE 754 kayan nokta hassasiyeti ve binlik ayırıcı senaryolarını barındıran kapsamlı bir test süitine sahiptir.

Birim testlerini (Unit Tests) çalıştırmak için proje ana dizininde şu komutu kullanın:
```bash
python -m unittest tests/test_matematik_motoru.py
```
Ekranda `OK` mesajını gördüğünüzde, motorun tüm sınır testlerinden başarıyla geçtiğinden emin olabilirsiniz.

---

> *"İşini yapar ve sistem kaynaklarını serbest bırakır."*