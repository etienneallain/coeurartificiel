import random

from enum import Enum


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

COULEUR_MAPPING = {
    'hearts': Couleur.COEURS,
    'diamonds': Couleur.CARREAUX,
    'clubs': Couleur.TREFLES,
    'spades': Couleur.PIQUES
}

# Mapping des noms de rangs anglais vers français
RANG_MAPPING = {
    'seven': Rang.SEPT,
    'eight': Rang.HUIT,
    'nine': Rang.NEUF,
    'ten': Rang.DIX,
    'jack': Rang.VALET,
    'queen': Rang.DAME,
    'king': Rang.ROI,
    'ace': Rang.AS
}

# Convertir les données en objets Carte en utilisant le mapping
def convertir_donnees_en_cartes(donnees):
    cartes = []
    for carte_data in donnees:
        couleur_str = carte_data['suit']
        rang_str = carte_data['rank']

        # Convertir les noms de couleur et de rang en objets correspondants
        couleur = COULEUR_MAPPING.get(couleur_str.lower())
        rang = RANG_MAPPING.get(rang_str.lower())

        if couleur and rang:
            cartes.append(Carte(couleur, rang))
        else:
            print(f"Ignorer la carte avec la couleur {couleur_str} et le rang {rang_str}")

    return cartes
class Paquet:
    def __init__(self):
        self.cartes = [Carte(couleur, rang) for couleur in Couleur for rang in Rang]

    def melanger_paquet(self):
        random.shuffle(self.cartes)

    def prendre_carte(self):
        return self.cartes.pop()

    def remove_card(self, carte):
        if carte in self.cartes:
            self.cartes.remove(carte)
            return carte
        else:
            print("Card not found in the paquet.")
            return None

    # def __str__(self):
    #     return "\n".join([f"{carte.couleur.name} - {carte.rang.name}" for carte in self.cartes])
    def __str__(self):
        return str(len(self.cartes))

    def remove_cards(self, cards):
        remaining_cards = [card for card in self.cartes if card not in cards]

        if len(cards) != len(self.cartes) - len(remaining_cards):
            print("Some cards not found in the paquet.")

        return remaining_cards


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
        return RANG_ORDER.get(self.rang, 1000)

    def __eq__(self, other):
        if isinstance(other, Carte):
            return self.couleur == other.couleur and self.rang == other.rang
        return False
