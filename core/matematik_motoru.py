import re
import statistics
import math
from typing import List, Dict, Optional, Union, Any

class MatematikMotoru:
    """
    Stateless (durumsuz) veri analiz ve regex ayıklama motoru.
    Metin içindeki sayıları format (US/TR) bağımsız olarak bulur ve istatistiklerini hesaplar.
    """

    SAYI_PATERNI = r"[-+]?(?:\d{1,3}(?:[.,]\d{3})+(?:[.,]\d+)?|\d+(?:[.,]\d+)?|[.,]\d+)"

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
        eslesmeler = re.findall(MatematikMotoru.SAYI_PATERNI, metin)
        
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
                if temiz_s.count(',') > 1 or len(temiz_s) - son_virgul == 4:   # Örn: 1,500,000 veya 1,000 (Sadece binlik US)
                    temiz_s = temiz_s.replace(',', '') 
                else:                        # Örn: 15,5 (Standart TR ondalık)
                    temiz_s = temiz_s.replace(',', '.') 
            # Sadece nokta varsa
            elif son_nokta != -1:
                if temiz_s.count('.') > 1 or len(temiz_s) - son_nokta == 4:   # Örn: 1.500.000 veya 1.000 (Sadece binlik TR)
                    temiz_s = temiz_s.replace('.', '')
                # Tek nokta varsa ve sonrasında 3 rakam yoksa standart float formatıdır (15.5), dokunmuyoruz.
                
            try:
                sayilar.append(isaret * float(temiz_s))
            except ValueError:
                continue
                
        return sayilar

    @staticmethod
    def _temiz_sayi(deger: float) -> Union[float, int]:
        """Kayan nokta hassasiyetini (IEEE 754) düzeltir ve .0 fazlalığını atar.
        Veri kaybını (büyük sayılarda :g truncating) önlemek için 4 basamak yuvarlama kullanılır."""
        if math.isinf(deger) or math.isnan(deger):
            return deger
        v = round(deger, 4)
        return int(v) if v.is_integer() else v

    @staticmethod
    def detayli_analiz_yap(sayi_listesi: List[Union[float, int]]) -> Optional[Dict[str, Any]]:
        """
        Verilen sayı listesi üzerinden temel ve ileri düzey istatistiksel hesaplamaları yapar.
        
        Args:
            sayi_listesi (List[Union[float, int]]): Analiz edilecek sayıların listesi.
            
        Returns:
            Optional[Dict[str, Any]]: Hesaplanmış istatistikleri içeren sözlük. 
            Liste boşsa None döner.
        """
        if not sayi_listesi:
            return None
        
        # Temel İstatistikler
        analiz = {
            "sayilar": [MatematikMotoru._temiz_sayi(s) for s in sayi_listesi],
            "ortalama": MatematikMotoru._temiz_sayi(sum(sayi_listesi) / len(sayi_listesi)),
            "adet": len(sayi_listesi),
            "en_buyuk": MatematikMotoru._temiz_sayi(max(sayi_listesi)),
            "en_kucuk": MatematikMotoru._temiz_sayi(min(sayi_listesi)),
            "medyan": MatematikMotoru._temiz_sayi(statistics.median(sayi_listesi)),
            "toplam": MatematikMotoru._temiz_sayi(sum(sayi_listesi)),
            "aciklik": MatematikMotoru._temiz_sayi(max(sayi_listesi) - min(sayi_listesi)),
            "std_sapma": MatematikMotoru._temiz_sayi(statistics.stdev(sayi_listesi)) if len(sayi_listesi) > 1 else 0
        }
        return analiz