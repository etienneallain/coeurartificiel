from enum import Enum

from carte import Carte
from paquet import Paquet
from joueur import Joueur
from pli import Pli
from JoueurEncoder import JoueurEncoder
import random
class Manche:
    def __init__(self,joueurs):
        self.ouvreur = None
        self.paquet = Paquet()
        self.joueurs = joueurs

        self.distribuer_cartes()
        self.paquet.melanger_paquet()


    def distribuer_cartes(self):
        for j in self.joueurs:
            for _ in range(8):
                j.add_card(self.paquet.prendre_carte())

    def jouer_manche(self):

        self.ouvreur = random.randrange(0,3)

        for i in range(8):
            pli = Pli(self.joueurs,self.ouvreur)
            pli.jouer_pli()
            gagnant = self.gagnant_pli(pli)
            self.ouvreur= self.joueurs.index(gagnant)
            for c in pli.get_pli():
                gagnant.add_remporte_carte(c)
        for j in self.joueurs:
            j.scoreCalc()
            print(j.getName()+": "+str(j.getScore()))


    def gagnant_pli(self,pli):
        carte_gagnante = None
        joueur = None
        j=0
        cartes_pli = pli.get_pli()
        couleur = pli.get_couleur()
        for carte in cartes_pli:
            if carte.get_couleur() == couleur:
                if carte_gagnante is None or carte.get_order()>carte_gagnante.get_order():
                    carte_gagnante = carte
                    joueur = self.joueurs[j]
            j=j+1
        return joueur

    def getIndex(self,joueur):
        k=0
        for j in self.joueurs:
            if j == joueur:
                return k
        return -1


