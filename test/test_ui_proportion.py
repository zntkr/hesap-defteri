import unittest
import tkinter as tk
import sys
import os

# Proje kök dizinini Python yoluna ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui.arayuz_tasarimi import MainUI

class TestUIProportionTool(unittest.TestCase):
    def setUp(self):
        """Her testten önce sanal bir pencere (Tk) oluşturulur."""
        self.root = tk.Tk()
        # Test sırasında pencerenin ekranda zıplayıp bizi rahatsız etmemesi için gizliyoruz
        self.root.withdraw() 
        
        # Ana arayüzü başlat
        self.app = MainUI(self.root)
        
        # MainUI içindeki orkestratörden (ToolsTab) Orantı aracını bul
        self.tool = self.app.main_view.frames["Orantı Hesaplayıcı"]

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
        self.assertEqual(sonuc_metni, "2250")
        
        # 4. Bilgi mesajının renginin ve metninin başarıyla güncellendiğini kontrol ediyoruz
        self.assertEqual(self.tool.info_lbl.cget("text"), "Hesaplandı • Kopyalamak için sonuca tıklayın")

if __name__ == '__main__':
    unittest.main()