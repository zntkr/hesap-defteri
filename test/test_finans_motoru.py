import unittest
import sys
import os
from datetime import datetime, timedelta
from unittest.mock import patch
import math

# Proje kök dizinini Python yoluna ekle (core modülünü bulabilmesi için)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.finans_motoru import FinansMotoru

class TestFinansMotoru(unittest.TestCase):

    def test_kdv_hesapla(self):
        sonuc = FinansMotoru.kdv_hesapla(1000, 20)
        self.assertEqual(sonuc["ham_tutar"], 1000.0)
        self.assertEqual(sonuc["kdv_tutari"], 200.0)
        self.assertEqual(sonuc["toplam"], 1200.0)
        
        # Ondalıklı/Küsüratlı Test
        sonuc_ondalik = FinansMotoru.kdv_hesapla(150.50, 18)
        self.assertEqual(sonuc_ondalik["kdv_tutari"], 27.09)

    def test_indirim_hesapla(self):
        sonuc = FinansMotoru.indirim_hesapla(2000, 15)
        self.assertEqual(sonuc["indirim_tutari"], 300.0)
        self.assertEqual(sonuc["net_tutar"], 1700.0)

    def test_degisim_orani_hesapla(self):
        # Artış senaryosu
        sonuc_artis = FinansMotoru.degisim_orani_hesapla(100, 150)
        self.assertEqual(sonuc_artis["degisim_orani"], 50.0)
        
        # Azalış senaryosu
        sonuc_azalis = FinansMotoru.degisim_orani_hesapla(200, 150)
        self.assertEqual(sonuc_azalis["degisim_orani"], -25.0)
        
        # Sıfıra bölünme koruması (eski değer 0 ise)
        sonuc_sifir = FinansMotoru.degisim_orani_hesapla(0, 100)
        self.assertEqual(sonuc_sifir["degisim_orani"], 0)

    def test_yas_hesapla(self):
        # Gelecek problemi yaşamamak için bugüne göre dinamik "10 yıl önce" tarihi
        bugun = datetime.now()
        gecmis = bugun - timedelta(days=365 * 10 + 2) # Yaklaşık 10 yıl
        tarih_str = gecmis.strftime("%d.%m.%Y")
        
        sonuc = FinansMotoru.yas_hesapla(tarih_str)
        self.assertIn("yillar", sonuc)
        self.assertEqual(sonuc["yillar"], 10)

    def test_yas_hesapla_hatalar(self):
        # Geçersiz format testi
        sonuc_format = FinansMotoru.yas_hesapla("45.15.1990")
        self.assertEqual(sonuc_format["hata"], "Geçersiz format")
        
        # Gelecek tarih testi
        gelecek = datetime.now() + timedelta(days=365 * 5)
        sonuc_gelecek = FinansMotoru.yas_hesapla(gelecek.strftime("%d.%m.%Y"))
        self.assertEqual(sonuc_gelecek["hata"], "Gelecek tarih")

    @patch('core.finans_motoru.datetime')
    def test_yas_hesapla_kapsam_artirici(self, mock_datetime):
        # Sahte bir bugün tarihi ayarlıyoruz: 10 Ocak 2026
        mock_datetime.now.return_value = datetime(2026, 1, 10)
        mock_datetime.strptime = datetime.strptime # strptime metodunu bozmamak için orijinaline bağlıyoruz
        
        # 1. Aylar < 0 Tetiklemesi (Doğum: 15 Mayıs 2020)
        sonuc_ay_eksi = FinansMotoru.yas_hesapla("15.05.2020")
        self.assertEqual(sonuc_ay_eksi["yillar"], 5)
        
        # 2. Günler < 0 Tetiklemesi (Doğum: 15 Ocak 2020)
        sonuc_gun_eksi = FinansMotoru.yas_hesapla("15.01.2020")
        self.assertEqual(sonuc_gun_eksi["yillar"], 5)
        
        # 3. Artık Yıl (29 Şubat) kapsamı ve ValueError tetiklemeleri
        # (Bu test, replace() hatalarının tümünü başarıyla cover eder)
        sonuc_artik = FinansMotoru.yas_hesapla("29.02.2020")
        self.assertEqual(sonuc_artik["yillar"], 5)

        # 4. Negatif Gün Mantık Hatası Testi (Örn: 31 Ocak doğum, 1 Mart bugün)
        mock_datetime.now.return_value = datetime(2020, 3, 1) # Artık yıl
        sonuc_negatif_gun = FinansMotoru.yas_hesapla("31.01.2020")
        # 31 Ocak'tan 29 Şubat'a 1 ay. 29 Şubat'tan 1 Mart'a 1 gün. Toplam: 1 Ay 1 Gün (Eskiden -1 Gün çıkıyordu)
        self.assertEqual(sonuc_negatif_gun["yillar"], 0)
        self.assertEqual(sonuc_negatif_gun["aylar"], 1)
        self.assertEqual(sonuc_negatif_gun["gunler"], 1)

    def test_oranti_hesapla(self):
        # 150 ürün 4500 ise, 75 ürün = 2250
        sonuc = FinansMotoru.oranti_hesapla(150, 4500, 75)
        self.assertEqual(sonuc["sonuc"], 2250.0)
        
        # 1. değer sıfır olursa ZeroDivisionError koruması
        sonuc_sifir = FinansMotoru.oranti_hesapla(0, 4500, 75)
        self.assertEqual(sonuc_sifir["hata"], "1. Deger sifir olamaz")

    def test_temiz_sayi_sonsuz_deger(self):
        # Çok yüksek işlemlerde veya geçersiz durumlarda Infinity'nin çökme yaratmaması
        sonsuz = float('inf')
        nan_deger = float('nan')
        
        self.assertTrue(math.isinf(FinansMotoru._temiz_sayi(sonsuz)))
        self.assertTrue(math.isnan(FinansMotoru._temiz_sayi(nan_deger)))

    def test_temiz_sayi_cok_buyuk_sayi(self):
        # Decimal'in precision limitini (varsayılan 28) aşıp InvalidOperation hatasına
        # düşecek ve fallback (round) bloğunu çalıştıracak devasa sayıların testi.
        cok_buyuk_sayi = 1e300
        sonuc = FinansMotoru._temiz_sayi(cok_buyuk_sayi)
        self.assertEqual(sonuc, 1e300)

if __name__ == '__main__':
    unittest.main()