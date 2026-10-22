#klasa za cvor stabla
class Cvor:
    def __init__(self,vrednost,roditelj,deca) -> None:
        self._vrednost = vrednost
        self._roditelj = roditelj
        self._deca = deca

    @property
    def vrednost(self):
        return self._vrednost
    @property
    def roditelj(self):
        return self._roditelj
    @property
    def deca(self):
        return self._deca
    @vrednost.setter
    def vrednost(self,vrednost):
        self._vrednost = vrednost
    @roditelj.setter
    def roditelj(self,roditelj):
        self._roditelj = roditelj
    @deca.setter
    def deca(self,deca):
        self._deca = deca

    #proverava da li je cvor koren
    def koren(self):
        if self._roditelj == None:
            return True
        return False
    
    #proverava da li je cvor list
    def list(self):
        if(len(self._deca) == 0):
            return True
        return False
    
    #dodaje dete cvoru
    def dodaj_dete(self,vrednost_deteta):
        novi_cvor= Cvor(vrednost_deteta,self,[])
        self._deca.append(novi_cvor)
        return novi_cvor

    #ispisuje cvor
    def __str__(self):
        return str(self._vrednost)

#klasa za red koji se koristi kod obilaska stabla po sirini
class Red:
    def __init__(self) -> None:
        self._elementi = []

    @property
    def elementi(self):
        return self._elementi
    @elementi.setter
    def elementi(self,elementi):
        self._elementi = elementi

    #dodaje element u red
    def dodaj(self,element):
        self._elementi.append(element)
    
    #izbacuje element iz reda
    def izbaci(self):
        return self._elementi.pop(0)

    #proverava da li je red prazan
    def prazan(self):
        return len(self._elementi) == 0
    
    #vraca duzinu reda
    def __len__(self):
        return len(self._elementi)
    
    #ispisuje red
    def __str__(self):
        return str(self._elementi)

#klasa za stablo
class Stablo:
    def __init__(self,vrednost) -> None:
        self._koren = Cvor(vrednost,None,[])

    @property
    def koren(self):
        return self._koren
    @koren.setter
    def koren(self,koren):
        self._koren = koren

    #vraca duzinu stabla(broj cvorova)
    def __len__(self):
        return self._duzina(self._koren)
    def _duzina(self,cvor):
        if cvor.list():
            return 1
        return 1 + sum(self._duzina(dete) for dete in cvor.deca)

    #vraća dubinu cvora(udaljenost od korena)
    def dubina(self,cvor):
        trenutni_cvor = cvor
        dubina = 1
        while not trenutni_cvor.koren():
            trenutni_cvor = trenutni_cvor.roditelj
            dubina += 1
        return dubina
    
    #vraća visinu stabla(udaljenost od korena do najudaljenijeg lista)
    def visina(self):
        return self._visina(self._koren)
    def _visina(self,cvor):
        if cvor.list():
            return 1
        else:
            return 1 + max(self._visina(dete) for dete in cvor.deca)

    #preorder obilazak stabla(koren,levo,desno) 
    def preorder(self):
        self._preorder(self._koren)
    def _preorder(self,cvor):
        print(cvor)
        for dete in cvor.deca:
            self._preorder(dete)

    #postorder obilazak stabla(levo,koren,desno)
    def postorder(self):
        self._postorder(self._koren)
    def _postorder(self,cvor):
        for dete in cvor.deca:
            self._postorder(dete)
        print(cvor)

    #obilazak stabla po sirini(koren,prvo deca korena,pa deca dece korena...)
    def po_sirini(self):
        red=Red()
        red.dodaj(self._koren)
        while not red.prazan():
            cvor=red.izbaci()
            print(cvor)
            for dete in cvor.deca:
                red.dodaj(dete)

    #vraca da li je stablo prazno
    def prazno(self):
        if self._koren == None:
            return True
        return False
    
    #vraca broj dece cvora
    def broj_dece(self,cvor):
        return len(cvor.deca)
    
    #vraca decu cvora
    def deca(self,cvor):
        for dete in cvor.deca:
            print(dete)

    #zamenjuje cvor sa novim cvorom
    def replace(self,stari,novi):
        for i in range(len(stari.roditelj.deca)):
            if stari.roditelj.deca[i] == stari:
                stari.roditelj.deca[i] = novi
                break
    
    #iteracija kroz stablo
    def __iter__(self):
        return self._iter(self._koren)
    def _iter(self,cvor):
        yield cvor
        for dete in cvor.deca:
            if not dete.list():
                yield from self._iter(dete)
            else:
                yield dete

    #ispisuje stablo
    def str(self):
        for cvor in self:
            print(cvor)