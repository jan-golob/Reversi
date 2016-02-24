osnova = [[None]*8 for _ in range(8)]
osnova[3][4] = "B"
osnova[4][3] = "B"
osnova[4][4] = "M"
osnova[3][3] = "M"

class Deska: 
    def __init__(self):
       osnova = [[None]*8 for _ in range(8)]
       osnova[3][4] = "B"
       osnova[4][3] = "B"
       osnova[4][4] = "M"
       osnova[3][3] = "M"
       self. ploskev = osnova

    def __repr__ (self):
        def mprint (m):
            for i in m:
                print (i)
        mprint(self.ploskev)



def mprint (m):
    for i in m:
        print (i)

def vstavi(deska, igralec, poz):
    (x,y) = poz
    deska[x][y] = igralec
    



#vstavi(osnova, "M", (0,0))

#mprint(osnova)
