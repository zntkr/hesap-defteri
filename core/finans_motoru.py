from typing import Dict, Union

class FinansMotoru:
    """
    Stateless (durumsuz) finans ve oran hesaplama motoru.
    KDV, yüzde hesaplamaları ve basit ticari araçları barındırır.
    """

    @staticmethod
    def _temiz_sayi(deger: float) -> Union[float, int]:
        """Finansal veriyi 2 basamağa yuvarlar ve gereksiz .0 küsuratını atar."""
        v = round(deger, 2)
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