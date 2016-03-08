class Deska:
    def __init__(self, igralec0="B", igralec1="W"):
       osnova =[[None]*8 for _ in range(8)]
       osnova[4][3] = igralec0
       osnova[3][4] = igralec0
       osnova[3][3] = igralec1
       osnova[4][4] = igralec1
       self.ploskev = osnova
       self.vlogi = (igralec0,igralec1)

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
        if self.ploskev[x][y] is not None:
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
        if len(izbor_potez) == 0:
            return None
        else:
            return izbor_potez

    # podobno kot mprint, le da ne izriše roba (ničel, ki jih imam zato da me program ne utopi z error)
    # zdaj sem to zbrisal ker v tem primeru avsca GUI zalije z erori
    def izrisi(self):
        for i in self.ploskev:
            print(i)

    # metoda pove ali je konec igre?
    # metoda vrne (False,None) če igre ni konec in (True, "zmagovalec) če je
    def alije_konec(self):
        if self.moznosti(0) == None and self.moznosti(1) == None:
            return (True,self.vodi())
        else:
            return (False,None)

    # prešteje vse žetone na deski vrne v obliki  (število modrih, število belih)
    def vodi(self):
        zetoni0 = 0
        zetoni1 = 0
        for x in range(8):
            for y in range(8):
                if self.ploskev[x][y]== self.protagonist(0):
                    zetoni0 += 1
                elif self.ploskev[x][y]== self.protagonist(1):
                    zetoni1 += 1
        return zetoni0, zetoni1

    #naredi kopijo, uporabno pri umetni intiligenci
    def copy(self):
        (n_igralec0,n_igralec1) = self.vlogi
        nova= Deska(n_igralec0,n_igralec1)
        for x in range(8):
            for y in range(8):
                nova.ploskev[x][y]= self.ploskev[x][y]
        return nova

# natisne matriko na malo bolj pregleden način
def mprint (m):
    for i in m:
        print (i)

# #TESTIRANJE
# b = Deska()
# a = b.copy()
# print(a.legalno(0,(5,6)))
# a.postavi(0,(2,3))
# a.izrisi()
# print(a.vodi())
# print("")
# b.izrisi()


class MinMax:
    def __init__(self, globina):
        def __init__(self, globina):
            self.globina = globina  # do katere globine iščemo?
            self.prekinitev = False # ali moramo končati?
            self.pozicija = None # objekt, ki opisuje igro (ga dobimo kasneje)
            self.jaz = None  # katerega igralca igramo (podatek dobimo kasneje)
            self.poteza = None # sem napišemo potezo, ko jo najdemo

    # samoumevno
    def prekini(self):
        """Metoda, ki jo pokliče GUI, če je treba nehati razmišljati, ker
           je uporabnik zaprl okno ali izbral novo igro."""
        self.prekinitev = True

    # izračuna vrednost pozicije, zankrat le izpiše koliko so vredna posamezna polja
    def hevristika(self,pozicija,igralec):
        vrednosti = {
            #koti
            (0,0) : 100,
            (0,7) : 100,
            (7,0) : 100,
            (7,7) : 100,
            #ob robovih zraven kota
            (0,1) : -20,
            (0,6) : -20,
            (1,0) : -20,
            (1,7) : -20,
            (6,0) : -20,
            (6,7) : -20,
            (7,1) : -20,
            (7,6) : -20,
            #diagonalno na kot = DeadZONE
            (1,1) : -50,
            (1,6) : -50,
            (6,1) : -50,
            (6,6) : -50,
            #na robu ob deadzone
            (0,2) : 10,
            (0,5) : 10,
            (2,0) : 10,
            (2,7) : 10,
            (5,0) : 10,
            (5,7) : 10,
            (7,2) : 10,
            (7,5) : 10,
            #na sredini roba
            (0,3) : 5,
            (0,4) : 5,
            (3,0) : 5,
            (4,0) : 5,
            (3,7) : 5,
            (4,7) : 5,
            (7,3) : 5,
            (7,4) : 5,
            #ob robu
            (1,2) : -2,
            (1,3) : -2,
            (1,4) : -2,
            (1,5) : -2,
            #
            (2,1) : -2,
            (3,1) : -2,
            (4,1) : -2,
            (5,1) : -2,
            #
            (2,6) : -2,
            (3,6) : -2,
            (4,6) : -2,
            (5,6) : -2,
            #
            (6,2) : -2,
            (6,3) : -2,
            (6,4) : -2,
            (6,5) : -2,
            #sredina
            (2,2) : -1,
            (2,3) : -1,
            (2,4) : -1,
            (2,5) : -1,

            (3,2) : -1,
            (3,3) : -1,
            (3,4) : -1,
            (3,5) : -1,

            (4,2) : -1,
            (4,3) : -1,
            (4,4) : -1,
            (4,5) : -1,

            (5,2) : -1,
            (5,3) : -1,
            (5,4) : -1,
            (5,5) : -1,
        }
        test = Deska()
        for x in range(8):
            for y in range(8):
                test.ploskev[x][y] = vrednosti[(x,y)]
        test.izrisi()

tata = MinMax(4)
tata.hevristika((2),1)