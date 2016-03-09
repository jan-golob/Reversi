import logging
import threading

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

def nasprotnik(i):
    if i == 0:
        return 1
    elif i == 1:
        return 0
    else:
        assert False, "to narobe uporabljaš"


class MinMax:
    ZMAGA = 10000
    INFI = ZMAGA + 109
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

    # Zažene minmax iz njim upravlja
    def optimalna_poteza(self, pozicija, igralec):
        self.pozicija = pozicija.copy()
        self.prekinitev = False # Glavno vlakno bo to nastvilo na True, če moramo nehati
        self.jaz = igralec
        self.poteza = None # Sem napišemo potezo, ko jo najdemo
        # Poženemo minimax
        (poteza, vrednost) = self.minimax(self.globina, True)
        self.jaz = None
        self.pozicija = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            logging.debug("minimax: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.poteza = poteza
    #
    def minimax(self, globina, maximiziramo):
        if self.prekinitev:
            # Sporočili so nam, da moramo prekiniti
            logging.debug ("Minimax prekinja, globina = {0}".format(globina))
            return (None, 0)
        #konec igre
        (konec, razmerje) = self.pozicija.alije_konec()
        if konec:
            (i0,i1) = razmerje
            if self.jaz == 0 and i0 > i1:
                return (None, MinMax.ZMAGA)
            elif self.jaz == 1 and i1 > i0:
                return (None, MinMax.ZMAGA)
            elif self.jaz == 0 and i1 > i0:
                return (None, -MinMax.ZMAGA)
            elif self.jaz == 1 and i0 > i1:
                return (None, -MinMax.ZMAGA)
            else:
                assert False, "neki je narobe a je mogoče neodločeno ali pa jst ne znam programirat"
        else:
            if globina == 0:
                return (None, self.hevristika(self.jaz))
            else:
                # Naredimo eno stopnjo minimax
                kopija = self.pozicija.copy()
                if maximiziramo:
                    # Maksimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = -MinMax.INFI
                    for p in self.pozicija.moznosti(self.jaz):
                        self.pozicija.postavi(self.jaz, p)
                        vrednost = self.minimax(globina-1, not maximiziramo)[1]
                        self.pozicija = kopija
                        if vrednost > vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = p
                else:
                    # Minimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = MinMax.INFI
                    for p in self.pozicija.moznosti(nasprotnik(self.jaz)):
                        self.pozicija.postavi(nasprotnik(self.jaz), p)
                        vrednost = self.minimax(globina-1, not maximiziramo)[1]
                        self.pozicija = kopija
                        if vrednost < vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = p
                assert (najboljsa_poteza is not None), "minimax: izračunana poteza je None"
                return (najboljsa_poteza, vrednost_najboljse)
                
        
    # izračuna vrednost pozicije, zankrat le izpiše koliko so vredna posamezna polja
    def hevristika(self,igralec):
        vrednosti= [[100, -20, 10, 5, 5, 10, -20, 100], [-20, -50, -2, -2, -2, -2, -50, -20],[10, -2, -1, -1, -1, -1, -2, 10], [5, -2, -1, -1, -1, -1, -2, 5],
            [5, -2, -1, -1, -1, -1, -2, 5], [10, -2, -1, -1, -1, -1, -2, 10], [-20, -50, -2, -2, -2, -2, -50, -20], [100, -20, 10, 5, 5, 10, -20, 100]]
        ocena = 0
        for x in range(8):
            for y in range(8):
                if self.pozicija.ploskev[x][y] == self.pozicija.protagonist(igralec):
                    ocena += vrednosti[x][y]
                elif self.pozicija.ploskev[x][y] == self.pozicija.antagonist(igralec):
                    ocena -= vrednosti[x][y]
        return ocena
        

test = Deska()

tata = MinMax(2)
