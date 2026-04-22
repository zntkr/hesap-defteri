from typing import Dict, Union
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta

class FinansMotoru:
    """
    Stateless (durumsuz) finans ve oran hesaplama motoru.
    KDV, yüzde hesaplamaları ve basit ticari araçları barındırır.
    """

    @staticmethod
    def _temiz_sayi(deger: float) -> Union[float, int]:
        """Finansal veriyi 2 basamağa yuvarlar ve gereksiz .0 küsuratını atar."""
        # IEEE 754 float kayıplarını ve Banker's Rounding'i aşmak için Decimal kullanıyoruz
        v = float(Decimal(str(deger)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
        return int(v) if v.is_integer() else v

    @staticmethod
    def kdv_hesapla(tutar: float, oran: float = 20.0) -> Dict[str, Union[float, int]]:
        """Verilen tutar üzerinden KDV tutarını ve toplam matrahı hesaplar."""
        kdv_tutari = tutar * (oran / 100)
        toplam_tutar = tutar + kdv_tutari
        
        return {
            "ham_tutar": FinansMotoru._temiz_sayi(tutar),
            "kdv_tutari": FinansMotoru._temiz_sayi(kdv_tutari),
            "toplam": FinansMotoru._temiz_sayi(toplam_tutar)
        }

    @staticmethod
    def indirim_hesapla(tutar: float, oran: float = 10.0) -> Dict[str, Union[float, int]]:
        """Verilen tutar üzerinden indirim miktarını ve net (indirimli) tutarı hesaplar."""
        indirim_tutari = tutar * (oran / 100)
        net_tutar = tutar - indirim_tutari
        
        return {
            "ham_tutar": FinansMotoru._temiz_sayi(tutar),
            "indirim_tutari": FinansMotoru._temiz_sayi(indirim_tutari),
            "net_tutar": FinansMotoru._temiz_sayi(net_tutar)
        }

    @staticmethod
    def degisim_orani_hesapla(eski_deger: float, yeni_deger: float) -> Dict[str, Union[float, int]]:
        """İki değer arasındaki yüzde değişim (artış/azalış) oranını hesaplar."""
        if eski_deger == 0:
            return {"eski_deger": 0, "yeni_deger": FinansMotoru._temiz_sayi(yeni_deger), "degisim_orani": 0}
            
        fark = yeni_deger - eski_deger
        oran = (fark / abs(eski_deger)) * 100
        
        return {
            "eski_deger": FinansMotoru._temiz_sayi(eski_deger),
            "yeni_deger": FinansMotoru._temiz_sayi(yeni_deger),
            "degisim_orani": FinansMotoru._temiz_sayi(oran)
        }

    @staticmethod
    def yas_hesapla(dogum_tarihi_str: str) -> Dict[str, Union[int, str]]:
        """Verilen doğum tarihine (GG.AA.YYYY) göre detaylı bir yaş/doğum günü analizi yapar."""
        try:
            # Kullanıcının "/" veya "-" girmesi ihtimaline karşı toleranslı (agnostik) temizleme
            temiz_tarih = dogum_tarihi_str.replace('/', '.').replace('-', '.')
            dogum = datetime.strptime(temiz_tarih, "%d.%m.%Y")
        except ValueError:
            return {"hata": "Geçersiz format"}
            
        # Saat farkından doğacak sapmaları engellemek için bugünü gece yarısına sabitliyoruz
        bugun = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        if dogum > bugun:
            return {"hata": "Gelecek tarih"}
            
        yillar = bugun.year - dogum.year
        aylar = bugun.month - dogum.month
        gunler = bugun.day - dogum.day
        
        if gunler < 0:
            aylar -= 1
            # Bir önceki ayın gün sayısını bulma
            ilk_gun = bugun.replace(day=1)
            onceki_ay_sonu = ilk_gun - timedelta(days=1)
            gunler += onceki_ay_sonu.day
            
        if aylar < 0:
            yillar -= 1
            aylar += 12
            
        aylar_tr = ["", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
        gunler_tr = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        
        # Artık yıl (29 Şubat) doğumlular için replace hatalarını yakalıyoruz
        try: son_dogum_gunu = dogum.replace(year=bugun.year)
        except ValueError: son_dogum_gunu = dogum.replace(year=bugun.year, day=28)
            
        if son_dogum_gunu > bugun:
            try: son_dogum_gunu = dogum.replace(year=bugun.year - 1)
            except ValueError: son_dogum_gunu = dogum.replace(year=bugun.year - 1, day=28)

        try: sonraki_dogum_gunu = dogum.replace(year=son_dogum_gunu.year + 1)
        except ValueError: sonraki_dogum_gunu = dogum.replace(year=son_dogum_gunu.year + 1, day=28)

        kalan_gun = (sonraki_dogum_gunu - bugun).days
        yasanilan_gun = (bugun - dogum).days + 1
        
        yasanilan_gun_str = f"{yasanilan_gun:,}".replace(",", ".")
        
        return {
            "yillar": yillar,
            "aylar": aylar,
            "gunler": gunler,
            "dogum_gunu_str": gunler_tr[dogum.weekday()],
            "sonraki_dogum_gunu_str": f"{sonraki_dogum_gunu.day} {aylar_tr[sonraki_dogum_gunu.month]} {sonraki_dogum_gunu.year} {gunler_tr[sonraki_dogum_gunu.weekday()]}",
            "kalan_gun": kalan_gun,
            "yasanilan_gun_str": yasanilan_gun_str
        }

    @staticmethod
    def oranti_hesapla(a: float, b: float, c: float) -> Dict[str, Union[float, int, str]]:
        """
        Doğru orantı (İçler dışlar) hesabı yapar.
        A değeri B'ye eşitse, C değeri X'e eşittir. X = (B * C) / A
        """
        if a == 0:
            return {"hata": "1. Deger sifir olamaz"}
            
        sonuc = (b * c) / a
        return {
            "sonuc": FinansMotoru._temiz_sayi(sonuc)
        }