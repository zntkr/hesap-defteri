from typing import Dict, Union
from decimal import Decimal, ROUND_HALF_UP

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