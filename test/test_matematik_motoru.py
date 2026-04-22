import unittest
import sys
import os

# Proje kök dizinini Python yoluna ekle (core modülünü bulabilmesi için)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.matematik_motoru import MatematikMotoru

class TestMatematikMotoru(unittest.TestCase):

    def test_sayilari_ayikla_temel(self):
        metin = "10 20 30"
        beklenen = [10.0, 20.0, 30.0]
        self.assertEqual(MatematikMotoru.metinden_sayilari_ayikla(metin), beklenen)

    def test_sayilari_ayikla_karisik(self):
        # Agnostic Parsing kuralını test ediyoruz (Metin içinden sayıları sağ salim çıkarabiliyor mu?)
        metin = "Ocak ayında 15.5 TL harcandı, -5 TL iade edildi."
        beklenen = [15.5, -5.0]
        self.assertEqual(MatematikMotoru.metinden_sayilari_ayikla(metin), beklenen)

    def test_sayilari_ayikla_bitisik_metin(self):
        # Sayılara bitişik harf veya semboller (Örn: 100px, v2.5, 50kg)
        metin = "Genişlik 100px, sürüm v2.5 ve ağırlık 50kg."
        beklenen = [100.0, 2.5, 50.0]
        self.assertEqual(MatematikMotoru.metinden_sayilari_ayikla(metin), beklenen)

    def test_sayilari_ayikla_sadece_isaretler(self):
        # Sadece artı, eksi veya nokta olan (rakam içermeyen) metinler "yalancı" sayılardır
        metin = "Burada + ve - veya sadece . karakterleri var."
        beklenen = []
        self.assertEqual(MatematikMotoru.metinden_sayilari_ayikla(metin), beklenen)

    def test_sayilari_ayikla_bos(self):
        # Graceful Degradation: Hatalı/sayısız metinde çökmeyip boş liste dönmeli
        metin = "Burada hiç sayı yok"
        beklenen = []
        self.assertEqual(MatematikMotoru.metinden_sayilari_ayikla(metin), beklenen)

    def test_sayilari_ayikla_binlik_ayiricilar(self):
        # US Format: 1,500,000.50 -> 1500000.5
        # EU/TR Format: 1.500.000,50 -> 1500000.5
        # Virgüllü ondalık: 15,5 -> 15.5
        # Çoklu binlik: 1.500.000 -> 1500000.0
        # Sadece virgüllü çoklu binlik: 1,500,000 -> 1500000.0
        metin = "US 1,500,000.50, TR 1.500.000,50, basit 15,5, TR 1.500.000 ve US 1,500,000"
        beklenen = [1500000.5, 1500000.5, 15.5, 1500000.0, 1500000.0]
        self.assertEqual(MatematikMotoru.metinden_sayilari_ayikla(metin), beklenen)

    def test_sayilari_ayikla_hatali_formatlar(self):
        # Regex'ten geçip float'a dönüşemeyen karmaşık yapılar (ValueError çökme koruması testi)
        # Örn: 1.234,567.89 -> 1.234567.89 -> ValueError
        metin = "Hatalı bir sayı formu olan 1.234,567.89 motoru çökertmemeli, atlanmalı."
        self.assertEqual(MatematikMotoru.metinden_sayilari_ayikla(metin), [])

    def test_detayli_analiz_yap_temel(self):
        sayilar = [10.0, 20.0, 30.0, 40.0, 50.0]
        analiz = MatematikMotoru.detayli_analiz_yap(sayilar)
        
        self.assertIsNotNone(analiz)
        # Pylance için açıkça Type Narrowing (Tip Daraltması) yapıyoruz:
        assert isinstance(analiz, dict)
        
        self.assertEqual(analiz["ortalama"], 30.0)
        self.assertEqual(analiz["adet"], 5)
        self.assertEqual(analiz["en_buyuk"], 50.0)
        self.assertEqual(analiz["en_kucuk"], 10.0)
        self.assertEqual(analiz["medyan"], 30.0)
        self.assertEqual(analiz["toplam"], 150.0)
        self.assertEqual(analiz["varyans"], 250.0)
        self.assertEqual(analiz["std_sapma"], 15.8114)

    def test_detayli_analiz_yap_sifir_degerleri(self):
        # 0 değerlerinin ve ortalama/toplamın 0 çıkmasının mantığı bozmadığını test ediyoruz
        sayilar = [0.0, 10.0, -10.0]
        analiz = MatematikMotoru.detayli_analiz_yap(sayilar)
        
        self.assertIsNotNone(analiz)
        # Pylance için açıkça Type Narrowing (Tip Daraltması) yapıyoruz:
        assert isinstance(analiz, dict)
        
        self.assertEqual(analiz["ortalama"], 0.0)
        self.assertEqual(analiz["adet"], 3)
        self.assertEqual(analiz["en_buyuk"], 10.0)
        self.assertEqual(analiz["en_kucuk"], -10.0)
        self.assertEqual(analiz["medyan"], 0.0)
        self.assertEqual(analiz["toplam"], 0.0)
        self.assertEqual(analiz["varyans"], 100.0)
        self.assertEqual(analiz["std_sapma"], 10.0)

    def test_detayli_analiz_yap_tek_eleman(self):
        # Sadece 1 eleman içeren listede istatistik (Medyan, Ort vb.) çökmemeli ve kendini dönmeli
        sayilar = [42.0]
        analiz = MatematikMotoru.detayli_analiz_yap(sayilar)
        
        self.assertIsNotNone(analiz)
        assert isinstance(analiz, dict)
        
        self.assertEqual(analiz["ortalama"], 42.0)
        self.assertEqual(analiz["medyan"], 42.0)
        self.assertEqual(analiz["en_buyuk"], 42.0)
        self.assertEqual(analiz["en_kucuk"], 42.0)
        self.assertEqual(analiz["varyans"], 0.0)
        self.assertEqual(analiz["std_sapma"], 0.0)

    def test_detayli_analiz_yap_hassasiyet(self):
        # IEEE 754 Kayan nokta problemi: 0.1 + 0.2 = 0.30000000000000004 sorununu ':g' çözüyor mu?
        sayilar = [0.1, 0.2]
        analiz = MatematikMotoru.detayli_analiz_yap(sayilar)
        
        self.assertIsNotNone(analiz)
        assert isinstance(analiz, dict)
        self.assertEqual(analiz["toplam"], 0.3)
        self.assertEqual(analiz["ortalama"], 0.15)
        self.assertEqual(analiz["varyans"], 0.005)
        self.assertEqual(analiz["std_sapma"], 0.0707107) # :g formatı 6 anlamlı basamağa yuvarlar

    def test_detayli_analiz_yap_bos_liste(self):
        # Anayasaya göre sayi_listesi boşsa None dönmelidir
        self.assertIsNone(MatematikMotoru.detayli_analiz_yap([]))

if __name__ == '__main__':
    unittest.main()