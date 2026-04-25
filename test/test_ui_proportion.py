import unittest
import tkinter as tk
import sys
import os
from unittest.mock import patch

# Proje kök dizinini Python yoluna ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui.arayuz_tasarimi import MainUI
import core.dil as dil
from ui.proportion_tool import ProportionToolWidget

class TestUIProportionTool(unittest.TestCase):
    def setUp(self):
        """Her testten önce sanal bir pencere (Tk) oluşturulur."""
        self.root = tk.Tk()
        self.root.withdraw()

        # Kayıtlı dil tercihinden bağımsız, her ortamda Türkçe başlat
        with patch("core.ayarlar.load", return_value={"lang": "tr"}):
            self.app = MainUI(self.root)

        tool_widget = self.app.main_view.frames[dil.TR["prop_name"]]
        assert isinstance(tool_widget, ProportionToolWidget)
        self.tool = tool_widget

    def tearDown(self):
        """Her testten sonra pencereyi ve hafızayı temizler."""
        self.root.destroy()

    def test_arayuzden_oranti_hesaplama(self):
        """Kullanıcının kutulara değer girip butona basmasını simüle eder."""
        
        # 1. Kutulara veri giriyoruz (Kullanıcı klavyeden yazmış gibi)
        self.tool.prop_a_entry.delete(0, tk.END)
        self.tool.prop_a_entry.insert(0, "150")
        
        self.tool.prop_b_entry.delete(0, tk.END)
        self.tool.prop_b_entry.insert(0, "4.500")
        
        self.tool.prop_c_entry.delete(0, tk.END)
        self.tool.prop_c_entry.insert(0, "75")
        
        # 2. Enter'a basılmış veya Hesapla butonuna tıklanmış gibi fonksiyonu tetikliyoruz
        self.tool.calculate_proportion()
        
        # 3. Sonuç etiketinde (Label) doğru sayının yazıp yazmadığını (cget("text") ile) kontrol ediyoruz
        sonuc_metni = self.tool.prop_res_lbl.cget("text")
        self.assertEqual(sonuc_metni, "2.250")
        
        # 4. Bilgi mesajının renginin ve metninin başarıyla güncellendiğini kontrol ediyoruz
        assert self.tool.info_lbl is not None
        self.assertEqual(self.tool.info_lbl.cget("text"), "Hesaplandı • Kopyalamak için sonuca tıklayın")

if __name__ == '__main__':
    unittest.main()