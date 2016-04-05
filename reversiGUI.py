import tkinter as tk
import skelet as sk
import threading # za vzporedno izvajanje
import logging # za odpravljanje napak


class Gui():
    def __init__(self, master, rows=8, columns=8, size=64, color1="gray2", color2="burlywood3"):
        '''nastavimo velikost zaslona in barve kvadratov'''

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2

        self.prekini = False
        self.zacetek = True
        #nastavimo začetno globina
        self.globina = 4
        self.igralec_1 = None
        self.igralec_2 = None

        canvas_width = columns * size
        canvas_height = rows * size

        self.napis = tk.StringVar(master, value="REVERSI")
        tk.Label(master, textvariable=self.napis).grid(row=2, column=0)

        # Glavni menu
        self.menu = tk.Menu(master)
        master.config(menu=self.menu) # Dodamo menu
        # Naredimo podmenu "File"
        self.file_menu = tk.Menu(self.menu)
        self.recent_menu = tk.Menu(self.menu)
        self.debug_menu = tk.Menu(self.menu)
        self.tez_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Nastavitve", menu=self.file_menu)
        self.file_menu.add_cascade(label="nacin igranja", menu=self.recent_menu)

        # Dodamo izbire v file_menu
        self.file_menu.add_separator() # To doda separator v menu
        self.file_menu.add_command(label="Izhod", command=lambda: self.zapri_okno(master))
        self.recent_menu.add_command(label="igralec vs igralec",command=lambda: self.prekini_in_nastavi(Clovek(self),Clovek(self),False,False))
        self.recent_menu.add_command(label="igralec vs racunalnik",command=lambda: self.prekini_in_nastavi(Clovek(self),Racunalnik(self, sk.AlphaBeta(self.globina)),False,True))
        self.recent_menu.add_command(label="racunalnik vs igralec",command=lambda: self.prekini_in_nastavi(Racunalnik(self, sk.AlphaBeta(self.globina)),Clovek(self),True,False))
        self.recent_menu.add_command(label="racunalnik vs racunalnik",command=lambda: self.prekini_in_nastavi(Racunalnik(self, sk.AlphaBeta(self.globina)),Racunalnik(self, sk.AlphaBeta(self.globina)),True,True))
        # Dodamo izbire v tez_menu
        self.menu.add_cascade(label="Težavnost", menu=self.tez_menu)
        self.tez_menu.add_command(label="Lahko", command=lambda: self.tezavnost(2))
        self.tez_menu.add_command(label="Normalno", command=lambda: self.tezavnost(3))
        self.tez_menu.add_command(label="Težko", command=lambda: self.tezavnost(4))
        self.tez_menu.add_command(label="Zelo Težko", command=lambda: self.tezavnost(5))
        self.tez_menu.add_command(label="Prekini", command=lambda: self.defenziva())

        self.canvas = tk.Canvas(master, width=canvas_width, height=canvas_height)
        self.canvas.grid(row = 1,column = 0)

        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color)
                color = self.color1 if color == self.color2 else self.color2

        #nastavimo začetno igro
        self.nastavitev_igralcev(Clovek(self),Racunalnik(self, sk.AlphaBeta(self.globina)),False,True)

    def defenziva(self):
        self.prekini_igralce()
        self.prekini = True
        self.omogoci()
        self.refresh()

    
    def onemogoci(self):
        """onemogoči spreminjanje nastavitev"""
        if not self.zacetek:
            self.recent_menu.entryconfig(1, state="disabled")
            self.recent_menu.entryconfig(2, state="disabled")
            self.recent_menu.entryconfig(3, state="disabled")
            self.recent_menu.entryconfig(4, state="disabled")
            self.tez_menu.entryconfig(1,state="disabled")
            self.tez_menu.entryconfig(2,state="disabled")
            self.tez_menu.entryconfig(3,state="disabled")
            self.tez_menu.entryconfig(4,state="disabled")

    def omogoci(self):
        """omogoči spreminjanje nastavitev"""
        if self.prekini:
            self.recent_menu.entryconfig(1, state="normal")
            self.recent_menu.entryconfig(2, state="normal")
            self.recent_menu.entryconfig(3, state="normal")
            self.recent_menu.entryconfig(4, state="normal")
            self.tez_menu.entryconfig(1,state="normal")
            self.tez_menu.entryconfig(2,state="normal")
            self.tez_menu.entryconfig(3,state="normal")
            self.tez_menu.entryconfig(4,state="normal")

    def nastavitev_igralcev(self, modri, beli,ali_je_racunalnik_1,ali_je_racunalnik_2):
        """nastavi igralce in pokliče metodo zacni_igro"""
        self.prekini_igralce()
        self.igralec_1 = modri
        self.igralec_2 = beli
        self.igralec_1_na_potezi = True
        self.je_prvi_racunalnik = ali_je_racunalnik_1
        self.je_drugi_racunalnik = ali_je_racunalnik_2
        if self.je_prvi_racunalnik or self.je_drugi_racunalnik: 
            self.onemogoci()
        self.zacni_igro()

    def zacni_igro(self):
        """nastavi desko in zacne igro"""     
        self.pl = sk.Deska()
        self.refresh()
        self.napis.set("modri igralec na potezi")

        self.igralec_1.igraj()

    def tezavnost(self,globina):
        """omogoča spreminjanje težavnosti nasprotnika(spreminja se globina alpha beta)"""
        self.globina = globina
        if self.je_prvi_racunalnik == False and self.je_drugi_racunalnik == False:
            pass
        elif self.je_prvi_racunalnik == False and self.je_drugi_racunalnik == True:
            self.prekini_in_nastavi(Clovek(self),Racunalnik(self, sk.AlphaBeta(self.globina)),False,True)
        elif self.je_prvi_racunalnik == True and self.je_drugi_racunalnik == False:
            self.prekini_in_nastavi(Racunalnik(self, sk.AlphaBeta(self.globina)),Clovek(self),True,False)
        else:
            self.prekini_in_nastavi(Racunalnik(self, sk.AlphaBeta(self.globina)),Racunalnik(self, sk.AlphaBeta(self.globina)),True,True)


    def prekini_igralce(self):
        """Sporoči igralcem, da morajo nehati razmišljati.""" 
        if self.igralec_1: self.igralec_1.prekini()
        if self.igralec_2: self.igralec_2.prekini()

    def prekini_in_nastavi(self,modri,beli,ali_je_racunalnik_1,ali_je_racunalnik_2):
        """Metoda se klice pri spreminjanju težavnosti. Metoda prekine dane igralce in
        uporabi nove nastavitve, da ponovno zažene igro"""
        self.prekini_igralce()
        self.zacetek = False
        #tuki mam to zato da slučajno mau mn zabugga
        self.nastavitev_igralcev(modri,beli,ali_je_racunalnik_1,ali_je_racunalnik_2)

    def zapri_okno(self, master):
        """Ta metoda se pokliče, ko uporabnik zapre aplikacijo."""
        # Vlaknom, ki tečejo vzporedno, je treba sporočiti, da morajo
        # končati, sicer se bo okno zaprlo, aplikacija pa bo še vedno
        # delovala.
        self.prekini_igralce()
        # Dejansko zapremo okno.
        master.destroy()

    def zamenjaj_napis(self,igralec):
        """metoda skrbi za menjavo napisov v GUI"""
        (a,b) = self.pl.vodi()
        if self.pl.alije_konec()[0]:
            if a > b:
                napis = "Konec igre zmagovalec je modri z rezultatom " + str(a) + " proti " + str(b)
                self.napis.set(napis)
            else:
                napis = "Konec igre zmagovalec je beli z rezultatom " + str(b) + " proti " + str(a)
                self.napis.set(napis)
        else:
            if not igralec:
                napis = "beli igralec na potezi M: " + str(a) + " B: " +str(b)
                self.napis.set(napis)
            else:
                napis = "modri igralec na potezi M: " + str(a) + " B: " +str(b)
                self.napis.set(napis)

    def naredi_potezo(self,x,y,igralec):
        """odigra potezo"""

        #v tem delu samo določimo spremenjljivke ki jih v nadaljevanju funkcije uporabljamo
        if igralec == 0:
            jaz = self.igralec_1
            neveljaven_napis = "neveljavna poteza modri"
            nasprotnik = self.igralec_2
            sm_rac = self.je_prvi_racunalnik
        if igralec == 1:
            nasprotnik = self.igralec_1
            jaz = self.igralec_2
            neveljaven_napis = "neveljavna poteza beli"
            sm_rac = self.je_drugi_racunalnik

        #tu se odigra poteza
        if self.pl.moznosti(igralec) != None:
            if self.pl.legalno(igralec,(x,y))[0]:
                self.pl.postavi(igralec,(x,y))
                self.addpiece(player2,x,y)
                self.refresh()
                self.igralec_1_na_potezi = not self.igralec_1_na_potezi
                if self.pl.alije_konec()[0]:
                    self.konec()
                else:
                    self.refresh()
                    self.zamenjaj_napis(self.igralec_1_na_potezi)
                    nasprotnik.igraj()
            else:
                jaz.igraj()
                self.napis.set(neveljaven_napis)
        else:
            self.igralec_1_na_potezi = not self.igralec_1_na_potezi
            self.zamenjaj_napis(self.igralec_1_na_potezi)
            nasprotnik.igraj()


    def povleci_potezo(self, x, y):
        """kliče funkcijo naredi potezo za primernega igralca
            ali pa zaključi igro"""
        if not self.pl.alije_konec()[0]:
            if self.igralec_1_na_potezi:
                self.naredi_potezo(x,y,0)

            else:
                self.naredi_potezo(x,y,1)

        else:
            self.konec()

    def konec(self):
        self.zamenjaj_napis(self.igralec_1_na_potezi)
        self.prekinitev = True
        self.omogoci()


    def addpiece(self, image, row, column):
        '''Doda figuro na igralno ploščo v kvadratek (row,column)'''

        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)

        self.canvas.create_image(x0,y0, image=image, tags="figura")


    def refresh(self):
        """Izbriše dosedanje figure in jih ponovno nariše glede na novo matriko"""

        self.canvas.delete("figura")
        for i in range(0,8):
            for j in range(0,8):
                if self.pl.ploskev[i][j] != None:
                    if self.pl.ploskev[i][j] == "W":
                        self.addpiece(player2, i, j)
                    else:
                        self.addpiece(player1, i, j)

    def potencialne(self):
        """preveri poteze, ki jih določen igralec lahko odigra"""
        if self.igralec_1_na_potezi:
            igr = 0
        else:
            igr = 1
        potencialne_poteze = self.pl.moznosti(igr)
        if potencialne_poteze is not None:
            #obrnemo vrstni red zaradi problemov
            for (y,x) in potencialne_poteze:
                x0 = (x * self.size) + int(self.size*(7/16))
                x1 = (x * self.size) + int(self.size*(9/16))
                y0 = (y * self.size) + int(self.size*(7/16))
                y1 = (y * self.size) + int(self.size*(9/16))
                self.canvas.create_oval(x1,y1,x0,y0, fill="green", tags="figura")


class Clovek():
    def __init__(self, gui):
        self.gui = gui

    def prekini(self):
        # To metodo kliče GUI, če je treba prekiniti razmišljanje.
        # Človek jo lahko ignorira.
        pass

    def igraj(self):
        self.gui.potencialne()
        self.gui.canvas.bind('<Button-1>', self.klik)

    def klik(self, event):
        if ((self.gui.igralec_1_na_potezi and self == self.gui.igralec_1) or
           (not self.gui.igralec_1_na_potezi and self == self.gui.igralec_2)):
            i = (event.y)//self.gui.size
            j = (event.x)//self.gui.size
            self.gui.povleci_potezo(i, j)

class Racunalnik():
    def __init__(self, gui, algoritem):
        self.gui = gui
        self.algoritem = algoritem # Algoritem, ki izračuna potezo
        self.mislec = None # Vlakno (thread), ki razmišlja

    def igraj(self):
        """Igraj potezo, ki jo vrne algoritem."""
        # Tu sprožimo vzporedno vlakno, ki računa potezo. Ker tkinter ne deluje,
        # če vzporedno vlakno direktno uporablja tkinter (glej http://effbot.org/zone/tkinter-threads.htm),
        # zadeve organiziramo takole:
        # - poženemo vlakno, ki poišče potezo
        # - to vlakno nekam zapiše potezo, ki jo je našlo
        # - glavno vlakno, ki sme uporabljati tkinter, vsakih 100ms pogleda, ali
        #   je že bila najdena poteza (metoda preveri_potezo spodaj).
        # Ta rešitev je precej amaterska. Z resno knjižnico za GUI bi zadeve lahko
        # naredili bolje (vlakno bi samo sporočilo GUI-ju, da je treba narediti potezo).
        # Naredimo vlakno, ki mu podamo *kopijo* igre (da ne bo zmedel GUIja):
        if self.gui.igralec_1_na_potezi:
            self.mislec = threading.Thread(
                target=lambda: self.algoritem.optimalna_poteza(self.gui.pl.copy(),0))
        else:
            self.mislec = threading.Thread(
                target=lambda: self.algoritem.optimalna_poteza(self.gui.pl.copy(),1))

        # Poženemo vlakno:
        self.mislec.start()

        # Gremo preverjat, ali je bila najdena poteza:
        self.gui.canvas.after(100, self.preveri_potezo)

    def preveri_potezo(self):
        """Vsakih 100ms preveri, ali je algoritem že izračunal potezo."""
        if self.algoritem.poteza is not None:
            # Algoritem je našel potezo, povleci jo, če ni bilo prekinitve
            self.gui.povleci_potezo(self.algoritem.poteza[0],self.algoritem.poteza[1])
            # Vzporedno vlakno ni več aktivno, zato ga "pozabimo"
            self.mislec = None
        else:
            # Algoritem še ni našel poteze, preveri še enkrat čez 100ms
            self.gui.canvas.after(100, self.preveri_potezo)

    def prekini(self):
        # To metodo kliče GUI, če je treba prekiniti razmišljanje.
        if self.mislec:
            #logging.debug ("Prekinjamo {0}".format(self.mislec))
            # Algoritmu sporočimo, da mora nehati z razmišljanjem
            self.algoritem.prekini()
            # Počakamo, da se vlakno ustavi
            self.mislec.join()
            self.mislec = None

    def klik(self, p):
        # Računalnik ignorira klike
        pass


            
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    root = tk.Tk()
    root.title("Reversi")
    player2 = tk.PhotoImage(file = "white.gif")
    player1 = tk.PhotoImage(file = "blue.gif")
    board = Gui(root)
    root.mainloop()
