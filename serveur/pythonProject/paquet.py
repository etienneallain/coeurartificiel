import random

from enum import Enum

from carte import Carte


class Couleur(Enum):
    COEURS = '♥'
    CARREAUX = '♦'
    TREFLES = '♣'
    PIQUES = '♠'


class Rang(Enum):
    SEPT = '7'
    HUIT = '8'
    NEUF = '9'
    DIX = '10'
    VALET = 'V'
    DAME = 'D'
    ROI = 'R'
    AS = 'A'


RANG_ORDER = {Rang.SEPT: 0, Rang.HUIT: 1, Rang.NEUF: 2, Rang.DIX: 3,
              Rang.VALET: 4, Rang.DAME: 5, Rang.ROI: 6, Rang.AS: 7}


class Paquet:
    def __init__(self):
        self.cartes = [Carte(couleur, rang) for couleur in Couleur for rang in Rang]

    def melanger_paquet(self):
        random.shuffle(self.cartes)

    def prendre_carte(self):
        return self.cartes.pop()


class Carte:
    def __init__(self, couleur, rang):
        self.couleur = couleur
        self.rang = rang

    def __str__(self):
        return f"{self.rang.value}{self.couleur.value}"

    def get_couleur(self):
        return self.couleur

    def get_rang(self):
        return self.rang

    def get_order(self):
        from paquet import RANG_ORDER
        return RANG_ORDER.get(self.rang, 1000)
