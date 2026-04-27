import tkinter as tk

class RetroSunkenMechanicalButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=130, height=130, **kwargs):
        # Arka planı koyu yapalım ki klavye kasası öne çıksın
        super().__init__(parent, width=width, height=height, bg="#1A1A1A", highlightthickness=0, **kwargs)
        self.command = command
        self.text = text
        self.W, self.H = width, height
        
        # --- Renk Paleti ---
        # 1. Klavye Kasası (Sabit çerçeve - Retro bej/gri)
        self.color_chassis_base = "#D9D9D9" # Ana kasa rengi
        self.color_well_shadow = "#404040"  # Yuvanın iç gölgesi (derinlik)
        self.color_well_highlight = "#FFFFFF" # Yuvanın ışık gören kenarı

        # 2. Keycap (Mekanik Tuş - Şeffaf Kırmızı)
        self.color_key_cap_top = "#e60000"     # Tuşun üst yüzeyi
        self.color_key_side_shadow = "#8b0000" # Tuşun yan gölgesi (koyu kırmızı)
        self.color_inner_stem = "#990000"      # Şeffaflık illüzyonu için iç parça
        
        # 3. Dinamik Parlama
        self.color_glare_normal = "#ffcccc"
        self.color_glare_pressed = "#ff9999"

        self.pressed = False
        self.draw_button()
        
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)

    def draw_button(self, offset=0):
        self.delete("all")
        W, H = self.W, self.H
        
        # --- 1. STATİK BÖLÜM: Klavye Kasası ve Yuva (Well) ---
        # Bu kısım hiç hareket etmez, "sunken" hissini bu verir.
        
        # Kasa tabanı
        self.create_rectangle(0, 0, W, H, fill=self.color_chassis_base, outline="")
        
        # Tuşun gireceği yuvanın (Well) koordinatları
        w_x1, w_y1 = 15, 15
        w_x2, w_y2 = 115, 115
        
        # Yuvanın içine derinlik gölgeleri çizelim (Üst ve Sol kenar koyu)
        self.create_line(w_x1, w_y1, w_x2, w_y1, fill=self.color_well_shadow, width=2) # Üst iç
        self.create_line(w_x1, w_y1, w_x1, w_y2, fill=self.color_well_shadow, width=2) # Sol iç
        # Yuvanın alt ve sağ kenarına hafif ışık (vurgu)
        self.create_line(w_x1, w_y2, w_x2, w_y2, fill=self.color_well_highlight, width=1) # Alt iç
        self.create_line(w_x2, w_y1, w_x2, w_y2, fill=self.color_well_highlight, width=1) # Sağ iç

        # --- 2. DİNAMİK BÖLÜM: Keycap (Mekanik Tuş) ---
        # Bu koordinatlar offset'e göre değişir ve tuşun yuva içinde hareketini sağlar.
        
        # Tuşun yuva içindeki taban koordinatları (Poligonların bağlandığı sabit noktalar)
        # Yuvanın (Well) hemen içinden başlarlar.
        k_base_x1, k_base_y1 = 20, 20
        k_base_x2, k_base_y2 = 110, 110
        
        # Tuşun hareket eden üst yüzey koordinatları (CY offset ile değişir)
        k_top_x1, k_top_y1 = 30, 25 + offset
        k_top_x2, k_top_y2 = 100, 95 + offset

        # -- A. Tuşun Yan Duvarları (3D Eğim) --
        # Üst eğim
        self.create_polygon(k_base_x1, k_base_y1, k_base_x2, k_base_y1, k_top_x2, k_top_y1, k_top_x1, k_top_y1, fill=self.color_key_cap_top, outline="")
        # Alt eğim (Gölge - Basılınca küçülür, sunken hissi verir)
        self.create_polygon(k_base_x1, k_base_y2, k_base_x2, k_base_y2, k_top_x2, k_top_y2, k_top_x1, k_top_y2, fill=self.color_key_side_shadow, outline="")
        # Sol eğim
        self.create_polygon(k_base_x1, k_base_y1, k_base_x1, k_base_y2, k_top_x1, k_top_y2, k_top_x1, k_top_y1, fill=self.color_key_side_shadow, outline="")
        # Sağ eğim
        self.create_polygon(k_base_x2, k_base_y1, k_base_x2, k_base_y2, k_top_x2, k_top_y2, k_top_x2, k_top_y1, fill=self.color_key_side_shadow, outline="")

        # -- B. Tuşun Üst Yüzeyi (Şeffaf Kapak) --
        self.create_rectangle(k_top_x1, k_top_y1, k_top_x2, k_top_y2, fill=self.color_key_cap_top, outline="")
        
        # -- C. Şeffaflık İllüzyonu (İç Parça) --
        self.create_rectangle(k_top_x1 + 10, k_top_y1 + 10, k_top_x2 - 10, k_top_y2 - 10, fill=self.color_inner_stem, outline="")
        
        # -- D. Dinamik Parlama (Köşe Işığı) --
        glare_size = 18
        if offset == 0:
            # NORMAL: Sol Üstte parlak
            self.create_polygon(k_top_x1, k_top_y1, k_top_x1 + glare_size, k_top_y1, k_top_x1, k_top_y1 + glare_size, fill=self.color_glare_normal, outline="")
        else:
            # PRESSED: Sağ Alta taşı ve sönükleştir
            self.create_polygon(k_top_x2, k_top_y2, k_top_x2 - glare_size, k_top_y2, k_top_x2, k_top_y2 - glare_size, fill=self.color_glare_pressed, outline="")
        
        # -- E. Yazı --
        text_y = (k_top_y1 + k_top_y2) // 2
        # Tuş çöktüğünde yazı da hafif sönükleşsin
        text_color = "white" if offset == 0 else "#DCDCDC"
        self.create_text(65, text_y, text=self.text, fill=text_color, font=("Courier", 18, "bold"))

    def on_press(self, event):
        self.pressed = True
        # Tuşu yuvanın içine 10 piksel çökert
        self.draw_button(offset=10) 

    def on_release(self, event):
        if self.pressed:
            self.pressed = False
            self.draw_button(offset=0)
            if self.command:
                self.command()

# --- Test Ekranı ---
root = tk.Tk()
root.title("Sunken Retro Button")
root.geometry("300x300")
root.configure(bg="#1A1A1A") # Koyu arka plan

# Özel sunken butonumuzu ekliyoruz
btn = RetroSunkenMechanicalButton(root, text="PUSH")
btn.pack(expand=True)

root.mainloop()