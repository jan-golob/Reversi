import tkinter as tk
import Skelet as sk
import threading # za vzporedno izvajanje
import logging # za odpravljanje napak

#GLOBINA MINMAXA
GLO= 3

class Gui():
    def __init__(self, master, rows=8, columns=8, size=64, color1="black", color2="red"):
        '''nastavimo velikost zaslona in barve kvadratov'''

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2

        canvas_width = columns * size
        canvas_height = rows * size
        
        self.napis = tk.StringVar(master, value="REVERSI")
        tk.Label(master, textvariable=self.napis).grid(row=2, column=0)

        # Glavni menu
        menu = tk.Menu(master)
        master.config(menu=menu) # Dodamo menu
        # Naredimo podmenu "File"
        file_menu = tk.Menu(menu)
        recent_menu = tk.Menu(menu)
        menu.add_cascade(label="Nastavitve", menu=file_menu)
        file_menu.add_cascade(label="nacin igranja", menu=recent_menu)
        # Dodamo izbire v file_menu
        file_menu.add_separator() # To doda separator v menu
        file_menu.add_command(label="Izhod", command=lambda: self.zapri_okno(master))
        recent_menu.add_command(label="igralec vs igralec",command=lambda: self.nastavitev_igralcev(Clovek(self),Clovek(self)))
        recent_menu.add_command(label="igralec vs racunalnik",command=lambda: self.nastavitev_igralcev(Clovek(self),Racunalnik(self, sk.MinMax(GLO))))
        recent_menu.add_command(label="racunalnik vs racunalnik",command=lambda: self.nastavitev_igralcev(Racunalnik(self, sk.MinMax(GLO)),Racunalnik(self, sk.MinMax(GLO))))
        recent_menu.add_command(label="racunalnik vs clovek",command=lambda: self.nastavitev_igralcev(Racunalnik(self, sk.MinMax(GLO)),Clovek(self)))
        
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


        self.nastavitev_igralcev(Clovek(self),Racunalnik(self, sk.MinMax(GLO)))

    def nastavitev_igralcev(self, modri, beli):
        self.igralec_1 = modri
        self.igralec_2 = beli
        self.igralec = True
        self.zacni_igro()

    def zacni_igro(self):
        self.prekini_igralce()
        self.pl = sk.Deska()
        self.pl.izrisi()
        self.refresh()
        self.napis.set("modri igralec na potezi")
        self.igralec_1.igraj()

    def prekini_igralce(self):
        """Sporoči igralcem, da morajo nehati razmišljati."""
        if self.igralec:
            self.igralec_1.prekini()
        if not self.igralec:
            self.igralec_2.prekini()

    def zapri_okno(self, master):
        """Ta metoda se pokliče, ko uporabnik zapre aplikacijo."""
        # Vlaknom, ki tečejo vzporedno, je treba sporočiti, da morajo
        # končati, sicer se bo okno zaprlo, aplikacija pa bo še vedno
        # delovala.
        self.prekini_igralce()
        # Dejansko zapremo okno.
        master.destroy()

    def zamenjaj_napis(self,igralec):
        (a,b) = self.pl.vodi()
        if self.pl.alije_konec()[0]:
            if a > b:
                napis = "Konec igre zmagovalec je modri z " + str(a) + " žetoni proti " + str(b) + " žetonom belega" 
                self.napis.set(napis)
            else:
                napis = "Konec igre zmagovalec je beli z " + str(b) + " žetoni proti " + str(a) + " žetonom modrega" 
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
        if igralec == 1:
            nasprotnik = self.igralec_1
            jaz = self.igralec_2
            neveljaven_napis = "neveljavna poteza beli"

        #tu se odigra poteza
        if self.pl.moznosti(igralec) != None:
            if self.pl.legalno(igralec,(x,y))[0]:
                self.pl.postavi(igralec,(x,y))
                self.addpiece(player2,x,y)
                self.refresh()
                self.igralec = not self.igralec
                if self.pl.alije_konec()[0]:
                    self.konec()
                else:
                    self.refresh()
                    self.zamenjaj_napis(self.igralec)
                    nasprotnik.igraj()
            else:
                jaz.igraj()
                self.napis.set(neveljaven_napis)
        else:
            self.igralec = not self.igralec
            self.zamenjaj_napis(self.igralec)
            nasprotnik.igraj()
        
             
    def povleci_potezo(self, x, y):
        """kliče funkcijo naredi potezo za primernega igralca
            ali pa zaključi igro"""
        if not self.pl.alije_konec()[0]:
            if self.igralec:
                self.naredi_potezo(x,y,0)

            else:
                self.naredi_potezo(x,y,1)

        else:
            self.konec()

    def konec(self):
        self.zamenjaj_napis(self.igralec)


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
                        self.addpiece(player1, i, j)
                    else:
                        self.addpiece(player2, i, j)


class Clovek():
    def __init__(self, gui):
        self.gui = gui

    def prekini(self):
        # To metodo kliče GUI, če je treba prekiniti razmišljanje.
        # Človek jo lahko ignorira.
        pass

    def igraj(self):
        self.gui.canvas.bind('<Button-1>', self.klik)

    def klik(self, event):
        
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
        print(self.gui.igralec)
        if self.gui.igralec:
            self.mislec = threading.Thread(
                target=lambda: self.algoritem.optimalna_poteza(self.gui.pl.copy(),0))
        if not self.gui.igralec:
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
            logging.debug ("Prekinjamo {0}".format(self.mislec))
            # Algoritmu sporočimo, da mora nehati z razmišljanjem
            self.algoritem.prekini()
            # Počakamo, da se vlakno ustavi
            self.mislec.join()
            self.mislec = None

    def klik(self, p):
        # Računalnik ignorira klike
        pass


            
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Reversi")
    player1 = tk.PhotoImage(file = "white.gif")
    player2 = tk.PhotoImage(file = "blue.gif")
    board = Gui(root)
    root.mainloop()
