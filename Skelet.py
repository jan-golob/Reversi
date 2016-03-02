class Deska:
    def __init__(self, igralec1="B", igralec2="W"):
       osnova =[[None]*8 for _ in range(8)]
       osnova[4][3] = igralec1
       osnova[3][4] = igralec1
       osnova[3][3] = igralec2
       osnova[4][4] = igralec2
       self.ploskev = osnova
       self.vlogi = (igralec1,igralec2)

    # metodi antagonist in protagonist sta trenutno vpleminintirani če bi hotel kdaj zamenjati oznaki (M) in (B) za kaj drugega, kot sem storil
    # vrne nasprotnika, kjer je 0 prvi igralec(B) in 1 drugi igralec(M)
    def antagonist(self, igralec):
        if igralec == 0:
            return self.vlogi[1]
        else:
            return self.vlogi[0]

    # vrne igralca, kjer je 0 prvi igralec(B) in 1 drugi igralec(M)
    def protagonist(self, igralec):
            return self.vlogi[igralec]

    # pogleda če je možno na mesto postaviti figuro, če je vrne poleg True tudi seznam figur ki se zamenjajo, če nanje postavimo figuro.
    def legalno (self, igralec, polozaj):
        (x,y) = polozaj
        if self.ploskev[x][y] != None:
            # print ("napaka!!!")
            return (False,None)
        menjaj = []
        # pogleda po vseh osmih smereh
        for (a,b) in [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]:
            # prvo pogleda, če je sploh v matriki
            if (x+a in range(8)) and (y+b in range(8)) and (self.ploskev[x+a][y+b]) == self.antagonist(igralec):
                (xt,yt) = (x+a,y+b)
                menjaj_temp = []
                na_deski= ((xt in range(8)) and (yt in range(8)))
                # nato si zapomni vrsto
                while na_deski and (self.ploskev[xt][yt]) == self.antagonist(igralec):
                    menjaj_temp += [(xt,yt)]
                    xt += a
                    yt += b
                    na_deski = ((xt in range(8)) and (yt in range(8)))
                if na_deski and (self.ploskev[xt][yt] == self.protagonist(igralec)):
                    menjaj += menjaj_temp
        #pogleda če se s postavitvjo na to mesto zamenja kaj žetonov, če se ne potem to ni legalna poteza
        if len(menjaj) == 0:
            return (False,None)
        else:
            return (True,menjaj)


    # postavi figuro igralca če je mogoče, na dano pozicijo in obrne žetone, ki jih je potrebno
    def postavi(self, igralec, poz):
        (a_je,polja) = self.legalno(igralec,poz)
        if a_je:
            for (m,n) in [poz]+polja:
                self.ploskev[m][n] = self.protagonist(igralec)
        else:
            print("Ilegalna poteza")

    # vrne vse možne poteze za danega igralca
    def moznosti(self,igralec):
        izbor_potez = []
        for x in range(8):
            for y in range(8):
                if self.legalno(igralec,(x,y))[0]:
                    izbor_potez.append((x,y))
        return izbor_potez

    # podobno kot mprint, le da ne izriše roba (ničel, ki jih imam zato da me program ne utopi z error)
    # zdaj sem to zbrisal ker v tem primeru avsca GUI zalije z erori
    def izrisi(self):
        for i in self.ploskev:
            print(i)


# natisne matriko na malo bolj pregleden način
def mprint (m):
    for i in m:
        print (i)


a = Deska()
print(a.legalno(0,(5,6)))
a.postavi(0,(2,3))
a.izrisi()
#testing
#
# a = Deska("a","b")
#
# print([a.protagonist(0)])
#
# dr = a.antagonist(0)
# pr = a.protagonist(0)
#
# a.ploskev[1][1]='?'
#
# a.ploskev[3][3] = pr
# a.ploskev[3][4] = dr
# a.ploskev[3][6] = dr
#
# a.ploskev[4][4] = dr
# a.ploskev[4][5] = dr
# a.ploskev[4][6] = dr
#
# a.ploskev[5][4] = dr
# a.ploskev[5][5] = pr
# a.ploskev[5][6] = dr
#
# a.ploskev[6][3] = pr
# a.ploskev[6][4] = dr
# a.ploskev[6][6] = dr
#
# a.izrisi()
# x=5
# y=3
# print((a.ploskev[y][x]))
# print(a.legalno(0,(y,x)))
