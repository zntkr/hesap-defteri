import re
import statistics
from typing import List, Dict, Optional, Union

class MatematikMotoru:
    """
    Stateless (durumsuz) veri analiz ve regex ayıklama motoru.
    Metin içindeki sayıları format (US/TR) bağımsız olarak bulur ve istatistiklerini hesaplar.
    """

    @staticmethod
    def metinden_sayilari_ayikla(metin: str) -> List[float]:
        """
        Karmaşık metin içerisinden US ve TR formatlı sayıları agnostik olarak ayıklar.
        
        Args:
            metin (str): İçinden sayı ayıklanacak ham metin.
            
        Returns:
            List[float]: Ayıklanmış ve float tipine dönüştürülmüş sayılar listesi.
        """
        # 1. Grup: 1,500,000.50 veya 1.500.000,50 gibi binlik ayırıcılı formatlar
        # 2. Grup: 15.5 veya 15,5 gibi standart ondalıklı tam sayılar
        # 3. Grup: .5 veya ,5 gibi doğrudan ondalıkla başlayanlar
        patern = r"[-+]?(?:\d{1,3}(?:[.,]\d{3})+(?:[.,]\d+)?|\d+(?:[.,]\d+)?|[.,]\d+)"
        eslesmeler = re.findall(patern, metin)
        
        sayilar = []
        for s in eslesmeler:
            isaret = -1 if s.startswith('-') else 1
            temiz_s = s.lstrip('+-')
            
            son_virgul = temiz_s.rfind(',')
            son_nokta = temiz_s.rfind('.')
            
            # İkisi de varsa: En sağdaki (en sondaki) her zaman ondalık ayırıcıdır!
            if son_virgul != -1 and son_nokta != -1:
                if son_virgul > son_nokta:   # Örn: 1.500.000,50 (TR Format)
                    temiz_s = temiz_s.replace('.', '').replace(',', '.')
                else:                        # Örn: 1,500,000.50 (US Format)
                    temiz_s = temiz_s.replace(',', '')
            # Sadece virgül varsa
            elif son_virgul != -1:
                if temiz_s.count(',') > 1:   # Örn: 1,500,000 (Sadece binlik US)
                    temiz_s = temiz_s.replace(',', '') 
                else:                        # Örn: 15,5 (Standart TR ondalık)
                    temiz_s = temiz_s.replace(',', '.') 
            # Sadece nokta varsa
            elif son_nokta != -1:
                if temiz_s.count('.') > 1:   # Örn: 1.500.000 (Sadece binlik TR)
                    temiz_s = temiz_s.replace('.', '')
                # Tek nokta varsa zaten standart float formatıdır (15.5), dokunmuyoruz.
                
            try:
                sayilar.append(isaret * float(temiz_s))
            except ValueError:
                continue
                
        return sayilar

    @staticmethod
    def _temiz_sayi(deger: float) -> Union[float, int]:
        """Kayan nokta hassasiyetini (IEEE 754) düzeltir ve .0 fazlalığını atar."""
        v = float(f"{deger:g}")
        return int(v) if v.is_integer() else v

    @staticmethod
    def detayli_analiz_yap(sayi_listesi: List[Union[float, int]]) -> Optional[Dict[str, Union[float, int]]]:
        """
        Verilen sayı listesi üzerinden temel ve ileri düzey istatistiksel hesaplamaları yapar.
        
        Args:
            sayi_listesi (List[Union[float, int]]): Analiz edilecek sayıların listesi.
            
        Returns:
            Optional[Dict[str, Union[float, int]]]: Hesaplanmış istatistikleri içeren sözlük. 
            Liste boşsa None döner.
        """
        if not sayi_listesi:
            return None
        
        # Temel İstatistikler
        analiz = {
            "ortalama": MatematikMotoru._temiz_sayi(sum(sayi_listesi) / len(sayi_listesi)),
            "adet": len(sayi_listesi),
            "en_buyuk": MatematikMotoru._temiz_sayi(max(sayi_listesi)),
            "en_kucuk": MatematikMotoru._temiz_sayi(min(sayi_listesi)),
            "medyan": MatematikMotoru._temiz_sayi(statistics.median(sayi_listesi)),
            "toplam": MatematikMotoru._temiz_sayi(sum(sayi_listesi)),
            "varyans": MatematikMotoru._temiz_sayi(statistics.variance(sayi_listesi)) if len(sayi_listesi) > 1 else 0,
            "std_sapma": MatematikMotoru._temiz_sayi(statistics.stdev(sayi_listesi)) if len(sayi_listesi) > 1 else 0
        }
        return analiz