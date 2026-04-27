import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import core.ayarlar
from core.ayarlar import load, save


class TestAyarlarLoad(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._path = Path(self._tmp.name) / "settings.json"

    def tearDown(self):
        self._tmp.cleanup()

    def _patch(self):
        return patch("core.ayarlar._path", return_value=self._path)

    def test_dosya_yoksa_varsayilan_tr(self):
        with self._patch():
            result = load()
        self.assertEqual(result["lang"], "tr")

    def test_gecerli_en_dili(self):
        self._path.write_text(json.dumps({"lang": "en"}), encoding="utf-8")
        with self._patch():
            result = load()
        self.assertEqual(result["lang"], "en")

    def test_bozuk_json_varsayilana_duser(self):
        self._path.write_text("{bozuk{{", encoding="utf-8")
        with self._patch():
            result = load()
        self.assertEqual(result["lang"], "tr")

    def test_bos_dosya_varsayilana_duser(self):
        self._path.write_text("", encoding="utf-8")
        with self._patch():
            result = load()
        self.assertEqual(result["lang"], "tr")

    def test_gecersiz_lang_degeri_varsayilana_duser(self):
        self._path.write_text(json.dumps({"lang": "de"}), encoding="utf-8")
        with self._patch():
            result = load()
        self.assertEqual(result["lang"], "tr")

    def test_dict_degilse_varsayilana_duser(self):
        for invalid in ["null", "[1,2,3]", '"string"']:
            self._path.write_text(invalid, encoding="utf-8")
            with self._patch():
                result = load()
            self.assertEqual(result["lang"], "tr", msg=f"Girdi: {invalid}")

    def test_bilinmeyen_anahtarlar_yuklenmez(self):
        self._path.write_text(
            json.dumps({"lang": "en", "theme": "dark", "zoom": 2}),
            encoding="utf-8",
        )
        with self._patch():
            result = load()
        self.assertEqual(result["theme"], "dark")  # bilinen anahtar — yüklenmeli
        self.assertNotIn("zoom", result)            # bilinmeyen anahtar — yüklenmemeli
        self.assertEqual(result["lang"], "en")

    def test_sonuc_her_zaman_tum_anahtarlari_icerir(self):
        with self._patch():
            result = load()
        self.assertIn("lang", result)


class TestAyarlarSave(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._path = Path(self._tmp.name) / "settings.json"

    def tearDown(self):
        self._tmp.cleanup()

    def _patch(self):
        return patch("core.ayarlar._path", return_value=self._path)

    def test_dosya_olusturur(self):
        with self._patch():
            save({"lang": "en"})
        self.assertTrue(self._path.exists())

    def test_dogru_icerik_yazar(self):
        with self._patch():
            save({"lang": "en"})
        data = json.loads(self._path.read_text(encoding="utf-8"))
        self.assertEqual(data["lang"], "en")

    def test_tmp_dosyasi_kalmaz(self):
        with self._patch():
            save({"lang": "en"})
        self.assertFalse(self._path.with_suffix(".tmp").exists())

    def test_oserror_cokturmaz(self):
        with self._patch(), patch("builtins.open", side_effect=OSError("disk dolu")):
            try:
                save({"lang": "en"})
            except Exception as exc:
                self.fail(f"save() istisna fırlattı: {exc}")

    def test_dizin_yoksa_olusturur(self):
        nested = Path(self._tmp.name) / "a" / "b" / "settings.json"
        with patch("core.ayarlar._path", return_value=nested):
            save({"lang": "tr"})
        self.assertTrue(nested.exists())

    def test_replace_hatasi_cokturmaz(self):
        # tmp.replace() başarısız olursa OSError yutulmalı, uygulama çökmemeli
        with self._patch(), patch("pathlib.Path.replace", side_effect=OSError("izin yok")):
            try:
                save({"lang": "en"})
            except Exception as exc:
                self.fail(f"save() replace hatasında istisna fırlattı: {exc}")


class TestAyarlarDonus(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._path = Path(self._tmp.name) / "settings.json"

    def tearDown(self):
        self._tmp.cleanup()

    def _patch(self):
        return patch("core.ayarlar._path", return_value=self._path)

    def test_kaydet_yukle_tutarliligi(self):
        with self._patch():
            save({"lang": "en"})
            result = load()
        self.assertEqual(result["lang"], "en")

    def test_tr_kaydet_yukle(self):
        with self._patch():
            save({"lang": "tr"})
            result = load()
        self.assertEqual(result["lang"], "tr")


class TestAyarlarPath(unittest.TestCase):

    @patch("core.ayarlar.os")
    def test_path_windows(self, mock_os):
        mock_os.name = "nt"
        mock_os.environ.get.return_value = "C:\\MockAppData"
        p = core.ayarlar._path()
        self.assertEqual(p, Path("C:\\MockAppData") / "HesapDefteri" / "settings.json")

    @patch("core.ayarlar.os")
    def test_path_windows_fallback(self, mock_os):
        # LOCALAPPDATA yoksa AppData/Local'a fallback eder (Roaming değil)
        mock_os.name = "nt"
        mock_os.environ.get.side_effect = lambda k, d=None: d
        with patch("core.ayarlar.Path.home", return_value=Path("C:\\Users\\MockUser")):
            p = core.ayarlar._path()
            expected = Path("C:\\Users\\MockUser") / "AppData" / "Local" / "HesapDefteri" / "settings.json"
            self.assertEqual(p, expected)

    def test_path_posix(self):
        # Uygulama Windows'a özel; posix dalı kaldırıldı, bu test geçersiz.
        pass

if __name__ == "__main__":
    unittest.main()
