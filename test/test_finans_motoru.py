import unittest
import sys
import os

# Proje kök dizinini Python yoluna ekle (core modülünü bulabilmesi için)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.finans_motoru import FinansMotoru

class TestFinansMotoru(unittest.TestCase):

    def test_temiz_sayi(self):
        self.assertEqual(FinansMotoru._temiz_sayi(10.0), 10)
        self.assertEqual(FinansMotoru._temiz_sayi(10.50), 10.5)
        self.assertEqual(FinansMotoru._temiz_sayi(10.555), 10.56)  # 2 basamağa yuvarlama kontrolü
        self.assertEqual(FinansMotoru._temiz_sayi(10.554), 10.55)

    def test_temiz_sayi_asiri_kucuk_kusuratlar(self):
        self.assertEqual(FinansMotoru._temiz_sayi(10.0000001), 10)
        self.assertEqual(FinansMotoru._temiz_sayi(10.999), 11)
        self.assertEqual(FinansMotoru._temiz_sayi(-0.0), 0)

    def test_kdv_hesapla_varsayilan(self):
        sonuc = FinansMotoru.kdv_hesapla(100.0)
        self.assertEqual(sonuc["ham_tutar"], 100)
        self.assertEqual(sonuc["kdv_tutari"], 20)
        self.assertEqual(sonuc["toplam"], 120)

    def test_kdv_hesapla_ozel_oran(self):
        sonuc = FinansMotoru.kdv_hesapla(100.0, 18.0)
        self.assertEqual(sonuc["kdv_tutari"], 18)
        self.assertEqual(sonuc["toplam"], 118)

    def test_kdv_hesapla_sifir(self):
        sonuc = FinansMotoru.kdv_hesapla(0.0)
        self.assertEqual(sonuc["toplam"], 0)
        
    def test_kdv_hesapla_negatif_tutar(self):
        # İade/İptal faturası senaryosu (Negatif tutar)
        sonuc = FinansMotoru.kdv_hesapla(-100.0, 20.0)
        self.assertEqual(sonuc["ham_tutar"], -100)
        self.assertEqual(sonuc["kdv_tutari"], -20)
        self.assertEqual(sonuc["toplam"], -120)

    def test_indirim_hesapla_varsayilan(self):
        sonuc = FinansMotoru.indirim_hesapla(200.0)
        self.assertEqual(sonuc["ham_tutar"], 200)
        self.assertEqual(sonuc["indirim_tutari"], 20)
        self.assertEqual(sonuc["net_tutar"], 180)

    def test_indirim_hesapla_ozel_oran(self):
        sonuc = FinansMotoru.indirim_hesapla(200.0, 15.0)
        self.assertEqual(sonuc["indirim_tutari"], 30)
        self.assertEqual(sonuc["net_tutar"], 170)
        
    def test_indirim_hesapla_yuzdeyuz_indirim(self):
        # Bedelsiz ürün / %100 indirim senaryosu
        sonuc = FinansMotoru.indirim_hesapla(500.0, 100.0)
        self.assertEqual(sonuc["indirim_tutari"], 500)
        self.assertEqual(sonuc["net_tutar"], 0)

    def test_indirim_hesapla_sifir_indirim(self):
        sonuc = FinansMotoru.indirim_hesapla(250.0, 0.0)
        self.assertEqual(sonuc["indirim_tutari"], 0)
        self.assertEqual(sonuc["net_tutar"], 250)

    def test_degisim_orani_hesapla_artis(self):
        sonuc = FinansMotoru.degisim_orani_hesapla(100.0, 150.0)
        self.assertEqual(sonuc["degisim_orani"], 50.0)

    def test_degisim_orani_hesapla_azalis(self):
        sonuc = FinansMotoru.degisim_orani_hesapla(100.0, 75.0)
        self.assertEqual(sonuc["degisim_orani"], -25.0)

    def test_degisim_orani_hesapla_sifir_bolme_hatasi_onleme(self):
        # Eski değer 0 olduğunda sıfıra bölme hatası vermemeli
        sonuc = FinansMotoru.degisim_orani_hesapla(0.0, 100.0)
        self.assertEqual(sonuc["eski_deger"], 0)
        self.assertEqual(sonuc["yeni_deger"], 100)
        self.assertEqual(sonuc["degisim_orani"], 0)

    def test_degisim_orani_hesapla_negatif_degerler(self):
        sonuc = FinansMotoru.degisim_orani_hesapla(-50.0, -25.0)
        self.assertEqual(sonuc["degisim_orani"], 50.0)

    def test_degisim_orani_hesapla_degisim_yok(self):
        sonuc = FinansMotoru.degisim_orani_hesapla(100.0, 100.0)
        self.assertEqual(sonuc["degisim_orani"], 0.0)

    def test_degisim_orani_hesapla_negatiften_pozitife(self):
        # Zarardan kâra geçiş senaryosu (Eski: -50, Yeni: 50 -> Beklenen %200 artış)
        sonuc = FinansMotoru.degisim_orani_hesapla(-50.0, 50.0)
        self.assertEqual(sonuc["degisim_orani"], 200.0)

    def test_degisim_orani_hesapla_ikisi_de_sifir(self):
        sonuc = FinansMotoru.degisim_orani_hesapla(0.0, 0.0)
        self.assertEqual(sonuc["eski_deger"], 0)
        self.assertEqual(sonuc["yeni_deger"], 0)
        self.assertEqual(sonuc["degisim_orani"], 0.0)

if __name__ == '__main__':
    unittest.main()