import logging

class Deska:
    def __init__(self, igralec0="B", igralec1="W"):
       osnova =[[None]*8 for _ in range(8)]
       osnova[4][3] = igralec0
       osnova[3][4] = igralec0
       osnova[3][3] = igralec1
       osnova[4][4] = igralec1
       self.ploskev = osnova
       self.vlogi = (igralec0,igralec1)


    def antagonist(self, igralec):
        """metodi antagonist in protagonist sta trenutno vpleminintirani če bi hotel kdaj zamenjati oznaki (M) in (B) za kaj drugega, kot sem storil
        vrne nasprotnika, kjer je 0 prvi igralec(B) in 1 drugi igralec(M)"""
        if igralec == 0:
            return self.vlogi[1]
        else:
            return self.vlogi[0]


    def protagonist(self, igralec):
        """vrne igralca, kjer je 0 prvi igralec(B) in 1 drugi igralec(M)"""
        return self.vlogi[igralec]

    def legalno (self, igralec, polozaj):
        """pogleda če je možno na mesto postaviti figuro, če je vrne poleg True tudi seznam figur ki se zamenjajo, če nanje postavimo figuro."""
        (x,y) = polozaj
        if self.ploskev[x][y] is not None:
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


    def postavi(self, igralec, poz):
        """postavi figuro igralca če je mogoče, na dano pozicijo in obrne žetone, ki jih je potrebno"""
        (a_je,polja) = self.legalno(igralec,poz)
        if a_je:
            for (m,n) in [poz]+polja:
                self.ploskev[m][n] = self.protagonist(igralec)
        else:
            pass

    def moznosti(self,igralec):
        """vrne vse možne poteze za danega igralca"""
        izbor_potez = []
        for x in range(8):
            for y in range(8):
                if self.legalno(igralec,(x,y))[0]:
                    izbor_potez.append((x,y))
        if len(izbor_potez) == 0:
            return None
        else:
            return izbor_potez


    def alije_konec(self):
        """metoda pove ali je konec igre?, metoda vrne (False,None) če igre ni konec in (True, "zmagovalec) če je"""
        if self.moznosti(0) == None and self.moznosti(1) == None:
            return (True,self.vodi())
        else:
            return (False,None)

    def vodi(self):
        """prešteje vse žetone na deski vrne v obliki  (število modrih, število belih)"""
        zetoni0 = 0
        zetoni1 = 0
        for x in range(8):
            for y in range(8):
                if self.ploskev[x][y]== self.protagonist(0):
                    zetoni0 += 1
                elif self.ploskev[x][y]== self.protagonist(1):
                    zetoni1 += 1
        return zetoni0, zetoni1

    def copy(self):
        """naredi kopijo, uporabno pri umetni intiligenci"""
        (n_igralec0,n_igralec1) = self.vlogi
        nova= Deska(n_igralec0,n_igralec1)
        for x in range(8):
            for y in range(8):
                nova.ploskev[x][y]= self.ploskev[x][y]
        return nova

def mprint (m):
    """natisne matriko na malo bolj pregleden način"""
    for i in m:
        print (i)


def nasprotnik(i):
    if i == 0:
        return 1
    elif i == 1:
        return 0
    else:
        assert False, "to narobe uporabljaš"


class AlphaBeta:
    ZMAGA = 1000000
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
        #logging.debug ("Alphabeta prekinja, self.prekinitev = {0}".format(self.prekinitev))
        self.prekinitev = True

    # Zažene alfabeta iz njim upravlja
    def optimalna_poteza(self, pozicija, igralec):
        self.prekinitev = False # Glavno vlakno bo to nastvilo na True, če moramo nehati
        # print("optimalna poteza")
        self.jaz = igralec
        self.poteza = None # Sem napišemo potezo, ko jo najdemo
        # Poženemo minimax
        (poteza, vrednost) = self.alphabeta(self.globina, -AlphaBeta.INFI, AlphaBeta.INFI, pozicija.copy(), True)
        # self.jaz = None
        self.pozicija = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            #print("minimax: poteza {0}, vrednost {1}".format(poteza, vrednost))
            #logging.debug("minimax: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.poteza = poteza
    #
    def alphabeta(self, globina, A, B, pozicija, maximiziramo):
        # print("alfabeta")
        if self.prekinitev:
            # Sporočili so nam, da moramo prekiniti
            #logging.debug ("Minimax prekinja, globina = {0}".format(globina))
            return (None, 0)
        #konec igre
        (konec, razmerje) = pozicija.alije_konec()
        if konec:
            (i0,i1) = razmerje
            if self.jaz == 0 and i0 > i1:
                return (None, AlphaBeta.ZMAGA)
            elif self.jaz == 1 and i1 > i0:
                return (None, AlphaBeta.ZMAGA)
            elif self.jaz == 0 and i1 > i0:
                return (None, -AlphaBeta.ZMAGA)
            elif self.jaz == 1 and i0 > i1:
                return (None, -AlphaBeta.ZMAGA)
            else:
                return (None, 0)
                #assert False, "neki je narobe a je mogoče neodločeno ali pa jst ne znam programirat"
        else:
            if globina == 0:
                return (None, self.hevristika(self.jaz, pozicija))
            else:
                # Naredimo eno stopnjo minimax
                if maximiziramo:
                    # Maksimiziramo
                    moznosti = pozicija.moznosti(self.jaz)
                    #preverimo če imamo sploh potezo
                    if moznosti == None:
                        return self.alphabeta(globina,A,B, pozicija.copy(), not maximiziramo)
                    else:
                        najboljsa_poteza = None
                        vrednost_najboljse = -AlphaBeta.INFI
                        for p in moznosti:
                            kopija = pozicija.copy()
                            kopija.postavi(self.jaz, p)
                            vrednost = self.alphabeta(globina-1,A,B,kopija, not maximiziramo)[1]

                            if vrednost > vrednost_najboljse:
                                vrednost_najboljse = vrednost
                                najboljsa_poteza = p
                                A = max(A,vrednost)
                                if B <= A:
                                    break
                else:
                    # Minimiziramo
                    moznosti = pozicija.moznosti(nasprotnik(self.jaz))
                    #preverimo če imamo sploh potezo
                    if moznosti == None:
                        return self.alphabeta(globina,A,B, pozicija.copy(), not maximiziramo)
                    else:
                        najboljsa_poteza = None
                        vrednost_najboljse = AlphaBeta.INFI
                        for p in moznosti:
                            kopija = pozicija.copy()
                            kopija.postavi(nasprotnik(self.jaz), p)
                            vrednost = self.alphabeta(globina-1, A, B, kopija, not maximiziramo)[1]

                            if vrednost < vrednost_najboljse:
                                vrednost_najboljse = vrednost
                                najboljsa_poteza = p
                                B = min(B,vrednost_najboljse)
                                if B <= A:
                                    break
                assert (najboljsa_poteza is not None), "minimax: izračunana poteza je None"
                return (najboljsa_poteza, vrednost_najboljse)
        
    # izračuna vrednost pozicije, zankrat le izpiše koliko so vredna posamezna polja
    def hevristika(self,igralec, tabla):
        vrednosti= [[4000, -20, 10, -10, -5, -10, -20, 4000], [-20, -50, -2, -2, -2, -2, -50, -20],[10, -2, -1, -1, -1, -1, -2, 10], [5, -2, -1, -1, -1, -1, -2, 5],
            [5, -2, -1, -1, -1, -1, -2, 5], [10, -2, -1, -1, -1, -1, -2, 10], [-20, -50, -2, -2, -2, -2, -50, -20], [4000, -20, -10, -5, -5, -10, -20, 4000]]
        ocena = 0
        for x in range(8):
            for y in range(8):
                if tabla.ploskev[x][y] == tabla.protagonist(igralec):
                    ocena += vrednosti[x][y]
                elif tabla.ploskev[x][y] == tabla.antagonist(igralec):
                    ocena -= vrednosti[x][y]
        return ocena
