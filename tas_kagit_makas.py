import tkinter as tk
from tkinter import messagebox
import random
import time
import pygame


# Ana pencere oluşturmaya yarar 
root = tk.Tk()
root.title("Taş, Kağıt, Makas Oyunu / Rock, Paper, Scissors Game")

# Ekran boyutunu tam ekran yapmaya yarar 
root.state('zoomed')

# Pygame'i başlatmaya yarar
pygame.mixer.init()


# Ses dosyalarını yüklemeye yarar
tas_hover_sesi = pygame.mixer.Sound("sounds/rock.wav")
tas_hover_sesi.set_volume(0.1)  # Ses seviyesi 1.0 ve 0.1 arasında olmalıdır

kagit_hover_sesi = pygame.mixer.Sound("sounds/paper.wav")
kagit_hover_sesi.set_volume(0.1)

makas_hover_sesi = pygame.mixer.Sound("sounds/scissors.wav")
makas_hover_sesi.set_volume(0.1)

turkce_hover_sesi = pygame.mixer.Sound("sounds/turkish.wav")
turkce_hover_sesi.set_volume(0.1)

english_hover_sesi = pygame.mixer.Sound("sounds/english.wav")
english_hover_sesi.set_volume(0.1)

click_hover_sesi = pygame.mixer.Sound("sounds/click.wav")
click_hover_sesi.set_volume(0.1)


# Ana pencere içi başlık için Label oluşturmaya yarar
header_label = tk.Label(root, text="Taş, Kağıt, Makas Oyunu / Rock, Paper, Scissors Game",font=('Arial', 24, 'bold'), pady=20)
header_label.pack()


# Butonların köşelerini ovalleştirmek için kullanılır
class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=100, height=50, cornerradius=25, color="#868561", **kwargs):
        tk.Canvas.__init__(self, parent, width=width, height=height, **kwargs)
        self.command = command
        self.cornerradius = cornerradius
        self.color = color
        self.text = text
        

        # Oval köşeleri oluşturmaya yarar 
        self.round_rectangle(0, 0, width, height, cornerradius, fill=color)

        # Buton metnini eklemeye yarar
        self.create_text(width/2, height/2, text=self.text, font=('Barlow ExtraBold', 24, 'bold'), fill='white')

        # Tıklanma olayını tanımlamaya yarar 
        self.bind("<ButtonPress-1>", self.on_click)

    def round_rectangle(self, x1, y1, x2, y2, r=1, **kwargs):
        points = [x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, 
                  y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)


    def on_click(self, event):
        if self.command:
            self.command()


# Önceki arayüzü temizlemeye yarar
def temizle_arayuz():
    for widget in root.winfo_children():
        widget.pack_forget()


def start_game():
    temizle_arayuz()  
    print("Oyun başladı!")
    secenekler_goster()


# Dil seçimi arayüzünü göstermeye yarar
def tas_kagit_makas_MUHSİNE_TAŞCI():
    global dil_label, turkce_btn, english_btn
    temizle_arayuz()

    dil_label = tk.Label(root, text="Lütfen dil seçin / Please choose a language:\n",font=('Barlow ExtraBold', 25, 'bold'), fg = '#5c340c')
    dil_label.pack(pady=20)

    def turkce_buton_hover(event):
        pygame.mixer.Sound.play(turkce_hover_sesi)

    def english_buton_hover(event):
        pygame.mixer.Sound.play(english_hover_sesi)

    turkce_btn = RoundedButton(root, text="Türkçe", command=lambda: dil_secimi('türkçe'), width=300, height=90, cornerradius=60, color='#7d0000')
    turkce_btn.bind("<Enter>", turkce_buton_hover)
    turkce_btn.pack(pady=10)

    english_btn = RoundedButton(root, text="English", command=lambda: dil_secimi('english'), width=300, height=90, cornerradius=60, color='#185853')
    english_btn.bind("<Enter>", english_buton_hover)
    english_btn.pack(pady=10)


def dil_secimi(dil):
    global secili_dil
    secili_dil = dil
    oyun_tanitimi()


# Oyun tanıtımını ekranda göstermeye yarar
def oyun_tanitimi():
    global geri_btn, tanitim_baslik_label, tanitim_icerik_label
    temizle_arayuz()

    if secili_dil == 'türkçe':
        tanitim_baslik = "Taş, Kağıt, Makas oyununa hoş geldiniz!\n"
        oyun_kurallari = "Oyun kuralları 📋:"
        tanitim_icerik = ("1. Taş, makası yener.         🪨    >    ✂️\n"
                         "2. Makas, kağıdı yener.  ✂️>    📜\n"
                         "3. Kağıt, taşı yener.            📜    >    🪨 \n"
                         "4. İlk iki turu kazanan oyunun galibi olur.\n"
                         "5. Oyunu başlatmak için taş, kağıt veya makas seçin.")
        
    elif secili_dil == 'english':
        tanitim_baslik = "Welcome to the Rock, Paper Scissors game!\n"
        oyun_kurallari = "Game rules 📋:"
        tanitim_icerik = ("1. Rock beats scissors.      🪨    >     ✂️\n"
                         "2. Scissors beat paper.    ✂️>     📜\n"
                         "3. Paper beats rock.             📜    >     🪨\n"
                         "4. The first to win two rounds wins the game.\n"
                         "5. Choose rock, paper, or scissors to start the game.")

    # tanitim_baslik bölümünü düzenlemeye yarar (yazı tipi, renk, boyut) 
    tanitim_baslik_label = tk.Label(root, text=tanitim_baslik, font=('Vineta BT', 35), fg = "#5c340c")
    tanitim_baslik_label.pack(pady=5)

    # oyun_kurallari bölümünü düzenleme yarar (yazı tipi, renk, boyut)
    oyun_kurallari_label = tk.Label(root, text=oyun_kurallari, font=('Barlow ExtraBold', 22), fg = "#5d4936")
    oyun_kurallari_label.pack(pady=5)

    # tanitim_icerik bölümünü düzenleme yarar (yazı tipi, hizalama, renk, boyut)
    tanitim_icerik_label = tk.Label(root, text=tanitim_icerik, font=('Barlow ExtraBold', 20), anchor='w', justify='left', fg= "#5d4936") 
    tanitim_icerik_label.pack(pady=10, padx=20) 


    def click_buton_hover(event):
        pygame.mixer.Sound.play(click_hover_sesi)

    # Geri butonunu eklemeye ve ses oynatmaya yarar
    geri_btn = RoundedButton(root, text="👈🏻 GERİ" if secili_dil == 'türkçe' else "👈🏻 BACK", command=tas_kagit_makas_MUHSİNE_TAŞCI, width=350, height=90, cornerradius=60, color='#787672')
    geri_btn.bind("<Enter>", click_buton_hover)
    geri_btn.pack(pady=10)

    # Oyuna Başla butonunu eklemeye ve ses oynatmaya yarar
    start_btn = RoundedButton(root, text="OYUNA BAŞLA 🎮" if secili_dil == 'türkçe' else "START GAME 🎮", command=start_game, width=350, height=90, cornerradius=60, color='#025e21')
    start_btn.bind("<Enter>", click_buton_hover)
    start_btn.pack(pady=10)


# Oyuncunun seçimini almaya yarar
def secenekler_goster():
    global secim_label, sonuc_label

    if secili_dil == 'türkçe':
        secenek_label_text = "Seçiminizi yapın"
    elif secili_dil == 'english':
        secenek_label_text = "Make your choice"

    secenek_label = tk.Label(root, text=secenek_label_text, font=('Barlow ExtraBold', 25, 'bold'), fg = "#5d4936") # Yazı tipi, boyut, stil ve renk
    secenek_label.pack(pady=10)

    def tas_buton_hover(event):
        pygame.mixer.Sound.play(tas_hover_sesi)

    def kagit_buton_hover(event):
        pygame.mixer.Sound.play(kagit_hover_sesi)

    def makas_buton_hover(event):
        pygame.mixer.Sound.play(makas_hover_sesi)

    if secili_dil == 'türkçe':
        tas_btn = RoundedButton(root, text="Taş 🪨", command=lambda: oyun_dongusu('taş'), width=300, height=90, cornerradius=60, color='#643219')
        kagit_btn = RoundedButton(root, text="Kağıt 📜", command=lambda: oyun_dongusu('kağıt'), width=300, height=90, cornerradius=60, color='#d8c8bc')
        makas_btn = RoundedButton(root, text="    Makas ✂️", command=lambda: oyun_dongusu('makas'), width=300, height=90, cornerradius=60, color='#918b80')
    elif secili_dil == 'english':
        tas_btn = RoundedButton(root, text="Rock 🪨", command=lambda: oyun_dongusu('rock'), width=300, height=90, cornerradius=60, color='#643219')
        kagit_btn = RoundedButton(root, text="Paper 📜", command=lambda: oyun_dongusu('paper'), width=300, height=90, cornerradius=60, color='#d8c8bc')
        makas_btn = RoundedButton(root, text="     Scissors ✂️", command=lambda: oyun_dongusu('scissors'), width=300, height=90, cornerradius=60, color='#918b80')

    # Sesleri çalmaya yarar
    tas_btn.bind("<Enter>", tas_buton_hover)
    tas_btn.pack(pady=10)

    kagit_btn.bind("<Enter>", kagit_buton_hover)
    kagit_btn.pack(pady=10)

    makas_btn.bind("<Enter>", makas_buton_hover)
    makas_btn.pack(pady=10)


    secim_label = tk.Label(root, text="")
    secim_label.pack(pady=10)

    sonuc_label = tk.Label(root, text="")
    sonuc_label.pack(pady=10)


# Bilgisayarın seçimini almaya yarar
def bilgisayar_secimi_al():
    if secili_dil == 'türkçe':
        secenekler = ['taş', 'kağıt', 'makas']
    elif secili_dil == 'english':
        secenekler = ['rock', 'paper', 'scissors']
    return random.choice(secenekler)


# Turu kimin kazandığını belirlemeye yarar
def tur_kazananini_belirle(kullanici_secimi, bilgisayar_secimi):
    if secili_dil == 'türkçe':
        if kullanici_secimi == bilgisayar_secimi:
            return "Berabere"
        elif (kullanici_secimi == 'taş' and bilgisayar_secimi == 'makas') or \
             (kullanici_secimi == 'kağıt' and bilgisayar_secimi == 'taş') or \
             (kullanici_secimi == 'makas' and bilgisayar_secimi == 'kağıt'):
            return "Kullanıcı"
        else:
            return "Bilgisayar"
    elif secili_dil == 'english':
        if kullanici_secimi == bilgisayar_secimi:
            return "Draw"
        elif (kullanici_secimi == 'rock' and bilgisayar_secimi == 'scissors') or \
             (kullanici_secimi == 'paper' and bilgisayar_secimi == 'rock') or \
             (kullanici_secimi == 'scissors' and bilgisayar_secimi == 'paper'):
            return "Player"
        else:
            return "Computer"

kullanici_galibiyetleri = 0
bilgisayar_galibiyetleri = 0


# Oyun döngüsü
def oyun_dongusu(kullanici_secimi):
    global kullanici_galibiyetleri, bilgisayar_galibiyetleri
    bilgisayar_secimi = bilgisayar_secimi_al()

    if secili_dil == 'türkçe':
        secim_text = f"Siz: {kullanici_secimi.capitalize()}  |  Bilgisayar: {bilgisayar_secimi.capitalize()}"
    elif secili_dil == 'english':
        secim_text = f"You: {kullanici_secimi.capitalize()}  |  Computer: {bilgisayar_secimi.capitalize()}"

    # Secim label'ını güncellemeye yarar
    secim_label.config(text=secim_text, font=('Barlow ExtraBold', 30, 'bold'), fg='#5c340c')  # Yazı tipi, boyut, stil ve renk

    kazanan = tur_kazananini_belirle(kullanici_secimi, bilgisayar_secimi)

    if secili_dil == 'türkçe':
        if kazanan == "Kullanıcı":
            kullanici_galibiyetleri += 1
            sonuc = f"Bu turu kazandınız❕🥳\nKullanıcı: {kullanici_galibiyetleri}, Bilgisayar: {bilgisayar_galibiyetleri}"
        elif kazanan == "Bilgisayar":
            bilgisayar_galibiyetleri += 1
            sonuc = f"Bu turu bilgisayar kazandı❕🫣\nKullanıcı: {kullanici_galibiyetleri}, Bilgisayar: {bilgisayar_galibiyetleri}"
        else:
            sonuc = "Bu tur berabere! 🤝🏻🫂"
    elif secili_dil == 'english':
        if kazanan == "Player":
            kullanici_galibiyetleri += 1
            sonuc = f"You won this round❕🥳\nPlayer: {kullanici_galibiyetleri}, Computer: {bilgisayar_galibiyetleri}"
        elif kazanan == "Computer":
            bilgisayar_galibiyetleri += 1
            sonuc = f"The computer won this round❕🫣\nPlayer: {kullanici_galibiyetleri}, Computer: {bilgisayar_galibiyetleri}"
        else:
            sonuc = "This round is a draw❕🤝🏻🫂"

    # 0.5 saniye bekledikten sonra sonucu güncelleme
    root.after(500, lambda: sonuc_label.config(text=sonuc, font=('Barlow ExtraBold', 25, 'bold'), fg='#aaaa55'))  # Yazı tipi, boyut, stil ve renk

    if kullanici_galibiyetleri == 2 or bilgisayar_galibiyetleri == 2:
        if kullanici_galibiyetleri == 2:
            if secili_dil == 'türkçe':
                final_sonuc = "Tebrikler, oyunu kazandınız❕ 👏🏻😎👏🏻"
            elif secili_dil == 'english':
                final_sonuc = "Congratulations, you won the game❕ 👏🏻😎👏🏻"
        else:
            if secili_dil == 'türkçe':
                final_sonuc = "Maalesef, bilgisayar oyunu kazandı. 😱 "
            elif secili_dil == 'english':
                final_sonuc = "Unfortunately, the computer won the game. 😱"

        messagebox.showinfo("Oyun Bitti / Game Over", final_sonuc)
        root.after(1000, devam_istegi) # 1 saniye bekledikten sonra devam_istegi fonksiyonunu çağırma


# Devam etme isteğini göstermeye yarar
def devam_istegi():
    global secili_dil
    
    if secili_dil == 'türkçe':
        devam_mi = messagebox.askyesno("Devam Etmek İster Misiniz?", "Başka bir oyun oynamak ister misiniz❓❔")
    elif secili_dil == 'english':
        devam_mi = messagebox.askyesno("Do You Want to Continue?", "Do you want to play another game❓❔")
    
    bilgisayar_devam_mi = random.choice([True, False]) # Bilgisayarın rastgele devam etme kararını vermeye yarar
    
    if secili_dil == 'türkçe':
        bilgisayar_mesaji = f"Bilgisayar oyuna {'devam ediyor 😊' if bilgisayar_devam_mi else 'devam etmiyor 🥹'}."
        messagebox.showinfo("Bilgisayarın Kararı", bilgisayar_mesaji) # Bilgisayarın kararını kullanıcıya göstermeye yarar
        
    elif secili_dil == 'english':
        bilgisayar_mesaji = f"The computer {'wants to continue 😊' if bilgisayar_devam_mi else 'does not want to continue 🥹'} the game."
        messagebox.showinfo("Computer's Decision", bilgisayar_mesaji) # Bilgisayarın kararını kullanıcıya göstermeye yarar

    if devam_mi and bilgisayar_devam_mi:
        oyun_sifirla() # Her iki oyuncu da oynamak istiyorsa oyunu sıfırla ve yeniden başlatmaya yarar
    else:
        root.quit() # Uygulamayı kapatmaya yarar


# Oyun sıfırlamaya yarar
def oyun_sifirla():
    global kullanici_galibiyetleri, bilgisayar_galibiyetleri
    kullanici_galibiyetleri = 0
    bilgisayar_galibiyetleri = 0
    temizle_arayuz()
    tas_kagit_makas_MUHSİNE_TAŞCI() # Dil seçimini tekrar göstermeye yarar


# İlk olarak dil seçimi arayüzünü göstermeye yarar
tas_kagit_makas_MUHSİNE_TAŞCI()

# Arayüzü başlatmaya yarar
root.mainloop()