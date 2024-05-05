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
suit_to_couleur = {
    'hearts': Couleur.COEURS,
    'diamonds': Couleur.CARREAUX,
    'clubs': Couleur.TREFLES,
    'spades': Couleur.PIQUES
}

def transform_color_name(color):
    return suit_to_couleur.get(color)

rank_to_rang = {
    'seven': Rang.SEPT,
    'eight': Rang.HUIT,
    'nine': Rang.NEUF,
    'ten': Rang.DIX,
    'jack': Rang.VALET,
    'queen': Rang.DAME,
    'king': Rang.ROI,
    'ace': Rang.AS
}

couleur_to_suit = {v: k for k, v in suit_to_couleur.items()}
rang_to_rank = {v: k for k, v in rank_to_rang.items()}

def parsing_of_card_to_return(card):
    suit_string = couleur_to_suit[card.couleur]
    rank_string = rang_to_rank[card.rang]
    return suit_string, rank_string

def json_to_cards(json_data):
    cards = []
    for item in json_data:
        suit = item['suit']
        rank = item['rank']
        couleur = suit_to_couleur[suit]
        rang = rank_to_rang[rank]
        cards.append((couleur, rang))
    
    list_of_cards = []
    for couleur, rang in cards:  # Corrigez cette ligne pour le déballage de tuple
        newcard = Carte(couleur, rang)  # Utilisez directement les variables déballées
        list_of_cards.append(newcard)
    print(type(list_of_cards))
    return list_of_cards

RANG_ORDER = {Rang.SEPT: 0, Rang.HUIT: 1, Rang.NEUF: 2, Rang.DIX: 3,
              Rang.VALET: 4, Rang.DAME: 5, Rang.ROI: 6, Rang.AS: 7}


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
