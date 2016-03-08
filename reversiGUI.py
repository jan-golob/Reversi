import tkinter as tk
import Skelet as sk


class Gui():
    def __init__(self, master, rows=8, columns=8, size=64, color1="black", color2="brown"):
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
        file_menu.add_command(label="Izhod", command=master.destroy)
        recent_menu.add_command(label="igralec vs igralec", command=self.nastavitev_igralcev)

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


        self.nastavitev_igralcev()

    def nastavitev_igralcev(self):
        self.igralec_1 = Clovek(self)
        self.igralec_2 = Clovek(self)
        self.zacni_igro()

    def zacni_igro(self):
        self.igralec = True
        self.pl = sk.Deska()
        self.pl.izrisi()
        self.refresh()
        self.napis.set("modri igralec na potezi")
        self.igralec_1.igraj()
        
    def povleci_potezo(self, x, y):
        if self.pl.alije_konec():
            if self.igralec:
                if self.pl.moznosti(0) != []:
                    (a,b) = self.pl.vodi()
                    if self.pl.legalno(0,(x,y))[0]:
                        self.pl.postavi(0,(x,y))
                        self.addpiece(player2,x,y)
                        self.igralec = not self.igralec
                        if self.pl.alije_konec()[0]:
                            self.konec()
                        else:
                            self.refresh()
                            napis = "beli igralec na potezi M: " + str(a) + " B: " +str(b)
                            self.napis.set(napis)
                            self.igralec_2.igraj()
                    else:
                        self.igralec_1.igraj()
                        self.napis.set("neveljavna poteza modri")
                else:
                    print("ni potez")
                    self.igralec = not self.igralec
                    napis = "beli igralec na potezi M: " + str(a) + " B: " +str(b)
                    self.napis.set(napis)
                    self.igralec_2.igraj()
            else:
                if self.pl.moznosti(1) != []:
                    (a,b) = self.pl.vodi()
                    if self.pl.legalno(1,(x,y))[0]:
                        self.pl.postavi(1,(x,y))
                        self.addpiece(player1,x,y)
                        self.igralec = not self.igralec
                        if self.pl.alije_konec()[0]:
                            self.konec()
                        else:
                            self.refresh()
                            napis = "modri igralec na potezi M: " + str(a) + " B: " +str(b)
                            self.napis.set(napis)
                            self.igralec_2.igraj()
                    else:
                        self.igralec_1.igraj()
                        self.napis.set("neveljavna poteza beli")
                else:
                    print("ni potez")
                    self.igralec = not self.igralec
                    napis = "modri igralec na potezi M: " + str(a) + " B: " +str(b)
                    self.napis.set(napis)
                    self.igralec_2.igraj()
        else:
            self.konec()

    def konec(self):
        print("konec")
        (a,b) = self.pl.vodi()
        if a > b:
            napis = "Konec igre zmagovalec je modri z " + str(a) + " žetoni"
            self.napis.set(napis)
        else:
            napis = "Konec igre zmagovalec je beli z " + str(b) + " žetoni"
            self.napis.set(napis)

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

    def igraj(self):
        self.gui.canvas.bind('<Button-1>', self.klik)

    def klik(self, event):
        
        i = (event.y)//self.gui.size
        j = (event.x)//self.gui.size
        
        self.gui.povleci_potezo(i, j)

            
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Reversi")
    player1 = tk.PhotoImage(file = "white.gif")
    player2 = tk.PhotoImage(file = "blue.gif")
    board = Gui(root)
    root.mainloop()
