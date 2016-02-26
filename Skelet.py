class Deska:
    def __init__(self):
       osnova = [[0]*10]+[[0]+[None]*8+[0] for _ in range(8)]+[[0]*10]
       osnova[5][4] = "B"
       osnova[4][5] = "B"
       osnova[4][4] = "M"
       osnova[5][5] = "M"
       self.ploskev = osnova

    #metodi antagonist in protagonist sta trenutno vpleminintirani če bi hotel kdaj zamenjati oznaki (M) in (B) za kaj drugega
    #vrne nasprotnika, kjer je 0 prvi igralec(B) in 1 drugi igralec(M)
    def antagonist(self, id):
        if id == 0:
            return "M"
        else:
            return "B"

    #vrne igralca, kjer je 0 prvi igralec(B) in 1 drugi igralec(M)
    def protagonist(self, id):
        if id == 0:
            return "B"
        else:
            return "M"

    #pogleda če je možno na mesto postaviti figuro, če je vrne poleg True tudi seznam figur ki se zamenjajo, če nanje postavimo figuro.
    def legalno (self, igralec, polozaj):
        (x,y) = polozaj
        if self.ploskev[x][y] != None:
            print ("napaka!!!")
            return (False)
        menjaj = []
        #pogleda po vseh osmih smereh
        for (a,b) in [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]:
            #čej je na tem sosednjem polju nasprotnik
            if (self.ploskev[x+a][y+b]) == self.antagonist(igralec):
                (xt,yt) = (x+a,y+b)
                menjaj_temp = []
                #nato si zapomni vrsto
                while (self.ploskev[xt][yt]) == self.antagonist(igralec):
                    menjaj_temp += [(xt,yt)]
                    xt += a
                    yt += b
                if self.ploskev[xt][yt] == self.protagonist(igralec):
                    menjaj += menjaj_temp
        #pogleda če se s postavitvjo na to mesto zamenja kaj žetonov, če se ne potem to ni legalna poteza
        if len(menjaj) == 0:
            return False
        else:
            return (True,menjaj)

    #postavi figuro igralca na dano pozicijo
    def postavi(self, igralec, poz):
        (x,y) = poz
        self.ploskev[x][y] = self.protagonist(igralec)

    #podobno kot mprint, le da ne izriše roba (ničel, ki jih imam zato da me program ne utopi z error)
    def izrisi(self):
        for i in self.ploskev[1:9]:
            print(i[1:9])

#natisne matriko na malo bolj pregleden način
def mprint (m):
    for i in m:
        print (i)


a = Deska()
a.izrisi()
#print(a.legalno(0,(3,4)))