import tkinter as tk

class GameBoard(tk.Frame):
    def __init__(self, parent, rows=8, columns=8, size=64, color1="black", color2="brown"):
        '''size is the size of a square, in pixels'''
        
        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2

        self.poteza = True

        a = Deska()
        self.pl = a.ploskev

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind('<Button-1>', self.click)
        self.canvas.bind("<ButtonRelease-1>", self.refresh)
        self.canvas.bind("<Configure>", self.refresh)

    def click(self, event):
        
        x = (event.y)//self.size
        y = (event.x)//self.size
        if self.pl[x][y] != None:
            pass
        else:
            if self.poteza == True:
                self.addpiece("player1"+ str(x) + str(y), player1, x, y)
                self.pl[x][y] = "B"
                self.poteza = False
            else:
                self.addpiece("player2" + str(x) + str(y), player2, x, y)
                self.pl[x][y] = "M"
                self.poteza = True
            self.refresh

    def addpiece(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        self.canvas.create_image(-100,-100, image=image, tags=(name, "piece"), anchor="c")
        self.placepiece(name, row, column)

    def placepiece(self, name, row, column):
        '''Place a piece at the given row/column'''
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords(name, x0, y0)

    def refresh(self, event):
        self.canvas.delete("square")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        for i in range(8):
            for j in range(8):
                if self.pl[i][j] != None:
                    if self.pl[i][j] == "B":
                        self.addpiece((self.pl[i][j]) + str(i) + str(j), player1, i, j)
                    else:
                        self.addpiece((self.pl[i][j]) + str(i) + str(j), player2, i, j)
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

class Deska():

    def __init__(self):
        osnova = [[None]*8 for _ in range(8)]
        osnova[3][4] = "B"
        osnova[4][3] = "B"
        osnova[4][4] = "M"
        osnova[3][3] = "M"
        self.ploskev = osnova

    def __repr__ (self):
        def mprint (m):
            for i in m:
                print (i)
        mprint(self.ploskev)
     

if __name__ == "__main__":
    root = tk.Tk()
    board = GameBoard(root)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    player1 = tk.PhotoImage(file = "white.gif")
    player2 = tk.PhotoImage(file = "blue.gif")
    root.mainloop()
