import pygame
pygame.init()
import os
import sys
import random
import copy
import ast
import time
from Stablo import *
from Konzola import *

#lokacija fajla
lokacija= os.path.realpath(os.path.dirname(__file__))

#tip igre, mora da se jede ili ne
mora_da_se_jede=None

#ciji je red da igra
moj_red=True

#da li kompjuter igra
kompjuter=True

#hash mapa za optimizaciju, jedna za stanje gde ne mora da se jede a druga gde mora
hash_optimizacija_ne_mora_jedenje={}
hash_optimizacija_mora_jedenje={}
#lista za cuvanje stanja, koristi se kod ucitavanja mape
stanja=[]
#da li postoji dama na tabli, koristi se kod kreiranja novih stanja u mapi
ima_dama=False

#da li ima neki token da moze da jede
ima_koji_moze_da_jede=False
#lista pozicija tokena koji mogu da jedu
tokeni_koji_mogu_da_jedu=[]
#da li je provereno ima li tokena koji mogu da jedu
provereno_jedenje=False

#da li je provereno pomeranje mojih tokena, ako nema pomeranja onda je kraj igre
provereno_pomeranje=False

#da li je doslo do restarta
restartovano=False

#klasa za polje table
class PoljeTable(pygame.sprite.Sprite):
    def __init__(self,slika):
        super().__init__()
        #ucitavanje slike iz foldera i postavljanje velicine
        self.slika=pygame.image.load(slika)
        velicina_slike=(sirina_prozora-100)//8
        self.slika=pygame.transform.scale(self.slika,(velicina_slike,velicina_slike))

#klasa za pozadinu
class Pozadina(pygame.sprite.Sprite):
    def __init__(self,slika):
        super().__init__()
        #ucitavanje slike iz foldera i postavljanje velicine
        self.slika=pygame.image.load(slika)
        self.slika=pygame.transform.scale(self.slika,(sirina_prozora,visina_prozora))

#klasa za token
class Token(pygame.sprite.Sprite):
    def __init__(self,slika,pozicija,moj_token):
        super().__init__()
        #ucitavanje slike iz datoteke i postavljanje velicine
        self.slika=pygame.image.load(slika)
        self.pozicija=pozicija
        #logicki atributi se koriste kod racunanja poteza kompjutera
        #ideja je da se pri racunu kompjutera igra odigrava na logickom nivou bez menjanja stvarnih atributa tokena
        self.logicka_pozicija=pozicija
        self.moj_token=moj_token
        self.kliknut=False
        self.dama=False
        velicina_slike=(sirina_prozora-100)//8
        self.slika=pygame.transform.scale(self.slika,(velicina_slike,velicina_slike))
        self.telo=self.slika.get_rect(topleft=self.pozicija)
        self.ima_pomeranje=False
        self.pojeden=False
        self.moguci_potezi=[]
        self.pozicije_za_jedenje={}
        self.logicka_dama=False
        self.sledece_pozicije={}

    #metoda za crtanje tokena
    def crtanje(self,pozicija):
        if self.moj_token and moj_red:
            self.provera_klika()

        if self.ima_pomeranje and self.moj_token:
            self.pomeranje_mog_tokena()
        if self.ima_pomeranje and not self.moj_token:
            self.pomeranje_protivnickog_tokena()

        if self.pojeden:
            self.smrt()
        
        prozor.blit(self.slika,pozicija)

    #metoda za pomeranje mog tokena
    def pomeranje_mog_tokena(self):
        global moj_red
        global kompjuter
        
        #provera da li ima krajnjih pozicija
        if len(krajnje_moje_pozicije)>0:
            moj_red=False
            if len(slike_moguci_potezi)>0:
                slike_moguci_potezi.clear()
            #pronalazak smera kretanja
            razlika_x=self.pozicija[0]-krajnje_moje_pozicije[0][0]
            razlika_y=self.pozicija[1]-krajnje_moje_pozicije[0][1]

            korak_x=0
            korak_y=0

            if razlika_x>0 and razlika_y>0:
                korak_x=-3
                korak_y=-3
            elif razlika_x>0 and razlika_y<0:
                korak_x=-3
                korak_y=3
            elif razlika_x<0 and razlika_y>0:
                korak_x=3
                korak_y=-3
            elif razlika_x<0 and razlika_y<0:
                korak_x=3
                korak_y=3

            #pomeranje tokena
            if self.pozicija!=krajnje_moje_pozicije[0]:
                #provera da token nije presao krajnju poziciju
                if abs(razlika_x)<2 or abs(razlika_y)<2:
                    self.pozicija=krajnje_moje_pozicije[0]
                    self.logicka_pozicija=krajnje_moje_pozicije[0]
                    self.telo=self.slika.get_rect(topleft=self.pozicija)
                else:
                    self.telo.move_ip(korak_x,korak_y)
                    self.pozicija=self.telo.topleft
                    self.logicka_pozicija=self.pozicija
            else:
                krajnje_moje_pozicije.pop(0)
        else:
            self.ima_pomeranje=False
            kompjuter=False

    #metoda za pomeranje protivnickog tokena
    def pomeranje_protivnickog_tokena(self):
        global moj_red
        global kompjuter
        global provereno_jedenje
        global provereno_pomeranje
        
        #provera da li ima krajnjih pozicija
        if len(krajnje_protivnicke_pozicije)>0:
            #pronalazak smera kretanja
            razlika_x=self.pozicija[0]-krajnje_protivnicke_pozicije[0][0]
            razlika_y=self.pozicija[1]-krajnje_protivnicke_pozicije[0][1]

            korak_x=0
            korak_y=0

            if razlika_x>0 and razlika_y>0:
                korak_x=-3
                korak_y=-3
            elif razlika_x>0 and razlika_y<0:
                korak_x=-3
                korak_y=3
            elif razlika_x<0 and razlika_y>0:
                korak_x=3
                korak_y=-3
            elif razlika_x<0 and razlika_y<0:
                korak_x=3
                korak_y=3

            #pomeranje tokena
            if self.pozicija!=krajnje_protivnicke_pozicije[0]:
                #provera da token nije presao krajnju poziciju
                if abs(razlika_x)<2 or abs(razlika_y)<2:
                    self.pozicija=krajnje_protivnicke_pozicije[0]
                    self.logicka_pozicija=krajnje_protivnicke_pozicije[0]
                    self.telo=self.slika.get_rect(topleft=self.pozicija)
                else:
                    self.telo.move_ip(korak_x,korak_y)
                    self.pozicija=self.telo.topleft
                    self.logicka_pozicija=self.pozicija
            else:
                krajnje_protivnicke_pozicije.pop(0)
        else:
            moj_red=True
            self.ima_pomeranje=False
            provereno_jedenje=False
            provereno_pomeranje=False
        
    #metoda koja proverava da li je token kliknut
    def provera_klika(self):
        pozicija_misa=pygame.mouse.get_pos()

        #provera da li je mis na tokenu
        if(self.telo.collidepoint(pozicija_misa) and not self.kliknut):
            #provera da li je token kliknut
            if(pygame.mouse.get_pressed()[0]):
                self.kliknut=True
                self.pravljenje_poteza(moji_tokeni,protivnicki_tokeni)

        if(pygame.mouse.get_pressed()[0]==False):
            self.kliknut=False
    
    #metoda koja proverava mogucnosti za pomeranje tokena
    def pravljenje_poteza(self,stanje_mojih_tokena,stanje_protivnickih_tokena,provera=False):
        global slike_moguci_potezi
        global pozicija_pritisnutog_tokena

        #brisanje pretodnih mogucnosti za pomeranje
        self.moguci_potezi.clear()
        self.pozicije_za_jedenje.clear()
        self.sledece_pozicije.clear()

        #dodela da je ovaj token kliknut ako su moj red i token
        if not igra_kompjuter:
            pozicija_pritisnutog_tokena=self.pozicija

        #ako ovaj token ne moze da jede nema potrebe da se bilo sta dalje proverava ako je mod igre da mora da se jede
        if ima_koji_moze_da_jede and self.logicka_pozicija not in tokeni_koji_mogu_da_jedu and mora_da_se_jede:
            slike_moguci_potezi.clear()
            return False

        #ako nje dama
        if(not self.logicka_dama):
            if not self.moj_token:
                dole_desno=(self.logicka_pozicija[0]+jedno_polje.slika.get_width(),self.logicka_pozicija[1]+jedno_polje.slika.get_height())
                dole_levo=(self.logicka_pozicija[0]-jedno_polje.slika.get_width(),self.logicka_pozicija[1]+jedno_polje.slika.get_height())
            else:
                gore_levo=(self.logicka_pozicija[0]-jedno_polje.slika.get_width(),self.logicka_pozicija[1]-jedno_polje.slika.get_height())
                gore_desno=(self.logicka_pozicija[0]+jedno_polje.slika.get_width(),self.logicka_pozicija[1]-jedno_polje.slika.get_height())
            slike_moguci_potezi.clear()

            #provera da token nije blokiran svojim tokenom
            blokiran_gore_levo=False
            blokiran_gore_desno=False
            blokiran_dole_levo=False
            blokiran_dole_desno=False

            #ako je token blokiran sa obe strane svojim znaci da ne moze da se pomeri i nema potrebe da se proverava dalje
            #ali kod protivnickog se prvo proverava da li je blokiran sa obe strane protivnickim pa mora da se proveri dodatno da li je blokiran sa obe strane svojim
            bio_blokiran=False
            for tokeni in stanje_mojih_tokena.values():
                if not self.moj_token:
                    if tokeni.logicka_pozicija==dole_levo:
                        blokiran_dole_levo=True
                        bio_blokiran=True
                    if tokeni.logicka_pozicija==dole_desno:
                        blokiran_dole_desno=True
                        bio_blokiran=True
                else:
                    if tokeni.logicka_pozicija==gore_levo:
                        blokiran_gore_levo=True
                    if tokeni.logicka_pozicija==gore_desno:
                        blokiran_gore_desno=True
                    if blokiran_gore_levo and blokiran_gore_desno:
                        return False
                
            for tokeni in stanje_protivnickih_tokena.values():
                if not self.moj_token:
                    if tokeni.logicka_pozicija==dole_levo:
                        blokiran_dole_levo=True
                    if tokeni.logicka_pozicija==dole_desno:
                        blokiran_dole_desno=True
                    if blokiran_dole_levo and blokiran_dole_desno and not bio_blokiran:
                        return False
                else:
                    if tokeni.logicka_pozicija==gore_levo:
                        blokiran_gore_levo=True
                    if tokeni.logicka_pozicija==gore_desno:
                        blokiran_gore_desno=True

            #provera da li je token blokiran protivnickim i da li moze da jede, provere sluze da vide da li ima bar jedan potez i slicno, ne mora sve da se proverava
            if not provera:
                self.provera_preskakanja(self.logicka_pozicija,stanje_mojih_tokena,stanje_protivnickih_tokena,True)
            else:
                ima_jedenje=self.provera_preskakanja(self.logicka_pozicija,stanje_mojih_tokena,stanje_protivnickih_tokena,True,[],True)
                if ima_jedenje:
                    return True

            #crtanje mogucnosti za pomeranje na prazno polje ako nema poteza za jedenje kod moda igre da mora da se jede
            if mora_da_se_jede==False or not ima_koji_moze_da_jede:
                if not igra_kompjuter:
                    if(self.pozicija[0]>pocetna_sirina and not blokiran_gore_levo):
                        if provera:
                            return True
                        if gore_levo[1]!=pocetna_visina:
                            potez1=PotezPolje(lokacija+"\Slike\Zeleno polje.png",gore_levo)
                        else:
                            potez1=PotezPolje(lokacija+"\Slike\Zuto polje.png",gore_levo)
                        slike_moguci_potezi[gore_levo]=potez1
                        self.moguci_potezi.append(gore_levo)
                    if(self.pozicija[0]<pocetna_sirina+jedno_polje.slika.get_width()*7 and not blokiran_gore_desno):
                        if provera:
                            return True
                        if gore_desno[1]!=pocetna_visina:
                            potez2=PotezPolje(lokacija+"\Slike\Zeleno polje.png",gore_desno)
                        else:
                            potez2=PotezPolje(lokacija+"\Slike\Zuto polje.png",gore_desno)
                        slike_moguci_potezi[gore_desno]=potez2
                        self.moguci_potezi.append(gore_desno)
                elif not self.moj_token:
                    if(self.logicka_pozicija[0]>pocetna_sirina  and not blokiran_dole_levo):
                        self.moguci_potezi.append(dole_levo)
                    if(self.logicka_pozicija[0]<pocetna_sirina+jedno_polje.slika.get_width()*7 and not blokiran_dole_desno):
                        self.moguci_potezi.append(dole_desno)
                else:
                    if(self.logicka_pozicija[0]>pocetna_sirina and not blokiran_gore_levo):
                        self.moguci_potezi.append(gore_levo)
                    if(self.logicka_pozicija[0]<pocetna_sirina+jedno_polje.slika.get_width()*7 and not blokiran_gore_desno):
                        self.moguci_potezi.append(gore_desno)
        else:
            gore_levo=(self.logicka_pozicija[0]-jedno_polje.slika.get_width(),self.logicka_pozicija[1]-jedno_polje.slika.get_height())
            gore_desno=(self.logicka_pozicija[0]+jedno_polje.slika.get_width(),self.logicka_pozicija[1]-jedno_polje.slika.get_height())
            dole_levo=(self.logicka_pozicija[0]-jedno_polje.slika.get_width(),self.logicka_pozicija[1]+jedno_polje.slika.get_height())
            dole_desno=(self.logicka_pozicija[0]+jedno_polje.slika.get_width(),self.logicka_pozicija[1]+jedno_polje.slika.get_height())
            slike_moguci_potezi.clear()

            #provera da token nije blokiran svojim tokenom
            blokiran_gore_levo=False
            blokiran_gore_desno=False
            blokiran_dole_levo=False
            blokiran_dole_desno=False
            bio_blokiran=False
            for tokeni in stanje_mojih_tokena.values():
                if tokeni.logicka_pozicija==gore_levo:
                    blokiran_gore_levo=True
                    bio_blokiran=True
                if tokeni.logicka_pozicija==gore_desno:
                    blokiran_gore_desno=True
                    bio_blokiran=True
                if tokeni.logicka_pozicija==dole_levo:
                    blokiran_dole_levo=True
                    bio_blokiran=True
                if tokeni.logicka_pozicija==dole_desno:
                    blokiran_dole_desno=True
                    bio_blokiran=True
                if blokiran_gore_levo and blokiran_gore_desno and blokiran_dole_levo and blokiran_dole_desno and self.moj_token:
                    return False
                
            for tokeni in stanje_protivnickih_tokena.values():
                if tokeni.logicka_pozicija==gore_levo:
                    blokiran_gore_levo=True
                if tokeni.logicka_pozicija==gore_desno:
                    blokiran_gore_desno=True
                if tokeni.logicka_pozicija==dole_levo:
                    blokiran_dole_levo=True
                if tokeni.logicka_pozicija==dole_desno:
                    blokiran_dole_desno=True
                if blokiran_gore_levo and blokiran_gore_desno and blokiran_dole_levo and blokiran_dole_desno and not self.moj_token and not bio_blokiran:
                    return False
            
            #provera da li je token blokiran protivnickim i da li moze da jede
            if not provera:
                self.provera_preskakanja_dama(self.logicka_pozicija,stanje_mojih_tokena,stanje_protivnickih_tokena, True)
            else:
                ima_jedenje=self.provera_preskakanja_dama(self.logicka_pozicija,stanje_mojih_tokena,stanje_protivnickih_tokena, True,[],True)
                if ima_jedenje:
                    return True

            #crtanje mogucnosti za pomeranje na prazno polje ako nema poteza za jedenje kod moda igre da mora da se jede
            if mora_da_se_jede==False or not ima_koji_moze_da_jede:
                if not igra_kompjuter:
                    if provera:
                        return True
                    if(self.pozicija[0]>pocetna_sirina and not blokiran_gore_levo and self.pozicija[1]>pocetna_visina):
                        potez1=PotezPolje(lokacija+"\Slike\Zeleno polje.png",gore_levo)
                        slike_moguci_potezi[gore_levo]=potez1
                    if(self.pozicija[0]<pocetna_sirina+jedno_polje.slika.get_width()*7 and not blokiran_gore_desno and self.pozicija[1]>pocetna_visina):
                        potez2=PotezPolje(lokacija+"\Slike\Zeleno polje.png",gore_desno)
                        slike_moguci_potezi[gore_desno]=potez2
                    if(self.pozicija[0]>pocetna_sirina  and not blokiran_dole_levo and self.pozicija[1]<pocetna_visina+jedno_polje.slika.get_height()*7):
                        potez3=PotezPolje(lokacija+"\Slike\Zeleno polje.png",dole_levo)
                        slike_moguci_potezi[dole_levo]=potez3
                    if(self.pozicija[0]<pocetna_sirina+jedno_polje.slika.get_width()*7 and not blokiran_dole_desno and self.pozicija[1]<pocetna_visina+jedno_polje.slika.get_height()*7):
                        potez4=PotezPolje(lokacija+"\Slike\Zeleno polje.png",dole_desno)
                        slike_moguci_potezi[dole_desno]=potez4
                else:
                    if(self.logicka_pozicija[0]>pocetna_sirina and not blokiran_dole_levo and self.logicka_pozicija[1]<pocetna_visina+jedno_polje.slika.get_height()*7):
                        self.moguci_potezi.append(dole_levo)
                    if(self.logicka_pozicija[0]<pocetna_sirina+jedno_polje.slika.get_width()*7 and not blokiran_dole_desno and self.logicka_pozicija[1]<pocetna_visina+jedno_polje.slika.get_height()*7):
                        self.moguci_potezi.append(dole_desno)
                    if(self.logicka_pozicija[0]>pocetna_sirina and not blokiran_gore_levo and self.logicka_pozicija[1]>pocetna_visina):
                        self.moguci_potezi.append(gore_levo)
                    if(self.logicka_pozicija[0]<pocetna_sirina+jedno_polje.slika.get_width()*7 and not blokiran_gore_desno and self.logicka_pozicija[1]>pocetna_visina):
                        self.moguci_potezi.append(gore_desno)  
    
    # Pamti sve figure pojedene tokom celog niza preskakanja, ne samo poslednju.
    def zapamti_jedenje(self, pozicija, prethodni_koraci, preskoceni, odrediste):
        putanja = prethodni_koraci + [pozicija]
        pojedeni = [
            ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2)
            for a, b in zip(putanja, putanja[1:])
        ]
        pojedeni.append(preskoceni)
        self.pozicije_za_jedenje[odrediste] = pojedeni

    #metoda koja crta mogucnosti za jedenje standardnog tokena
    def provera_preskakanja(self,pozicija,stanje_mojih_tokena,stanje_protivnickih_tokena, prvi=False,prethodni_koraci=[],provera=False):
        global slike_moguci_potezi

        #crta se mogucnost za jedenje, prvi put se samo racuna pa se ne crta
        if not prvi:
            if not igra_kompjuter:
                potez=PotezPolje(lokacija+"\Slike\Crveno polje.png",pozicija)
                for pozicije in prethodni_koraci:
                    potez.prethodni_koraci.append(pozicije)
                slike_moguci_potezi[pozicija]=potez
            else:
                #dodavanje pozicije kao sledeci korak za animaciju
                self.sledece_pozicije[pozicija]=prethodni_koraci
                self.moguci_potezi.append(pozicija)

        gore_levo=(pozicija[0]-jedno_polje.slika.get_width(),pozicija[1]-jedno_polje.slika.get_height())
        gore_desno=(pozicija[0]+jedno_polje.slika.get_width(),pozicija[1]-jedno_polje.slika.get_height())
        dole_levo=(pozicija[0]-jedno_polje.slika.get_width(),pozicija[1]+jedno_polje.slika.get_height())
        dole_desno=(pozicija[0]+jedno_polje.slika.get_width(),pozicija[1]+jedno_polje.slika.get_height())
       
        #provera da li je token blokiran protivnickim i da li moze da jede
        protivnik_gore_levo=False
        protivnik_gore_desno=False
        protivnik_dole_levo=False
        protivnik_dole_desno=False
        moze_jedenje_gore_levo=True
        moze_jedenje_gore_desno=True
        moze_jedenje_dole_levo=True
        moze_jedenje_dole_desno=True
        if self.moj_token:
            for tokeni in stanje_protivnickih_tokena.values():
                if tokeni.logicka_pozicija==gore_levo and gore_levo[0]-jedno_polje.slika.get_width()>=pocetna_sirina and not protivnik_gore_levo:
                    protivnik_gore_levo=True
                    #ako je token uz ivicu ne moze da se jede
                    if gore_levo[1]-jedno_polje.slika.get_height()<pocetna_visina:
                        moze_jedenje_gore_levo=False
                    #ako je token blokiran svojim tokenom ne moze da se jede
                    if moze_jedenje_gore_levo:
                        for tokeni1 in stanje_mojih_tokena.values():
                            if tokeni1.logicka_pozicija==(gore_levo[0]-jedno_polje.slika.get_width(),gore_levo[1]-jedno_polje.slika.get_height()):
                                moze_jedenje_gore_levo=False
                                break
                    #ako je token blokiran protivnickim tokenom ne moze da se jede
                    if moze_jedenje_gore_levo:
                        for tokeni1 in stanje_protivnickih_tokena.values():
                            if tokeni1.logicka_pozicija==(gore_levo[0]-jedno_polje.slika.get_width(),gore_levo[1]-jedno_polje.slika.get_height()):
                                moze_jedenje_gore_levo=False
                                break
                if tokeni.logicka_pozicija==gore_desno and gore_desno[0]+jedno_polje.slika.get_width()<pocetna_sirina+jedno_polje.slika.get_width()*8 and not protivnik_gore_desno:
                    protivnik_gore_desno=True
                    if gore_desno[1]-jedno_polje.slika.get_height()<pocetna_visina:
                        moze_jedenje_gore_desno=False
                    if moze_jedenje_gore_desno:
                        for tokeni1 in stanje_mojih_tokena.values():
                            if tokeni1.logicka_pozicija==(gore_desno[0]+jedno_polje.slika.get_width(),gore_desno[1]-jedno_polje.slika.get_height()):
                                moze_jedenje_gore_desno=False
                                break
                    if moze_jedenje_gore_desno:
                        for tokeni1 in stanje_protivnickih_tokena.values():
                            if tokeni1.logicka_pozicija==(gore_desno[0]+jedno_polje.slika.get_width(),gore_desno[1]-jedno_polje.slika.get_height()):
                                moze_jedenje_gore_desno=False
                if protivnik_gore_levo and protivnik_gore_desno:
                    break
            
            if not protivnik_gore_levo and not protivnik_gore_desno:
                return False
            if not protivnik_gore_levo:
                moze_jedenje_gore_levo=False
            if not protivnik_gore_desno:
                moze_jedenje_gore_desno=False
            if not moze_jedenje_gore_levo and not moze_jedenje_gore_desno:
                return False

            #ako je token blokiran protivnickim tokenom ali posle njega je prazno polje moze da se jede
            if moze_jedenje_gore_levo:
                if provera:
                    return True
                self.zapamti_jedenje(pozicija, prethodni_koraci, gore_levo, (gore_levo[0]-jedno_polje.slika.get_width(),gore_levo[1]-jedno_polje.slika.get_height()))
                self.provera_preskakanja((gore_levo[0]-jedno_polje.slika.get_width(),gore_levo[1]-jedno_polje.slika.get_height()),stanje_mojih_tokena,stanje_protivnickih_tokena, False,prethodni_koraci+[pozicija])
            if moze_jedenje_gore_desno:
                if provera:
                    return True
                self.zapamti_jedenje(pozicija, prethodni_koraci, gore_desno, (gore_desno[0]+jedno_polje.slika.get_width(),gore_desno[1]-jedno_polje.slika.get_height()))
                self.provera_preskakanja((gore_desno[0]+jedno_polje.slika.get_width(),gore_desno[1]-jedno_polje.slika.get_height()),stanje_mojih_tokena, stanje_protivnickih_tokena, False,prethodni_koraci+[pozicija])
            return True
        else:
            #provera da li protivnicki token moze da jede, slicno kao kod mog tokena
            for tokeni in stanje_mojih_tokena.values():
                if tokeni.logicka_pozicija==dole_levo and dole_levo[0]-jedno_polje.slika.get_width()>=pocetna_sirina and not protivnik_dole_levo:
                    protivnik_dole_levo=True
                    if dole_levo[1]+jedno_polje.slika.get_height()>pocetna_visina+jedno_polje.slika.get_height()*7:
                        moze_jedenje_dole_levo=False
                    if moze_jedenje_dole_levo:
                        for tokeni1 in stanje_mojih_tokena.values():
                            if tokeni1.logicka_pozicija==(dole_levo[0]-jedno_polje.slika.get_width(),dole_levo[1]+jedno_polje.slika.get_height()):
                                moze_jedenje_dole_levo=False
                                break
                    if moze_jedenje_dole_levo:
                        for tokeni1 in stanje_protivnickih_tokena.values():
                            if tokeni1.logicka_pozicija==(dole_levo[0]-jedno_polje.slika.get_width(),dole_levo[1]+jedno_polje.slika.get_height()):
                                moze_jedenje_dole_levo=False
                                break
                if tokeni.logicka_pozicija==dole_desno and dole_desno[0]+jedno_polje.slika.get_width()<pocetna_sirina+jedno_polje.slika.get_width()*8 and not protivnik_dole_desno:
                    protivnik_dole_desno=True
                    if dole_desno[1]+jedno_polje.slika.get_height()>pocetna_visina+jedno_polje.slika.get_height()*7:
                        moze_jedenje_dole_desno=False
                    if moze_jedenje_dole_desno:
                        for tokeni1 in stanje_mojih_tokena.values():
                            if tokeni1.logicka_pozicija==(dole_desno[0]+jedno_polje.slika.get_width(),dole_desno[1]+jedno_polje.slika.get_height()):
                                moze_jedenje_dole_desno=False
                                break
                    if moze_jedenje_dole_desno:
                        for tokeni1 in stanje_protivnickih_tokena.values():
                            if tokeni1.logicka_pozicija==(dole_desno[0]+jedno_polje.slika.get_width(),dole_desno[1]+jedno_polje.slika.get_height()):
                                moze_jedenje_dole_desno=False
                                break
                if protivnik_dole_levo and protivnik_dole_desno:
                    break

            if not protivnik_dole_levo and not protivnik_dole_desno:
                return False
            if not protivnik_dole_levo:
                moze_jedenje_dole_levo=False
            if not protivnik_dole_desno:
                moze_jedenje_dole_desno=False
            if not moze_jedenje_dole_levo and not moze_jedenje_dole_desno:
                return False
            
            #ako je token blokiran protivnickim tokenom ali posle njega je prazno polje moze da se jede
            if moze_jedenje_dole_levo:
                if provera:
                    return True
                self.zapamti_jedenje(pozicija, prethodni_koraci, dole_levo, (dole_levo[0]-jedno_polje.slika.get_width(),dole_levo[1]+jedno_polje.slika.get_height()))
                self.provera_preskakanja((dole_levo[0]-jedno_polje.slika.get_width(),dole_levo[1]+jedno_polje.slika.get_height()),stanje_mojih_tokena,stanje_protivnickih_tokena, False,prethodni_koraci+[pozicija])
            if moze_jedenje_dole_desno:
                if provera:
                    return True
                self.zapamti_jedenje(pozicija, prethodni_koraci, dole_desno, (dole_desno[0]+jedno_polje.slika.get_width(),dole_desno[1]+jedno_polje.slika.get_height()))
                self.provera_preskakanja((dole_desno[0]+jedno_polje.slika.get_width(),dole_desno[1]+jedno_polje.slika.get_height()),stanje_mojih_tokena,stanje_protivnickih_tokena, False,prethodni_koraci+[pozicija])
            return True
    
    #metoda koja crta mogucnosti za jedenje dame, slicno kao kod standardnog tokena
    def provera_preskakanja_dama(self,pozicija,stanje_mojih_tokena,stanje_protivnickih_tokena, prvi=False,prethodni_koraci=[],provera=False):
        global slike_moguci_potezi

        #crta se mogucnost za jedenje
        if not prvi:
            if not igra_kompjuter:
                potez=PotezPolje(lokacija+"\Slike\Crveno polje.png",pozicija)
                for pozicije in prethodni_koraci:
                    potez.prethodni_koraci.append(pozicije)
                slike_moguci_potezi[pozicija]=potez
            else:
                #dodavanje pozicije kao sledeci korak za animaciju
                self.sledece_pozicije[pozicija]=prethodni_koraci
                self.moguci_potezi.append(pozicija)

        gore_levo=(pozicija[0]-jedno_polje.slika.get_width(),pozicija[1]-jedno_polje.slika.get_height())
        gore_desno=(pozicija[0]+jedno_polje.slika.get_width(),pozicija[1]-jedno_polje.slika.get_height())
        dole_levo=(pozicija[0]-jedno_polje.slika.get_width(),pozicija[1]+jedno_polje.slika.get_height())
        dole_desno=(pozicija[0]+jedno_polje.slika.get_width(),pozicija[1]+jedno_polje.slika.get_height())
       
        #provera da li je token blokiran protivnickim i da li moze da jede
        protivnik_gore_levo=False
        protivnik_gore_desno=False
        protivnik_dole_levo=False
        protivnik_dole_desno=False
        moze_jedenje_gore_levo=True
        moze_jedenje_gore_desno=True
        moze_jedenje_dole_levo=True
        moze_jedenje_dole_desno=True
        if self.moj_token:
            for tokeni in stanje_protivnickih_tokena.values():
                if tokeni.logicka_pozicija==gore_levo and gore_levo[0]-jedno_polje.slika.get_width()>=pocetna_sirina and not protivnik_gore_levo:
                    protivnik_gore_levo=True
                    if gore_levo[1]-jedno_polje.slika.get_height()<pocetna_visina:
                        moze_jedenje_gore_levo=False
                    if moze_jedenje_gore_levo:
                        for tokeni1 in stanje_mojih_tokena.values():
                            if tokeni1.logicka_pozicija==(gore_levo[0]-jedno_polje.slika.get_width(),gore_levo[1]-jedno_polje.slika.get_height()):
                                moze_jedenje_gore_levo=False
                                break
                    if moze_jedenje_gore_levo:
                        for tokeni1 in stanje_protivnickih_tokena.values():
                            if tokeni1.logicka_pozicija==(gore_levo[0]-jedno_polje.slika.get_width(),gore_levo[1]-jedno_polje.slika.get_height()):
                                moze_jedenje_gore_levo=False
                                break
                if tokeni.logicka_pozicija==gore_desno and gore_desno[0]+jedno_polje.slika.get_width()<pocetna_sirina+jedno_polje.slika.get_width()*8 and not protivnik_gore_desno:
                    protivnik_gore_desno=True
                    if gore_desno[1]-jedno_polje.slika.get_height()<pocetna_visina:
                        moze_jedenje_gore_desno=False
                    if moze_jedenje_gore_desno:
                        for tokeni1 in stanje_mojih_tokena.values():
                            if tokeni1.logicka_pozicija==(gore_desno[0]+jedno_polje.slika.get_width(),gore_desno[1]-jedno_polje.slika.get_height()):
                                moze_jedenje_gore_desno=False
                                break
                    if moze_jedenje_gore_desno:
                        for tokeni1 in stanje_protivnickih_tokena.values():
                            if tokeni1.logicka_pozicija==(gore_desno[0]+jedno_polje.slika.get_width(),gore_desno[1]-jedno_polje.slika.get_height()):
                                moze_jedenje_gore_desno=False
                                break
                if tokeni.logicka_pozicija==dole_levo and dole_levo[0]-jedno_polje.slika.get_width()>=pocetna_sirina and not protivnik_dole_levo:
                    protivnik_dole_levo=True
                    if dole_levo[1]+jedno_polje.slika.get_height()>pocetna_visina+jedno_polje.slika.get_height()*7:
                        moze_jedenje_dole_levo=False
                    if moze_jedenje_dole_levo:
                        for tokeni1 in stanje_mojih_tokena.values():
                            if tokeni1.logicka_pozicija==(dole_levo[0]-jedno_polje.slika.get_width(),dole_levo[1]+jedno_polje.slika.get_height()):
                                moze_jedenje_dole_levo=False
                                break
                    if moze_jedenje_dole_levo:
                        for tokeni1 in stanje_protivnickih_tokena.values():
                            if tokeni1.logicka_pozicija==(dole_levo[0]-jedno_polje.slika.get_width(),dole_levo[1]+jedno_polje.slika.get_height()):
                                moze_jedenje_dole_levo=False
                                break
                if tokeni.logicka_pozicija==dole_desno and dole_desno[0]+jedno_polje.slika.get_width()<pocetna_sirina+jedno_polje.slika.get_width()*8 and not protivnik_dole_desno:
                    protivnik_dole_desno=True
                    if dole_desno[1]+jedno_polje.slika.get_height()>pocetna_visina+jedno_polje.slika.get_height()*7:
                        moze_jedenje_dole_desno=False
                    if moze_jedenje_dole_desno:
                        for tokeni1 in stanje_mojih_tokena.values():
                            if tokeni1.logicka_pozicija==(dole_desno[0]+jedno_polje.slika.get_width(),dole_desno[1]+jedno_polje.slika.get_height()):
                                moze_jedenje_dole_desno=False
                                break
                    if moze_jedenje_dole_desno:
                        for tokeni1 in stanje_protivnickih_tokena.values():
                            if tokeni1.logicka_pozicija==(dole_desno[0]+jedno_polje.slika.get_width(),dole_desno[1]+jedno_polje.slika.get_height()):
                                moze_jedenje_dole_desno=False
                                break
                if protivnik_gore_levo and protivnik_gore_desno and protivnik_dole_levo and protivnik_dole_desno:
                    break
        else:
            for tokeni in stanje_mojih_tokena.values():
                if tokeni.logicka_pozicija==dole_levo and dole_levo[0]-jedno_polje.slika.get_width()>=pocetna_sirina and not protivnik_dole_levo:
                    protivnik_dole_levo=True
                    if dole_levo[1]+jedno_polje.slika.get_height()>pocetna_visina+jedno_polje.slika.get_height()*7:
                        moze_jedenje_dole_levo=False
                    if moze_jedenje_dole_levo:
                        for tokeni1 in stanje_mojih_tokena.values():
                            if tokeni1.logicka_pozicija==(dole_levo[0]-jedno_polje.slika.get_width(),dole_levo[1]+jedno_polje.slika.get_height()):
                                moze_jedenje_dole_levo=False
                                break
                    if moze_jedenje_dole_levo:
                        for tokeni1 in stanje_protivnickih_tokena.values():
                            if tokeni1.logicka_pozicija==(dole_levo[0]-jedno_polje.slika.get_width(),dole_levo[1]+jedno_polje.slika.get_height()):
                                moze_jedenje_dole_levo=False
                                break
                if tokeni.logicka_pozicija==dole_desno and dole_desno[0]+jedno_polje.slika.get_width()<pocetna_sirina+jedno_polje.slika.get_width()*8 and not protivnik_dole_desno:
                    protivnik_dole_desno=True
                    if dole_desno[1]+jedno_polje.slika.get_height()>pocetna_visina+jedno_polje.slika.get_height()*7:
                        moze_jedenje_dole_desno=False
                    if moze_jedenje_dole_desno:
                        for tokeni1 in stanje_mojih_tokena.values():
                            if tokeni1.logicka_pozicija==(dole_desno[0]+jedno_polje.slika.get_width(),dole_desno[1]+jedno_polje.slika.get_height()):
                                moze_jedenje_dole_desno=False
                                break
                    if moze_jedenje_dole_desno:
                        for tokeni1 in stanje_protivnickih_tokena.values():
                            if tokeni1.logicka_pozicija==(dole_desno[0]+jedno_polje.slika.get_width(),dole_desno[1]+jedno_polje.slika.get_height()):
                                moze_jedenje_dole_desno=False
                                break
                if tokeni.logicka_pozicija==gore_levo and gore_levo[0]-jedno_polje.slika.get_width()>=pocetna_sirina and not protivnik_gore_levo:
                    protivnik_gore_levo=True
                    if gore_levo[1]-jedno_polje.slika.get_height()<pocetna_visina:
                        moze_jedenje_gore_levo=False
                    if moze_jedenje_gore_levo:
                        for tokeni1 in stanje_mojih_tokena.values():
                            if tokeni1.logicka_pozicija==(gore_levo[0]-jedno_polje.slika.get_width(),gore_levo[1]-jedno_polje.slika.get_height()):
                                moze_jedenje_gore_levo=False
                                break
                    if moze_jedenje_gore_levo:
                        for tokeni1 in stanje_protivnickih_tokena.values():
                            if tokeni1.logicka_pozicija==(gore_levo[0]-jedno_polje.slika.get_width(),gore_levo[1]-jedno_polje.slika.get_height()):
                                moze_jedenje_gore_levo=False
                                break
                if tokeni.logicka_pozicija==gore_desno and gore_desno[0]+jedno_polje.slika.get_width()<pocetna_sirina+jedno_polje.slika.get_width()*8 and not protivnik_gore_desno:
                    protivnik_gore_desno=True
                    if gore_desno[1]-jedno_polje.slika.get_height()<pocetna_visina:
                        moze_jedenje_gore_desno=False
                    if moze_jedenje_gore_desno:
                        for tokeni1 in stanje_mojih_tokena.values():
                            if tokeni1.logicka_pozicija==(gore_desno[0]+jedno_polje.slika.get_width(),gore_desno[1]-jedno_polje.slika.get_height()):
                                moze_jedenje_gore_desno=False
                                break
                    if moze_jedenje_gore_desno:
                        for tokeni1 in stanje_protivnickih_tokena.values():
                            if tokeni1.logicka_pozicija==(gore_desno[0]+jedno_polje.slika.get_width(),gore_desno[1]-jedno_polje.slika.get_height()):
                                moze_jedenje_gore_desno=False
                                break
                    if protivnik_gore_levo and protivnik_gore_desno and protivnik_dole_levo and protivnik_dole_desno:
                        break

        if not protivnik_gore_levo and not protivnik_gore_desno and not protivnik_dole_levo and not protivnik_dole_desno:
            return False
        if not protivnik_gore_levo:
            moze_jedenje_gore_levo=False
        if not protivnik_gore_desno:
            moze_jedenje_gore_desno=False
        if not protivnik_dole_levo:
            moze_jedenje_dole_levo=False
        if not protivnik_dole_desno:
            moze_jedenje_dole_desno=False
        if not moze_jedenje_gore_levo and not moze_jedenje_gore_desno and not moze_jedenje_dole_levo and not moze_jedenje_dole_desno:
            return False
        
        #ako je token blokiran protivnickim tokenom ali posle njega je prazno polje moze da se jede
        if moze_jedenje_gore_levo:
            if provera:
                return True
            self.zapamti_jedenje(pozicija, prethodni_koraci, gore_levo, (gore_levo[0]-jedno_polje.slika.get_width(),gore_levo[1]-jedno_polje.slika.get_height()))
            #namestanje da ne dodje do beskonacne petlje jer dama moze da jede u svim pravcima tako sto obrisemo logicki pojeden token
            novo_stanje_mojih_tokena=stanje_mojih_tokena.copy()
            novo_stanje_protivnickih_tokena=stanje_protivnickih_tokena.copy()
            if self.moj_token:
                novo_stanje_protivnickih_tokena.pop(gore_levo)
            else:
                novo_stanje_mojih_tokena.pop(gore_levo)
            self.provera_preskakanja_dama((gore_levo[0]-jedno_polje.slika.get_width(),gore_levo[1]-jedno_polje.slika.get_height()),novo_stanje_mojih_tokena,novo_stanje_protivnickih_tokena,False,prethodni_koraci+[pozicija])
        if moze_jedenje_gore_desno:
            if provera:
                return True
            self.zapamti_jedenje(pozicija, prethodni_koraci, gore_desno, (gore_desno[0]+jedno_polje.slika.get_width(),gore_desno[1]-jedno_polje.slika.get_height()))
            #namestanje da ne dodje do beskonacne petlje jer dama moze da jede u svim pravcima
            novo_stanje_mojih_tokena=stanje_mojih_tokena.copy()
            novo_stanje_protivnickih_tokena=stanje_protivnickih_tokena.copy()
            if self.moj_token:
                novo_stanje_protivnickih_tokena.pop(gore_desno)
            else:
                novo_stanje_mojih_tokena.pop(gore_desno)
            self.provera_preskakanja_dama((gore_desno[0]+jedno_polje.slika.get_width(),gore_desno[1]-jedno_polje.slika.get_height()),novo_stanje_mojih_tokena,novo_stanje_protivnickih_tokena,False,prethodni_koraci+[pozicija])
        if moze_jedenje_dole_levo:
            if provera:
                return True
            self.zapamti_jedenje(pozicija, prethodni_koraci, dole_levo, (dole_levo[0]-jedno_polje.slika.get_width(),dole_levo[1]+jedno_polje.slika.get_height()))
            #namestanje da ne dodje do beskonacne petlje jer dama moze da jede u svim pravcima
            novo_stanje_mojih_tokena=stanje_mojih_tokena.copy()
            novo_stanje_protivnickih_tokena=stanje_protivnickih_tokena.copy()
            if self.moj_token:
                novo_stanje_protivnickih_tokena.pop(dole_levo)
            else:
                novo_stanje_mojih_tokena.pop(dole_levo)
            self.provera_preskakanja_dama((dole_levo[0]-jedno_polje.slika.get_width(),dole_levo[1]+jedno_polje.slika.get_height()),novo_stanje_mojih_tokena,novo_stanje_protivnickih_tokena,False,prethodni_koraci+[pozicija])
        if moze_jedenje_dole_desno:
            if provera:
                return True
            self.zapamti_jedenje(pozicija, prethodni_koraci, dole_desno, (dole_desno[0]+jedno_polje.slika.get_width(),dole_desno[1]+jedno_polje.slika.get_height()))
            #namestanje da ne dodje do beskonacne petlje jer dama moze da jede u svim pravcima
            novo_stanje_mojih_tokena=stanje_mojih_tokena.copy()
            novo_stanje_protivnickih_tokena=stanje_protivnickih_tokena.copy()
            if self.moj_token:
                novo_stanje_protivnickih_tokena.pop(dole_desno)
            else:
                novo_stanje_mojih_tokena.pop(dole_desno)
            self.provera_preskakanja_dama((dole_desno[0]+jedno_polje.slika.get_width(),dole_desno[1]+jedno_polje.slika.get_height()),novo_stanje_mojih_tokena,novo_stanje_protivnickih_tokena,False,prethodni_koraci+[pozicija])
        return True

    #metoda kada se token pojede
    def smrt(self):
        self.pojeden=True
        self.slika.set_alpha(self.slika.get_alpha()-15)
               
#klasa za polje na koje se moze pomeriti token
class PotezPolje(pygame.sprite.Sprite):
    def __init__(self,slika,pozicija):
        super().__init__()
        #ucitavanje slike iz foldera i postavljanje velicine
        self.slika=pygame.image.load(slika)
        self.pozicija=pozicija
        velicina_slike=(sirina_prozora-100)//8
        self.slika=pygame.transform.scale(self.slika,(velicina_slike,velicina_slike))
        self.prethodni_koraci=[]

    #metoda za crtanje polja
    def crtanje(self):
        self.provera_klika()

        prozor.blit(self.slika,self.pozicija)

    #metoda koja proverava da li je polje kliknuto
    def provera_klika(self):
        pozicija_misa=pygame.mouse.get_pos()
        telo=self.slika.get_rect(topleft=self.pozicija)

        #provera da li je mis na polju
        if(telo.collidepoint(pozicija_misa)):
            #provera da li je polje kliknuto
            if(pygame.mouse.get_pressed()[0]):
                self.klik()

    #ako je polje kliknuto token se pomeri na to polje
    def klik(self):
        global tokeni_koji_mogu_da_jedu
        tokeni_koji_mogu_da_jedu=[]

        token=moji_tokeni[pozicija_pritisnutog_tokena]
        token.ima_pomeranje=True
        self.prethodni_koraci.append(self.pozicija)
        for pozicije in self.prethodni_koraci:
            krajnje_moje_pozicije.append(pozicije)
        moji_tokeni.pop(pozicija_pritisnutog_tokena)
        moji_tokeni[self.pozicija]=token
        self.prethodni_koraci.clear()

#klasa za senku
class Senka(pygame.sprite.Sprite):
    def __init__(self,slika,sirina,visina):
        super().__init__()
        #ucitavanje slike iz foldera i postavljanje velicine
        self.slika=pygame.image.load(slika)
        self.slika=pygame.transform.scale(self.slika,(sirina,visina))

#klasa za dugme
class Dugme(pygame.sprite.Sprite):
    def __init__(self,slika,pozicija,vrednost):
        super().__init__()
        #ucitavanje slike iz foldera i postavljanje velicine
        self.slika=pygame.image.load(slika)
        self.slika=pygame.transform.scale(self.slika,(150,100))
        self.rect=self.slika.get_rect(topleft=pozicija)
        self.vrednost=vrednost

    #metoda za crtanje dugmeta
    def crtanje(self):
        self.provera_klika()

        prozor.blit(self.slika,self.rect.topleft)
    
    #metoda koja proverava da li je dugme kliknuto
    def provera_klika(self):
        pozicija_misa=pygame.mouse.get_pos()

        #provera da li je mis na dugmetu
        if(self.rect.collidepoint(pozicija_misa)):
            #provera da li je dugme kliknuto
            if(pygame.mouse.get_pressed()[0]):
                self.klik()

    #ako je dugme kliknuto desava se odredjena radnja
    def klik(self):
        global mora_da_se_jede
        global igra_kompjuter
        global pozicija_pritisnutog_tokena
        global moj_red
        global restartovano
        global tokeni_koji_mogu_da_jedu
        global ima_koji_moze_da_jede
        global provereno_jedenje
        global provereno_pomeranje
        global slike_moguci_potezi
        global krajnje_moje_pozicije
        global krajnje_protivnicke_pozicije
        global moji_tokeni
        global protivnicki_tokeni
        global kompjuter

        if self.vrednost=="mora_da_se_jede":
            mora_da_se_jede=True
        elif self.vrednost=="ne_mora_da_se_jede":
            mora_da_se_jede=False
        elif self.vrednost=="izadji":
            #pozdrav i zatvaranje prozora
            prozor.blit(pozadina.slika,(0,0))
            font=pygame.font.Font(lokacija+"\Font\Piksel.ttf", 36)
            text=font.render("Dovidjenja",True,(255,215,0))
            textRect=text.get_rect()
            textRect.center=(sirina_prozora//2,visina_prozora//2)
            prozor.blit(text,textRect)
            pisanje_mape()
            pygame.display.flip()
            time.sleep(2)
            pygame.quit()
        elif self.vrednost=="restart":
            moji_tokeni.clear()
            protivnicki_tokeni.clear()
            slike_moguci_potezi.clear()
            krajnje_moje_pozicije.clear()
            krajnje_protivnicke_pozicije.clear()
            pozicija_pritisnutog_tokena=None
            igra_kompjuter=False
            moj_red=True
            restartovano=True
            tokeni_koji_mogu_da_jedu.clear()
            ima_koji_moze_da_jede=False
            provereno_jedenje=False
            provereno_pomeranje=False
            kompjuter=True
            crtanje_pocetak()

#dimenzije prozora
sirina_prozora=750
visina_prozora=750
#pravljenje prozora
prozor=pygame.display.set_mode((sirina_prozora, visina_prozora))

#pravljenje polja
jedno_polje=PoljeTable(lokacija+"\Slike\Belo polje.png")
drugo_polje=PoljeTable(lokacija+"\Slike\Braon polje.png")

#pravljenje senke
senka=Senka(lokacija+"\Slike\Senka.png",jedno_polje.slika.get_width()*8,jedno_polje.slika.get_height()//10)

#pravljenje pozadine
pozadina=Pozadina(lokacija+"\Slike\Pozadina.png")

#koordinate pocetnog polja
pocetna_sirina=sirina_prozora//2-jedno_polje.slika.get_width()*4
pocetna_visina=(visina_prozora+50)//2-jedno_polje.slika.get_height()*4

#recnici tokena i poteza, kljucevi su pozicije
moji_tokeni={}
protivnicki_tokeni={}
slike_moguci_potezi={}

#pozicija tokena koji je pritisnut
pozicija_pritisnutog_tokena=None

#krajnje pozicije tokena za pomeranje
krajnje_moje_pozicije=[]
krajnje_protivnicke_pozicije=[]

#dubina stabla za minimax algoritam
dubina=3

#da li igra kompjuter
igra_kompjuter=False

#pocetno cratnje pozadine, polja, tokena i senke
def crtanje_pocetak():
    #crtanje pozadine
    prozor.blit(pozadina.slika,(0,0))

    #pravljenje fonta
    font = pygame.font.Font(lokacija+"\Font\Piksel.ttf", 36)
    #pravljenje teksta
    text = font.render("Dobrodosli", True, (255, 215, 0))
    #pravljenje pravougaonika za tekst
    textRect = text.get_rect()
    #centriranje teksta
    textRect.center = (sirina_prozora // 2, visina_prozora // 2)
    #crtanje teksta
    prozor.blit(text, textRect)

    pygame.display.flip()
    time.sleep(2)

    #crtanje pozadine
    prozor.blit(pozadina.slika,(0,0))

    #pravljenje fonta
    font = pygame.font.Font(lokacija+"\Font\Piksel.ttf", 36)
    #pravljenje teksta
    text = font.render("Da li zelite da jedenje bude obavezno?", True, (255, 215, 0))
    #pravljenje pravougaonika za tekst
    textRect = text.get_rect()
    #centriranje teksta
    textRect.center = (sirina_prozora // 2, visina_prozora // 2-50)
    #crtanje teksta
    prozor.blit(text, textRect)

    #crtane dugmica za izbor da li mora da se jede ili ne
    mora_da_se_jede_dugme=Dugme(lokacija+"\Slike\Dugme da.png",(sirina_prozora//2-200,visina_prozora//2),"mora_da_se_jede")
    ne_mora_da_se_jede_dugme=Dugme(lokacija+"\Slike\Dugme ne.png",(sirina_prozora//2+50,visina_prozora//2),"ne_mora_da_se_jede")

    # pauza dok se ne klikne na dugme
    pritisnuo_dugme = False
    while not pritisnuo_dugme:
        for dogadjaj in pygame.event.get():
            #ako se klikne na X zatvara se prozor i prekida se igra
            if dogadjaj.type==pygame.QUIT:
                pygame.quit()
                break
            
            #crtanje dugmica
            mora_da_se_jede_dugme.crtanje()
            ne_mora_da_se_jede_dugme.crtanje()

            if dogadjaj.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if mora_da_se_jede_dugme.rect.collidepoint(mouse_pos):
                    pritisnuo_dugme = True
                elif ne_mora_da_se_jede_dugme.rect.collidepoint(mouse_pos):
                    pritisnuo_dugme = True

        #osvezavanje prozora
        pygame.display.flip()

    #crtanje pozaadine
    prozor.blit(pozadina.slika,(0,0))

    #crtanje senke
    prozor.blit(senka.slika,(pocetna_sirina,pocetna_visina+jedno_polje.slika.get_height()*8))

    #animacija crtanja table i tokena
    zavrseno=False
    transparentnost=0
    while not zavrseno:
        for dogadjaj in pygame.event.get():
            #ako se klikne na X zatvara se prozor i prekida se igra
            if dogadjaj.type==pygame.QUIT:
                pygame.quit()
                break

        if transparentnost==255:
            zavrseno=True

        for i in range(8):
            for j in range(8):
                pozicija=(pocetna_sirina+j*jedno_polje.slika.get_width(),pocetna_visina+i*jedno_polje.slika.get_height())
                if (i+j)%2==0:
                    #crtanje prvog polja
                    jedno_polje.slika.set_alpha(transparentnost)
                    prozor.blit(jedno_polje.slika,pozicija)
                else:
                    #crtanje drugog polja
                    drugo_polje.slika.set_alpha(transparentnost)
                    prozor.blit(drugo_polje.slika,pozicija)
                    #crtanje tokena
                    if(i<3):
                        token=Token(lokacija+"\Slike\Crveni token.png",pozicija,False)
                        token.slika.set_alpha(transparentnost)
                        token.crtanje(pozicija)
                        protivnicki_tokeni[pozicija]=token
                    elif(i>4):
                        token=Token(lokacija+"\Slike\Sivi token.png",pozicija,True)
                        token.slika.set_alpha(transparentnost)
                        token.crtanje(pozicija)
                        moji_tokeni[pozicija]=token

        transparentnost+=2.5

        #osvezavanje prozora
        pygame.display.flip()

#crtanje table
def crtanje_table():
    #crtanje pozadine
    prozor.blit(pozadina.slika,(0,0))

    for i in range(8):
        #crtanje senke od table
        if(i==7):
            prozor.blit(senka.slika,(pocetna_sirina,pocetna_visina+jedno_polje.slika.get_height()*8))
        for j in range(8):
            pozicija=(pocetna_sirina+j*jedno_polje.slika.get_width(),pocetna_visina+i*jedno_polje.slika.get_height())
            if (i+j)%2==0:
                #crtanje prvog polja
                prozor.blit(jedno_polje.slika,pozicija)
            else:
                #crtanje drugog polja
                prozor.blit(drugo_polje.slika,pozicija)

#igranje kompjutera
def igranje_kompjutera():
    global kompjuter
    global krajnje_protivnicke_pozicije
    global protivnicki_tokeni
    global igra_kompjuter
    global ima_dama

    igra_kompjuter=True

    #pravljenje stabla igre
    stablo_igre=Stablo([moji_tokeni,protivnicki_tokeni,-sys.maxsize-1,sys.maxsize])
    rezultat=pravljenje_stabla(moji_tokeni,protivnicki_tokeni,stablo_igre.koren,1,False)

    #stanje je stanje protivnickih tokena u koje treba da se dodje
    stanje={}
    #ako koren nema dece znaci da je igra gotova ili da je potez uzet iz mape za optimizaciju
    if len(stablo_igre.koren.deca)==0:
        if rezultat is None:
            kraj(True)
            return
        else:
            if not mora_da_se_jede:
                vrednost=hash_optimizacija_ne_mora_jedenje[rezultat[1]]
            else:
                vrednost=hash_optimizacija_mora_jedenje[rezultat[1]]
            kljucevi=vrednost.split("|")
            for kljuc in kljucevi:
                stanje[ast.literal_eval(kljuc)]=None
    
    #ako potez nije iz mape za optimizaciju
    if rezultat is None:
        #uzimanje najboljih poteza
        najbolja_vrednost=stablo_igre.koren.vrednost[2]

        najbolja_stanja=[]
        for dete in stablo_igre.koren.deca:
            if dete.vrednost[3]==najbolja_vrednost:
                najbolja_stanja.append(dete.vrednost[1])

        #uzimanje jednog od najboljih poteza
        rand=random.randint(0,len(najbolja_stanja)-1)
        stanje=najbolja_stanja[rand]

        #dodavanje u mapu za optimizaciju ali samo ako na tabli ne postoji dama
        #radi se ovako jer bi bilo previse stanja za pamcenje sa damama i moralo bi se pamtiti u stanju i da li je token dama a i kad postoji dama znaci da ima manje tokena pa ce svakako biti brze
        if not ima_dama:
            kljuc=""
            for token in moji_tokeni.keys():
                kljuc+=str(token)+"|"
            for token in protivnicki_tokeni.keys():
                kljuc+=str(token)+"|"
            kljuc=kljuc[:-1]
            vrednost=""
            for stanje1 in stanje.keys():
                vrednost+=str(stanje1)+"|"
            vrednost=vrednost[:-1]
            if not mora_da_se_jede:
                hash_optimizacija_ne_mora_jedenje[kljuc]=vrednost
            else:
                hash_optimizacija_mora_jedenje[kljuc]=vrednost
    
    #namestanje pomeranja tokena
    kompjuter=True
    token_za_pomeranje=None
    for token in protivnicki_tokeni.keys():
        if token not in stanje.keys():
            token_za_pomeranje=protivnicki_tokeni[token]
            break
    kljucevi=list(stanje.keys())
    pozicija_na_koju_se_pomera=kljucevi[-1]

    token_za_pomeranje.ima_pomeranje=True

    if token_za_pomeranje.sledece_pozicije.get(pozicija_na_koju_se_pomera)==None:
        krajnje_protivnicke_pozicije.append(pozicija_na_koju_se_pomera)
    else:
        for pozicija in token_za_pomeranje.sledece_pozicije[pozicija_na_koju_se_pomera]:
            krajnje_protivnicke_pozicije.append(pozicija)
    krajnje_protivnicke_pozicije.append(pozicija_na_koju_se_pomera)

    protivnicki_tokeni.pop(token_za_pomeranje.pozicija)
    protivnicki_tokeni[pozicija_na_koju_se_pomera]=token_za_pomeranje

    slike_moguci_potezi.clear()

    igra_kompjuter=False

# Odvojena kopija logickog stanja figure za svaku granu pretrage.
# copy.deepcopy nije pogodan za pygame.Surface koji Token sadrzi.
def kopija_tokena_za_stablo(token):
    kopija = copy.copy(token)
    kopija.moguci_potezi = list(token.moguci_potezi)
    kopija.pozicije_za_jedenje = {
        pozicija: list(pojedeni)
        for pozicija, pojedeni in token.pozicije_za_jedenje.items()
    }
    kopija.sledece_pozicije = {
        pozicija: list(koraci)
        for pozicija, koraci in token.sledece_pozicije.items()
    }
    return kopija

#rekurzivna metoda za pravljenje stabla igre sa razlicitim stanjima table
def pravljenje_stabla(stanje_moji_tokeni,stanje_protivnicki_tokeni,trenutni_cvor,trenutna_dubina,moj_red):
    global tokeni_koji_mogu_da_jedu
    global ima_koji_moze_da_jede
    global mora_da_se_jede
    global hash_optimizacija_ne_mora_jedenje
    global hash_optimizacija_mora_jedenje
    global ima_dama

    #ako se doslo do krajnje dubine stabla racuna se heuristika
    if trenutna_dubina==dubina:
        vrednost=heuristika(stanje_moji_tokeni,stanje_protivnicki_tokeni)
        #razlikuje se da li je dubina parna ili ne
        if dubina%2!=0:
            trenutni_cvor.vrednost[2]=vrednost
        else:
            trenutni_cvor.vrednost[3]=vrednost
        return
    
    if not ima_dama:
        #pravljenje kljuca za ovo stanje za mapu za optimizaciju
        kljuc=""
        for token in stanje_moji_tokeni.keys():
            kljuc+=str(token)+"|"
        for token in stanje_protivnicki_tokeni.keys():
            kljuc+=str(token)+"|"
        kljuc=kljuc[:-1]

        #provera da li je ovo stanje vec bilo, ako jeste uzima se vrednost iz mape i to su pozicije za sledece stanje
        try:
            if not mora_da_se_jede:
                ima_vrednost=hash_optimizacija_ne_mora_jedenje[kljuc]
            else:
                ima_vrednost=hash_optimizacija_mora_jedenje[kljuc]
            return ["hesovano",kljuc]
        except KeyError:
            pass
        #ako nije bilo ovog stanja pravi se novo stanje i dodaje se kasnije u mapu
    
    #pravljenje mogucih stanja table
    if moj_red:
        #provera da li neki od mojih tokena moze da jede ako je mod za obavezno jedenje
        if mora_da_se_jede:
            provera_tokena_koji_jedu(stanje_moji_tokeni,stanje_moji_tokeni,stanje_protivnicki_tokeni)
        for token in stanje_moji_tokeni.values():
            #dobijam moguce poteze za token
            token.pravljenje_poteza(stanje_moji_tokeni,stanje_protivnicki_tokeni)
            # Sacuvaj poteze ovog nivoa: dublja rekurzija ih ne sme izmeniti.
            moguci_potezi = list(token.moguci_potezi)
            pozicije_za_jedenje = {
                pozicija: list(pojedeni)
                for pozicija, pojedeni in token.pozicije_za_jedenje.items()
            }
            #prolazim kroz sve moguce poteze
            for potez in moguci_potezi:
                #pravljenje novog stanja table
                novo_stanje_moji_tokeni = {
                    pozicija: kopija_tokena_za_stablo(t)
                    for pozicija, t in stanje_moji_tokeni.items()
                }
                novo_stanje_protivnicki_tokeni = {
                    pozicija: kopija_tokena_za_stablo(t)
                    for pozicija, t in stanje_protivnicki_tokeni.items()
                }
                #pomeram token na novo stanje
                token1 = novo_stanje_moji_tokeni.pop(token.logicka_pozicija)
                novo_stanje_moji_tokeni[potez] = token1
                # Menjaj samo figuru u novom stanju, ne roditeljsko stanje.
                token1.logicka_pozicija = potez
                # Zapamti globalno stanje za vracanje posle grane.
                stari_tokeni_koji_mogu_da_jedu = tokeni_koji_mogu_da_jedu
                staro_ima_koji_moze_da_jede = ima_koji_moze_da_jede
                #provera da token nije postao dama
                if token1.logicka_pozicija[1]==pocetna_visina:
                    token1.logicka_dama=True
                #logicki brisem token koji je pojeden
                for pozicija1 in pozicije_za_jedenje.get(potez, []):
                    novo_stanje_protivnicki_tokeni.pop(pozicija1)
                ############################################################
                #debag_u_konzoli(novo_stanje_moji_tokeni,novo_stanje_protivnicki_tokeni,jedno_polje,pocetna_sirina,pocetna_visina)
                ############################################################
                #pravljenje novog cvora stabla
                novi_cvor=trenutni_cvor.dodaj_dete([novo_stanje_moji_tokeni,novo_stanje_protivnicki_tokeni,trenutni_cvor.vrednost[2],trenutni_cvor.vrednost[3]])
                pravljenje_stabla(novo_stanje_moji_tokeni,novo_stanje_protivnicki_tokeni,novi_cvor,trenutna_dubina+1,False)
                #u povratku iz rekurzije do prethodnog cvora vracam stanje table i racunam minimax algoritam
                tokeni_koji_mogu_da_jedu = stari_tokeni_koji_mogu_da_jedu
                ima_koji_moze_da_jede = staro_ima_koji_moze_da_jede

                #racunanje minimax algoritma
                if trenutna_dubina%2!=0:
                    if novi_cvor.vrednost[3]>trenutni_cvor.vrednost[2]:
                        trenutni_cvor.vrednost[2]=novi_cvor.vrednost[3]
                    elif novi_cvor.vrednost[2]>trenutni_cvor.vrednost[2]:
                        trenutni_cvor.vrednost[2]=novi_cvor.vrednost[2]
                else:
                    if novi_cvor.vrednost[2]<trenutni_cvor.vrednost[3]:
                        trenutni_cvor.vrednost[3]=novi_cvor.vrednost[2]
                    elif novi_cvor.vrednost[3]<trenutni_cvor.vrednost[3]:
                        trenutni_cvor.vrednost[3]=novi_cvor.vrednost[3]

                #rezanje
                if trenutni_cvor.vrednost[2]>=trenutni_cvor.vrednost[3]:
                    return
    else:
        #provera da li neki od protivnickih tokena moze da jede ako je mod za obavezno jedenje
        if mora_da_se_jede:
            provera_tokena_koji_jedu(stanje_protivnicki_tokeni,stanje_moji_tokeni,stanje_protivnicki_tokeni)
        for token in stanje_protivnicki_tokeni.values():
            token.pravljenje_poteza(stanje_moji_tokeni,stanje_protivnicki_tokeni)
            # Sacuvaj poteze ovog nivoa: dublja rekurzija ih ne sme izmeniti.
            moguci_potezi = list(token.moguci_potezi)
            pozicije_za_jedenje = {
                pozicija: list(pojedeni)
                for pozicija, pojedeni in token.pozicije_za_jedenje.items()
            }
            #prolazim kroz sve moguce poteze
            for potez in moguci_potezi:
                #pravljenje novog stanja table
                novo_stanje_moji_tokeni = {
                    pozicija: kopija_tokena_za_stablo(t)
                    for pozicija, t in stanje_moji_tokeni.items()
                }
                novo_stanje_protivnicki_tokeni = {
                    pozicija: kopija_tokena_za_stablo(t)
                    for pozicija, t in stanje_protivnicki_tokeni.items()
                }
                #pomeram token na novo stanje
                token1 = novo_stanje_protivnicki_tokeni.pop(token.logicka_pozicija)
                novo_stanje_protivnicki_tokeni[potez] = token1
                # Menjaj samo figuru u novom stanju, ne roditeljsko stanje.
                token1.logicka_pozicija = potez
                # Zapamti globalno stanje za vracanje posle grane.
                stari_tokeni_koji_mogu_da_jedu = tokeni_koji_mogu_da_jedu
                staro_ima_koji_moze_da_jede = ima_koji_moze_da_jede
                #provera da token nije postao dama
                if token1.logicka_pozicija[1]==pocetna_visina+jedno_polje.slika.get_height()*7:
                    token1.logicka_dama=True
                #logicki brisem token koji je pojeden
                for pozicija1 in pozicije_za_jedenje.get(potez, []):
                    novo_stanje_moji_tokeni.pop(pozicija1)
                ############################################################
                #debag_u_konzoli(novo_stanje_moji_tokeni,novo_stanje_protivnicki_tokeni,jedno_polje,pocetna_sirina,pocetna_visina)
                ############################################################
                #pravljenje novog cvora stabla
                novi_cvor=trenutni_cvor.dodaj_dete([novo_stanje_moji_tokeni,novo_stanje_protivnicki_tokeni,trenutni_cvor.vrednost[2],trenutni_cvor.vrednost[3]])
                pravljenje_stabla(novo_stanje_moji_tokeni,novo_stanje_protivnicki_tokeni,novi_cvor,trenutna_dubina+1,True)
                #u povratku iz rekurzije do prethodnog cvora vracam stanje table i racunam minimax algoritam
                tokeni_koji_mogu_da_jedu = stari_tokeni_koji_mogu_da_jedu
                ima_koji_moze_da_jede = staro_ima_koji_moze_da_jede

                #racunanje minimax algoritma
                if trenutna_dubina%2!=0:
                    if novi_cvor.vrednost[3]>trenutni_cvor.vrednost[2]:
                        trenutni_cvor.vrednost[2]=novi_cvor.vrednost[3]
                    if novi_cvor.vrednost[2]>trenutni_cvor.vrednost[2]:
                        trenutni_cvor.vrednost[2]=novi_cvor.vrednost[2]
                else:
                    if novi_cvor.vrednost[2]<trenutni_cvor.vrednost[3]:
                        trenutni_cvor.vrednost[3]=novi_cvor.vrednost[2]
                    if novi_cvor.vrednost[3]<trenutni_cvor.vrednost[3]:
                        trenutni_cvor.vrednost[3]=novi_cvor.vrednost[3]

                #rezanje
                if trenutni_cvor.vrednost[2]>=trenutni_cvor.vrednost[3]:
                    return

#metoda za heuristiku za minimax algoritam
def heuristika(stanje_moji_tokeni,stanje_protivnicki_tokeni):
    rezultat=0
    moji_koji_mogu_da_se_pojedu=[]
    protivnicki_koji_mogu_da_se_pojedu=[]
    ############################################################
    #debag_u_konzoli(stanje_moji_tokeni,stanje_protivnicki_tokeni,jedno_polje,pocetna_sirina,pocetna_visina)
    ############################################################
    for token in stanje_moji_tokeni.values():
        #ako je moj token dama vrednost mu je -5 a ako nije -1
        if token.logicka_dama:
            rezultat-=7.75
        else:
            rezultat-=5

        #ako je token u zadnjem redu ne moze da se pojede i protivnik ne moze da bude dama
        if token.logicka_pozicija[1]==pocetna_visina+jedno_polje.slika.get_height()*7:
            rezultat-=4

        #ako je token u srednje 4 kolone i srednja 2 reda oni kontrolisu sredinu
        if (token.logicka_pozicija[0]>=pocetna_sirina+jedno_polje.slika.get_width()*2 and token.logicka_pozicija[0]<=pocetna_sirina+jedno_polje.slika.get_width()*5) and (token.logicka_pozicija[1]==pocetna_visina+jedno_polje.slika.get_height()*3 or token.logicka_pozicija[1]==pocetna_visina+jedno_polje.slika.get_height()*4):
            rezultat-=2.5
        #ako je token u srednja 2 reda ali ne u srednje 4 kolone oni su isto vazni ali ne toliko
        elif (token.logicka_pozicija[0]<=pocetna_sirina+jedno_polje.slika.get_width() or token.logicka_pozicija[0]>=pocetna_sirina+jedno_polje.slika.get_width()*6) and (token.logicka_pozicija[1]==pocetna_visina+jedno_polje.slika.get_height()*3 or token.logicka_pozicija[1]==pocetna_visina+jedno_polje.slika.get_height()*4):
            rezultat-=0.5

        #broj protivnikovih tokena koji mogu biti pojedeni u sledecoj rundi je naravno vazan
        kopija_tokena=Token(lokacija+"\Slike\Crveni token.png",token.logicka_pozicija,True)
        if token.logicka_dama:
            kopija_tokena.logicka_dama=True
        kopija_tokena.pravljenje_poteza(stanje_moji_tokeni,stanje_protivnicki_tokeni)
        if len(kopija_tokena.pozicije_za_jedenje)>0:
            for pozicija in kopija_tokena.pozicije_za_jedenje.keys():
                if pozicija not in protivnicki_koji_mogu_da_se_pojedu:
                    protivnicki_koji_mogu_da_se_pojedu.append(pozicija)
                    rezultat-=3
        
        #broj mojih tokena koji ne mogu biti pojedeni jer su na ivicama ili se iza njih nalazi jos jedan moj ili protivnicki token
        #broj mojih tokena koji ne mogu biti pojedeni jer su na ivicama
        if token.logicka_pozicija[0]==pocetna_sirina or token.logicka_pozicija[0]==pocetna_sirina+jedno_polje.slika.get_width()*7 or token.logicka_pozicija[1]==pocetna_visina:
            rezultat-=3
        #moji tokeni iza koji se nalazi jos jedan moj token ili protivnicki token
        ima_dole_levo=False
        ima_dole_desno=False
        for token1 in stanje_moji_tokeni.values():
            if token1.logicka_pozicija[0]==token.logicka_pozicija[0]-jedno_polje.slika.get_width() and token1.logicka_pozicija[1]==token.logicka_pozicija[1]+jedno_polje.slika.get_height():
                ima_dole_levo=True
            if token1.logicka_pozicija[0]==token.logicka_pozicija[0]+jedno_polje.slika.get_width() and token1.logicka_pozicija[1]==token.logicka_pozicija[1]+jedno_polje.slika.get_height():
                ima_dole_desno=True

            if not ima_dole_desno or not ima_dole_levo:
                for token2 in stanje_protivnicki_tokeni.values():
                    if not token2.logicka_dama:
                        if token2.logicka_pozicija[0]==token.logicka_pozicija[0]-jedno_polje.slika.get_width() and token2.logicka_pozicija[1]==token.logicka_pozicija[1]+jedno_polje.slika.get_height():
                            ima_dole_levo=True
                        if token2.logicka_pozicija[0]==token.logicka_pozicija[0]+jedno_polje.slika.get_width() and token2.logicka_pozicija[1]==token.logicka_pozicija[1]+jedno_polje.slika.get_height():
                            ima_dole_desno=True
        if ima_dole_desno and ima_dole_levo:
            rezultat-=3
    for token in stanje_protivnicki_tokeni.values():
        #ako je protivnicki token dama vrednost mu je 5 a ako nije 1
        if token.logicka_dama:
            rezultat+=7.75
        else:
            rezultat+=5

        #ako je token u zadnjem redu ne moze da se pojede i protivnik ne moze da bude dama
        if token.logicka_pozicija[1]==pocetna_visina:
            rezultat+=4

        #ako je token u srednje 4 kolone i srednja 2 reda oni kontrolisu sredinu
        if (token.logicka_pozicija[0]>=pocetna_sirina+jedno_polje.slika.get_width()*2 and token.logicka_pozicija[0]<=pocetna_sirina+jedno_polje.slika.get_width()*5) and (token.logicka_pozicija[1]==pocetna_visina+jedno_polje.slika.get_height()*3 or token.logicka_pozicija[1]==pocetna_visina+jedno_polje.slika.get_height()*4):
            rezultat+=2.5
        #ako je token u srednja 2 reda ali ne u srednje 4 kolone oni su isto vazni ali ne toliko
        elif (token.logicka_pozicija[0]<=pocetna_sirina+jedno_polje.slika.get_width() or token.logicka_pozicija[0]>=pocetna_sirina+jedno_polje.slika.get_width()*6) and (token.logicka_pozicija[1]==pocetna_visina+jedno_polje.slika.get_height()*3 or token.logicka_pozicija[1]==pocetna_visina+jedno_polje.slika.get_height()*4):
            rezultat+=0.5

        #broj protivnikovih tokena koji mogu biti pojedeni u sledecoj rundi je naravno vazan
        kopija_tokena=Token(lokacija+"\Slike\Sivi token.png",token.logicka_pozicija,False)
        if token.logicka_dama:
            kopija_tokena.logicka_dama=True
        kopija_tokena.pravljenje_poteza(stanje_protivnicki_tokeni,stanje_moji_tokeni)
        if len(kopija_tokena.pozicije_za_jedenje)>0:
            for pozicija in kopija_tokena.pozicije_za_jedenje.keys():
                if pozicija not in moji_koji_mogu_da_se_pojedu:
                    moji_koji_mogu_da_se_pojedu.append(pozicija)
                    rezultat+=3

        #broj mojih tokena koji ne mogu biti pojedeni jer su na ivicama ili se iza njih nalazi jos jedan moj ili protivnicki token
        #broj protivnickih tokena koji ne mogu biti pojedeni jer su na ivicama
        if token.logicka_pozicija[0]==pocetna_sirina or token.logicka_pozicija[0]==pocetna_sirina+jedno_polje.slika.get_width()*7 or token.logicka_pozicija[1]==pocetna_visina+jedno_polje.slika.get_height()*7:
            rezultat+=3
        #moji tokeni iza koji se nalazi jos jedan moj token ili protivnicki token
        ima_gore_levo=False
        ima_gore_desno=False
        for token1 in stanje_moji_tokeni.values():
            if token1.logicka_pozicija[0]==token.logicka_pozicija[0]-jedno_polje.slika.get_width() and token1.logicka_pozicija[1]==token.logicka_pozicija[1]-jedno_polje.slika.get_height():
                ima_gore_levo=True
            if token1.logicka_pozicija[0]==token.logicka_pozicija[0]+jedno_polje.slika.get_width() and token1.logicka_pozicija[1]==token.logicka_pozicija[1]-jedno_polje.slika.get_height():
                ima_gore_desno=True

            if not ima_gore_desno or not ima_gore_levo:
                for token2 in stanje_protivnicki_tokeni.values():
                    if token2.logicka_pozicija[0]==token.logicka_pozicija[0]-jedno_polje.slika.get_width() and token2.logicka_pozicija[1]==token.logicka_pozicija[1]-jedno_polje.slika.get_height():
                        ima_gore_levo=True
                    if token2.logicka_pozicija[0]==token.logicka_pozicija[0]+jedno_polje.slika.get_width() and token2.logicka_pozicija[1]==token.logicka_pozicija[1]-jedno_polje.slika.get_height():
                        ima_gore_desno=True
        if ima_gore_levo and ima_gore_desno:
            rezultat+=3

    return rezultat

#metoda koja proverava za sve tokene da li mogu da pojedu bar jedan protivnicki token
def provera_tokena_koji_jedu(tokeni,stanje_moji_tokeni,stanje_protivnicki_tokeni):
    global ima_koji_moze_da_jede
    global tokeni_koji_mogu_da_jedu
    global provereno_jedenje

    ima_koji_moze_da_jede=False
    tokeni_koji_mogu_da_jedu=[]
    provereno_jedenje=True

    for token in tokeni.values():
        if not token.logicka_dama:
            jede=token.provera_preskakanja(token.logicka_pozicija,stanje_moji_tokeni,stanje_protivnicki_tokeni,True,[],True)
            if jede:
                ima_koji_moze_da_jede=True
                tokeni_koji_mogu_da_jedu.append(token.logicka_pozicija)
        else:
            jede=token.provera_preskakanja_dama(token.logicka_pozicija,stanje_moji_tokeni,stanje_protivnicki_tokeni,True,[],True)
            if jede:
                ima_koji_moze_da_jede=True
                tokeni_koji_mogu_da_jedu.append(token.logicka_pozicija)

#provera da li imam token koji moze da se pomeri
def provera_pomeranja():
    for token in moji_tokeni.values():
        ima_pomeraj=token.pravljenje_poteza(moji_tokeni,protivnicki_tokeni,True)
        if ima_pomeraj:
            return True
    return False

#metoda za kraj igre
def kraj(ja_pobedio):
    global restartovano

    #pravljenje fonta
    font = pygame.font.Font(lokacija+"\Font\Piksel.ttf", 36)

    #pravljenje pozadine za kraj igre
    if ja_pobedio:
        zelena_pozadina=Pozadina(lokacija+"\Slike\Zelena pozadina.png")
        prozor.blit(zelena_pozadina.slika,(0,0))
        #pravljenje teksta
        text = font.render("Pobedili ste", True, (255, 215, 0))
    else:
        crvena_pozadina=Pozadina(lokacija+"\Slike\Crvena pozadina.png")
        prozor.blit(crvena_pozadina.slika,(0,0))
        #pravljenje teksta
        text = font.render("Izgubili ste", True, (255, 215, 0))

    #pitanje da li zelite da igrate ponovo
    text1=font.render("Da li zelite da igrate ponovo?",True,(255,215,0))

    #pravljenje pravougaonika za tekst
    textRect = text.get_rect()
    textRect1=text1.get_rect()
    #centriranje teksta
    textRect.center = (sirina_prozora // 2, visina_prozora // 2-50)
    textRect1.center=(sirina_prozora // 2, visina_prozora // 2+25)
    #crtanje teksta
    prozor.blit(text, textRect)
    prozor.blit(text1,textRect1)

    #pravljenje dugmica
    izadji_dugme=Dugme(lokacija+"\Slike\Dugme ne.png",(pocetna_sirina+4*jedno_polje.slika.get_width(),pocetna_visina+4*jedno_polje.slika.get_height()+50),"izadji")
    restart_dugme=Dugme(lokacija+"\Slike\Dugme da.png",(pocetna_sirina+2*jedno_polje.slika.get_width(),pocetna_visina+4*jedno_polje.slika.get_height()+50),"restart")
    #crtanje dugmica
    izadji_dugme.crtanje()
    restart_dugme.crtanje()

    #petlja igre
    igranje=True
    while igranje:
        for dogadjaj in pygame.event.get():
            #ako se klikne na X zatvara se prozor i prekida se igra
            if dogadjaj.type==pygame.QUIT:
                pygame.quit()

        #ako se klikne na izadji dugme zatvara se prozor i prekida se igra
        izadji_dugme.provera_klika()

        #ako se klikne na restart dugme igra se ponovo pokrece
        restart_dugme.provera_klika()

        #osvezavanje prozora
        pygame.display.flip()
    
        if restartovano:
            igranje=False
            continue

    restartovano=False

#metoda za uzitavanje mape za optimizaciju iz fajla
def citanje_mape():
    global stanja

    #prvo za mapu gde ne mora da se jede
    file=open(os.path.join(lokacija, "StanjaNeMoraJedenje.txt"),"r")
    stanja=file.read().split("\n")
    file.close()

    stanja=stanja[:-1]
    if len(stanja)==0:
        return

    for i in range(len(stanja)):
        stanja[i]=stanja[i].split(" - ")

    for i in range(len(stanja)):
        hash_optimizacija_ne_mora_jedenje[stanja[i][0]]=stanja[i][1]

    #drugo za mapu gde mora da se jede
    file=open(os.path.join(lokacija, "StanjaMoraJedenje.txt"),"r")
    stanja=file.read().split("\n")
    file.close()

    stanja=stanja[:-1]
    if len(stanja)==0:
        return

    for i in range(len(stanja)):
        stanja[i]=stanja[i].split(" - ")

    for i in range(len(stanja)):
        hash_optimizacija_mora_jedenje[stanja[i][0]]=stanja[i][1]

#metoda za pisanje mape za optimizaciju u fajl
def pisanje_mape():
    #prvo za mapu gde ne mora da se jede
    file=open(os.path.join(lokacija, "StanjaNeMoraJedenje.txt"),"w")
    for stanje in hash_optimizacija_ne_mora_jedenje.keys():
        file.write(str(stanje)+" - "+str(hash_optimizacija_ne_mora_jedenje[stanje])+"\n")
    file.close()

    #drugo za mapu gde mora da se jede
    file=open(os.path.join(lokacija, "StanjaMoraJedenje.txt"),"w")
    for stanje in hash_optimizacija_mora_jedenje.keys():
        file.write(str(stanje)+" - "+str(hash_optimizacija_mora_jedenje[stanje])+"\n")
    file.close()

#metoda za varijabilnu dubinu
#iz testiranja je utvrdjeno da je za igru najbolja dubina 3, preko toga kompjuter previse komplikuje i igra nije dobra
#kako je igra pravljena za dubinu 3 jedina dubina koja je jos dobra je 2, 1 vec nema smisla
#tako da je ova metoda napravljena da se varijabilno menja dubina tako da pokusa da odrzi igru izjednacenom
def varijabilna_dubina():
    global dubina

    if len(moji_tokeni)>=len(protivnicki_tokeni):
        dubina=3
    else:
        dubina=2

#pocetno crtanje
crtanje_pocetak()

#ucitavanje mape za optimizaciju iz fajla
citanje_mape()

#petlja igre
igranje=True
while igranje:
    for dogadjaj in pygame.event.get():
        #ako se klikne na X zatvara se prozor i prekida se igra
        if dogadjaj.type==pygame.QUIT:
            igranje=False
            break
    
    #provera da li neki protivnicki token treba da se pomera
    ima_pomeranja=False
    for token in protivnicki_tokeni.values():
        if token.ima_pomeranje:
            ima_pomeranja=True
            break
    #igranje kompjutera
    if not moj_red and not kompjuter and not ima_pomeranja:
        varijabilna_dubina()
        vreme=time.time()
        igranje_kompjutera()
        print(time.time()-vreme)

        tokeni_koji_mogu_da_jedu.clear()

    #crtanje table
    crtanje_table()

    #provera da li je neki token pojeden
    for token in moji_tokeni.values():
        for token1 in protivnicki_tokeni.values():
            if token.telo.colliderect(token1.telo):
                if len(krajnje_moje_pozicije)>0:
                    token1.pojeden=True
                else:
                    token.pojeden=True

    #crtanje tokena i poteza i provera da li su tokeni pojedeni ili postaju dame
    za_brisanje_protivnicki=[]
    za_brisanje_moji=[]
    #koji tokeni se crtaju drugi oni se vide preko prvih
    if kompjuter:
        for token in protivnicki_tokeni.values():
            token.crtanje(token.pozicija)
            if token.slika.get_alpha()==0:
                za_brisanje_protivnicki.append(token.pozicija)
            if token.pozicija[1]==pocetna_visina+jedno_polje.slika.get_height()*7 and not token.dama:
                token.dama=True
                token.logicka_dama=True
                ima_dama=True
                slika_dame = pygame.image.load(lokacija+"\Slike\Crvena dama.png")
                slika_dame = pygame.transform.scale(slika_dame, (token.slika.get_width(), token.slika.get_height()))
                token.slika = slika_dame
        for token in moji_tokeni.values():
            token.crtanje(token.pozicija)
            if token.slika.get_alpha()==0:
                za_brisanje_moji.append(token.pozicija)
            if token.pozicija[1]==pocetna_visina and not token.dama:
                token.dama=True
                token.logicka_dama=True
                ima_dama=True
                slika_dame = pygame.image.load(lokacija+"\Slike\Siva dama.png")
                slika_dame = pygame.transform.scale(slika_dame, (token.slika.get_width(), token.slika.get_height()))
                token.slika = slika_dame
    else:
        for token in moji_tokeni.values():
            token.crtanje(token.pozicija)
            if token.slika.get_alpha()==0:
                za_brisanje_moji.append(token.pozicija)
            if token.pozicija[1]==pocetna_visina and not token.dama:
                token.dama=True
                token.logicka_dama=True
                ima_dama=True
                slika_dame = pygame.image.load(lokacija+"\Slike\Siva dama.png")
                slika_dame = pygame.transform.scale(slika_dame, (token.slika.get_width(), token.slika.get_height()))
                token.slika = slika_dame
        for token in protivnicki_tokeni.values():
            token.crtanje(token.pozicija)
            if token.slika.get_alpha()==0:
                za_brisanje_protivnicki.append(token.pozicija)
            if token.pozicija[1]==pocetna_visina+jedno_polje.slika.get_height()*7 and not token.dama:
                token.dama=True
                token.logicka_dama=True
                ima_dama=True
                slika_dame = pygame.image.load(lokacija+"\Slike\Crvena dama.png")
                slika_dame = pygame.transform.scale(slika_dame, (token.slika.get_width(), token.slika.get_height()))
                token.slika=slika_dame

    #provera da li neki od mojih tokena moze da jede
    if not provereno_jedenje and mora_da_se_jede:
        provera_tokena_koji_jedu(moji_tokeni,moji_tokeni,protivnicki_tokeni)

    #provera da li neki od mojih tokena moze da se pomeri jer ako ne mogu onda je kraj
    if not provereno_pomeranje:
        ima_pomeranja=provera_pomeranja()
        if not ima_pomeranja:
            kraj(False)
        provereno_pomeranje=True

    #crtanje mogucih poteza     
    if moj_red:
        for potez in slike_moguci_potezi.values():
            potez.crtanje()

    #crtanje okvira oko tokena koji mogu da jedu ako je mod da mora da se jede
    if not igra_kompjuter and mora_da_se_jede:
        for pozicija in tokeni_koji_mogu_da_jedu:
            slika_okvira=pygame.image.load(lokacija+"\Slike\Oznaka.png")
            slika_okvira=pygame.transform.scale(slika_okvira,(jedno_polje.slika.get_width(),jedno_polje.slika.get_height()))
            prozor.blit(slika_okvira,pozicija)

    #brisanje pojedenih tokena
    for pozicija in za_brisanje_protivnicki:
        protivnicki_tokeni.pop(pozicija)
    for pozicija in za_brisanje_moji:
        moji_tokeni.pop(pozicija)

    #provera da protivnik nije pobedio
    if len(moji_tokeni)==0:
        kraj(False)
    
    #osvezavanje prozora
    pygame.display.flip()

#zatvaranje prozora
pygame.quit()