from typing import Dict, Any, List, Tuple

TR: Dict[str, Any] = {
    # App
    "app_name": "Hesap Defteri",
    "date_placeholder": "GG/AA/YYYY",
    "placeholder_text": "Sayıları yazın veya yapıştırın...",

    # Menu - File
    "menu_file": "Dosya",
    "menu_exit": "Çıkış",

    # Menu - Edit
    "menu_edit": "Düzenle",
    "menu_cut": "Kes",
    "menu_copy": "Kopyala",
    "menu_paste": "Yapıştır",
    "menu_select_all": "Tümünü Seç",
    "menu_clear_all": "Tümünü Temizle",

    # Menu - Tools
    "menu_tools": "Araçlar",

    # Menu - View
    "menu_view": "Görünüş",
    "menu_always_on_top": "Her Zaman Üstte Tut",
    "menu_show_tape": "Hesap Şeridini Göster",
    "menu_scale": "Ölçek",
    "menu_theme": "Tema",
    "menu_theme_light": "Açık",
    "menu_theme_dark": "Koyu",

    # Menu - Language
    "menu_language": "Dil",
    "lang_tr": "Türkçe",
    "lang_en": "İngilizce",

    # Menu - Help
    "menu_help": "Yardım",
    "menu_guide": "Kullanma Rehberi",
    "menu_about": "Hakkında",

    # Tape
    "tape_header": "HESAP ŞERİDİ",
    "tape_copy_btn": "Kopyala",
    "tape_clear_btn": "Temizle",
    "tape_result_label": "Sonuç",

    # About dialog
    "about_title": "Hakkında",
    "about_copyright": "Telif Hakkı © {year} | MIT Lisansı\nSıfır bloatware, maksimum odak.",
    "about_ok": "TAMAM",

    # Guide dialog
    "guide_title": "Kullanma Rehberi",
    "guide_heading": "KULLANMA KILAVUZU",
    "guide_ok": "TAMAM",
    "guide_content": [
        ("ÖZELLİKLER\n", "header"),
        ("• ", "bullet"), ("Akıllı Veri Girişi: ", "highlight"), ("Metinleri yapıştırın, sayılar otomatik ayıklanır.\n", "list_item"),
        ("• ", "bullet"), ("Agnostik Format: ", "highlight"), ("TR (1.500,50) ve US (1,500.50) aynı anda tanınır.\n", "list_item"),
        ("• ", "bullet"), ("Hızlı Kopyalama: ", "highlight"), ("Sonuçlara tıklayarak anında panoya kopyalayın.\n", "list_item"),
        ("KISAYOLLAR\n", "header"),
        (" Enter ", "key"), ("\tHesapla\n", "shortcut"),
        (" Esc ", "key"), ("\tTemizle\n", "shortcut"),
        (" Ctrl + Tab ", "key"), ("\tSekme değiştir\n", "shortcut"),
        (" Ctrl + 1..6 ", "key"), ("\tAraçlara git\n", "shortcut"),
        (" Ctrl + H ", "key"), ("\tHesap şeridi\n", "shortcut"),
        (" Sağ Tık ", "key"), ("\tİçerik menüsü\n", "shortcut"),
    ],

    # Base tool
    "msg_calculated": "Hesaplandı • Kopyalamak için sonuca tıklayın",
    "msg_copied": "Kopyalandı!",
    "btn_calculate": "HESAPLA",
    "btn_clear": "Temizle",

    # Average tool
    "avg_short": "ORTALAMA",
    "avg_name": "Ortalama Hesaplayıcı",
    "avg_desc": "Bir metinde bulunan sayıları ayıklayıp ortalamasını ve istatistiklerini hesaplar.",
    "avg_label_avg": "Ortalama:",
    "avg_label_sum": "Toplam:",
    "avg_stat_count": "VERİ ADEDİ:",
    "avg_stat_median": "MEDYAN:",
    "avg_stat_max": "EN BÜYÜK:",
    "avg_stat_range": "FARK:",
    "avg_stat_min": "EN KÜÇÜK:",
    "avg_stat_std": "STD.SAPMA:",
    "avg_info_default": "Sayıları yapıştırıp Enter'a basın",
    "avg_info_limit": "Limit aşıldı! En fazla 5.000 karakter girilebilir.",
    "avg_info_truncated": "Metin çok uzundu, 5.000 karaktere kırpılarak yapıştırıldı.",
    "avg_info_result": "{count} sayı hesaplandı • Kopyalamak için rakama tıklayın",
    "avg_info_error": "Sayı bulunamadı veya geçersiz veri girişi!",
    "avg_char_warning": "Son {n} karakter",
    "avg_char_over": "Limit aşıldı: {n} karakter silin",
    "avg_tape_title": "ORTALAMA HESABI",
    "avg_tape_count": "Adet",
    "avg_tape_sum": "Toplam",

    # Tax tool
    "tax_short": "KDV",
    "tax_name": "KDV Hesaplayıcı",
    "tax_desc": "Örn: 1.500 TL tutar ve %20 oran girerek KDV payını ve toplam matrahı hesaplayabilirsiniz.",
    "tax_label_amount": "Tutar:",
    "tax_label_rate": "Oran (%):",
    "tax_label_gross": "Ham Tutar:",
    "tax_label_vat": "KDV Tutarı:",
    "tax_label_total": "Toplam Tutar:",
    "tax_info_default": "KDV hesaplamak için tutarı girin",
    "tax_info_error": "Geçersiz veya eksik değer!",
    "tax_info_err_amount": "Tutar eksik!",
    "tax_info_err_rate": "KDV Oranı eksik!",
    "tax_info_ok": "KDV hesaplandı",
    "tax_tape_title": "KDV HESABI",
    "tax_tape_amount": "Tutar",
    "tax_tape_rate": "Oran",

    # Discount tool
    "disc_short": "İSKONTO",
    "disc_name": "İndirim Hesaplayıcı",
    "disc_desc": "Örn: 2.500 TL'lik bir malın %15 indirim yapıldığında indirimli fiyatını ve indirim miktarını hesaplar.",
    "disc_label_amount": "Tutar:",
    "disc_label_rate": "İndirim (%):",
    "disc_label_price": "Fiyat:",
    "disc_label_discount": "İndirim Miktarı:",
    "disc_label_net": "İndirimli Fiyat:",
    "disc_info_default": "İndirim hesaplamak için tutarı girin",
    "disc_info_error": "Geçersiz veya eksik değer!",
    "disc_info_err_amount": "Tutar eksik!",
    "disc_info_err_rate": "İndirim Oranı eksik!",
    "disc_info_ok": "İndirim hesaplandı",
    "disc_tape_title": "İNDİRİM HESABI",
    "disc_tape_amount": "Tutar",
    "disc_tape_rate": "İndirim",

    # Change tool
    "chng_short": "DEĞİŞME",
    "chng_name": "Değişiklik Hesaplayıcı",
    "chng_desc": "Örn: Eski fiyatı 150 TL, yeni fiyatı 200 TL olan bir malın yüzde kaç zamlandığını hesaplar.",
    "chng_label_old": "Eski Değer:",
    "chng_label_new": "Yeni Değer:",
    "chng_label_rate": "Değişiklik Oranı:",
    "chng_info_default": "Artış veya azalışı görmek için değerleri girin",
    "chng_info_error": "Geçersiz veya eksik değer!",
    "chng_info_err_old": "Eski değer eksik!",
    "chng_info_err_new": "Yeni değer eksik!",
    "chng_tape_title": "DEĞİŞME HESABI",
    "chng_tape_old": "Eski",
    "chng_tape_new": "Yeni",

    # Proportion tool
    "prop_short": "ORANTI",
    "prop_name": "Orantı Hesaplayıcı",
    "prop_desc": "Örn: 150 adet mal 4.500 TL ise, 75 adet mal kaç TL yapar?",
    "prop_label_a": "1. Değer (A):",
    "prop_label_b": "Karşılığı (B):",
    "prop_label_c": "3. Değer (C):",
    "prop_label_result": "Netice (X):",
    "prop_info_default": "Orantı sonucunu görmek için değerleri girin",
    "prop_info_error_missing": "Lütfen üç değeri de eksiksiz girin!",
    "prop_info_err_a": "1. Değer (A) eksik!",
    "prop_info_err_b": "Karşılığı (B) eksik!",
    "prop_info_err_c": "3. Değer (C) eksik!",
    "prop_info_error_zero": "1. Değer (A) sıfır olamaz!",
    "prop_tape_title": "ORANTI HESABI",

    # Age tool
    "age_short": "YAŞ",
    "age_name": "Yaş Hesaplayıcı",
    "age_desc": "Doğum tarihinizi girerek doğduğunuz günü, tam yaşınızı ve kalan süreyi bulun.",
    "age_label_dob": "GG/AA/YYYY:",
    "age_info_default": "Doğum tarihinizi GG/AA/YYYY formatında girin ve Enter'a basın",
    "age_info_error_empty": "Lütfen doğum tarihinizi girin!",
    "age_info_error_future": "Gelecek bir tarih giremezsiniz!",
    "age_info_error_format": "Geçersiz format! Örn: 15/05/1990",
    "age_info_ok": "Hesaplandı • Kopyalamak için cevaba tıklayın",
    "age_tape_title": "YAŞ HESABI",
    "age_tape_born_label": "Doğum",
    "age_tape_years": "Yıl",
    "age_tape_months": "Ay",
    # Age result text segments (interleaved with bold values)
    "age_res_prefix": "• Yaşınız: ",
    "age_res_years": " yıl, ",
    "age_res_months": " ay, ",
    "age_res_days_section": " gün\n\n• Gün Alma: ",
    "age_res_completed": " yaş bitti, ",
    "age_res_taking": " yaşından gün alıyorsunuz.\n\n• Doğduğunuz Gün: ",
    "age_res_next_bd": "\n\n• Sonraki Doğum Günü: ",
    "age_res_today_bd": "Bugün Doğum Gününüz! 🎂",
    "age_res_days_left": " gün kaldı",
    "age_res_lived": "\n\n• Yaşanan Gün: Toplam ",
    "age_res_lived_end": " gün.",
}

EN: Dict[str, Any] = {
    # App
    "app_name": "Account Book",
    "date_placeholder": "DD/MM/YYYY",
    "placeholder_text": "Type or paste numbers...",

    # Menu - File
    "menu_file": "File",
    "menu_exit": "Exit",

    # Menu - Edit
    "menu_edit": "Edit",
    "menu_cut": "Cut",
    "menu_copy": "Copy",
    "menu_paste": "Paste",
    "menu_select_all": "Select All",
    "menu_clear_all": "Clear All",

    # Menu - Tools
    "menu_tools": "Tools",

    # Menu - View
    "menu_view": "View",
    "menu_always_on_top": "Always on Top",
    "menu_show_tape": "Show Receipt Tape",
    "menu_scale": "Scale",
    "menu_theme": "Theme",
    "menu_theme_light": "Light",
    "menu_theme_dark": "Dark",

    # Menu - Language
    "menu_language": "Language",
    "lang_tr": "Turkish",
    "lang_en": "English",

    # Menu - Help
    "menu_help": "Help",
    "menu_guide": "User Guide",
    "menu_about": "About",

    # Tape
    "tape_header": "RECEIPT TAPE",
    "tape_copy_btn": "Copy",
    "tape_clear_btn": "Clear",
    "tape_result_label": "Result",

    # About dialog
    "about_title": "About",
    "about_copyright": "Copyright © {year} | MIT License\nZero bloatware, maximum focus.",
    "about_ok": "OK",

    # Guide dialog
    "guide_title": "User Guide",
    "guide_heading": "USER GUIDE",
    "guide_ok": "OK",
    "guide_content": [
        ("FEATURES\n", "header"),
        ("• ", "bullet"), ("Smart Paste: ", "highlight"), ("Paste text, numbers are extracted automatically.\n", "list_item"),
        ("• ", "bullet"), ("Format Agnostic: ", "highlight"), ("US (1,500.50) & EU (1.500,50) recognized together.\n", "list_item"),
        ("• ", "bullet"), ("Quick Copy: ", "highlight"), ("Click any result to instantly copy to clipboard.\n", "list_item"),
        ("SHORTCUTS\n", "header"),
        (" Enter ", "key"), ("\tCalculate\n", "shortcut"),
        (" Esc ", "key"), ("\tClear data\n", "shortcut"),
        (" Ctrl + Tab ", "key"), ("\tCycle tabs\n", "shortcut"),
        (" Ctrl + 1..6 ", "key"), ("\tJump to tool\n", "shortcut"),
        (" Ctrl + H ", "key"), ("\tToggle tape\n", "shortcut"),
        (" Right Click ", "key"), ("\tContext menu\n", "shortcut"),
    ],

    # Base tool
    "msg_calculated": "Calculated • Click result to copy",
    "msg_copied": "Copied!",
    "btn_calculate": "CALCULATE",
    "btn_clear": "Clear",

    # Average tool
    "avg_short": "AVERAGE",
    "avg_name": "Average Calculator",
    "avg_desc": "Extracts numbers from text and calculates their average and statistics. Paste numbers into the box below.",
    "avg_label_avg": "Average:",
    "avg_label_sum": "Total:",
    "avg_stat_count": "COUNT:",
    "avg_stat_median": "MEDIAN:",
    "avg_stat_max": "MAX:",
    "avg_stat_range": "RANGE:",
    "avg_stat_min": "MIN:",
    "avg_stat_std": "STD. DEV:",
    "avg_info_default": "Paste numbers and press Enter",
    "avg_info_limit": "Limit exceeded! Max 5,000 characters allowed.",
    "avg_info_truncated": "Text was too long, truncated to 5,000 characters.",
    "avg_info_result": "{count} numbers calculated • Click a value to copy",
    "avg_info_error": "No numbers found or invalid input!",
    "avg_char_warning": "{n} chars left",
    "avg_char_over": "Limit exceeded: delete {n} chars",
    "avg_tape_title": "AVERAGE CALC",
    "avg_tape_count": "Count",
    "avg_tape_sum": "Total",

    # Tax tool
    "tax_short": "VAT",
    "tax_name": "VAT Calculator",
    "tax_desc": "Ex: Enter amount 1,500 and rate 20% to calculate the VAT and total.",
    "tax_label_amount": "Amount:",
    "tax_label_rate": "Rate (%):",
    "tax_label_gross": "Gross Amount:",
    "tax_label_vat": "VAT Amount:",
    "tax_label_total": "Total Amount:",
    "tax_info_default": "Enter amount to calculate VAT",
    "tax_info_error": "Invalid or missing value!",
    "tax_info_err_amount": "Amount is missing!",
    "tax_info_err_rate": "VAT Rate is missing!",
    "tax_info_ok": "VAT calculated",
    "tax_tape_title": "VAT CALC",
    "tax_tape_amount": "Amount",
    "tax_tape_rate": "Rate",

    # Discount tool
    "disc_short": "DISCOUNT",
    "disc_name": "Discount Calculator",
    "disc_desc": "Ex: Calculate the discounted price and discount amount for a 2,500 item at 15% off.",
    "disc_label_amount": "Amount:",
    "disc_label_rate": "Discount (%):",
    "disc_label_price": "Price:",
    "disc_label_discount": "Discount Amount:",
    "disc_label_net": "Discounted Price:",
    "disc_info_default": "Enter amount to calculate discount",
    "disc_info_error": "Invalid or missing value!",
    "disc_info_err_amount": "Amount is missing!",
    "disc_info_err_rate": "Discount Rate is missing!",
    "disc_info_ok": "Discount calculated",
    "disc_tape_title": "DISCOUNT CALC",
    "disc_tape_amount": "Amount",
    "disc_tape_rate": "Discount",

    # Change tool
    "chng_short": "CHANGE",
    "chng_name": "Change Calculator",
    "chng_desc": "Ex: Calculate the percentage change from old price 150 to new price 200.",
    "chng_label_old": "Old Value:",
    "chng_label_new": "New Value:",
    "chng_label_rate": "Change Rate:",
    "chng_info_default": "Enter values to see increase/decrease",
    "chng_info_error": "Invalid or missing value!",
    "chng_info_err_old": "Old value is missing!",
    "chng_info_err_new": "New value is missing!",
    "chng_tape_title": "CHANGE CALC",
    "chng_tape_old": "Old",
    "chng_tape_new": "New",

    # Proportion tool
    "prop_short": "RATIO",
    "prop_name": "Proportion Calculator",
    "prop_desc": "Ex: If 150 items cost 4,500, how much do 75 items cost?",
    "prop_label_a": "1st Value (A):",
    "prop_label_b": "Equivalent (B):",
    "prop_label_c": "3rd Value (C):",
    "prop_label_result": "Result (X):",
    "prop_info_default": "Enter values to see proportion result",
    "prop_info_error_missing": "Please enter all three values!",
    "prop_info_err_a": "1st Value (A) is missing!",
    "prop_info_err_b": "Equivalent (B) is missing!",
    "prop_info_err_c": "3rd Value (C) is missing!",
    "prop_info_error_zero": "1st Value (A) cannot be zero!",
    "prop_tape_title": "PROPORTION CALC",

    # Age tool
    "age_short": "AGE",
    "age_name": "Age Calculator",
    "age_desc": "Enter your birth date to find your birth day, exact age, and time remaining.",
    "age_label_dob": "DD/MM/YYYY:",
    "age_info_default": "Enter your birth date in DD/MM/YYYY format and press Enter",
    "age_info_error_empty": "Please enter your birth date!",
    "age_info_error_future": "You cannot enter a future date!",
    "age_info_error_format": "Invalid format! Ex: 15/05/1990",
    "age_info_ok": "Calculated • Click answer to copy",
    "age_tape_title": "AGE CALC",
    "age_tape_born_label": "Born",
    "age_tape_years": "Years",
    "age_tape_months": "Months",
    # Age result text segments (interleaved with bold values)
    "age_res_prefix": "• Your Age: ",
    "age_res_years": " years, ",
    "age_res_months": " months, ",
    "age_res_days_section": " days\n\n• Milestone: ",
    "age_res_completed": " years completed, progressing through ",
    "age_res_taking": ".\n\n• Born on: ",
    "age_res_next_bd": "\n\n• Next Birthday: ",
    "age_res_today_bd": "Today is your Birthday! 🎂",
    "age_res_days_left": " days left",
    "age_res_lived": "\n\n• Days Lived: A total of ",
    "age_res_lived_end": " days.",
}

LANGS: Dict[str, Dict[str, Any]] = {"tr": TR, "en": EN}
