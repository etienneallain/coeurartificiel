import torch

from carte import Carte
from joueur import Joueur
from paquet import Couleur, Rang


class JoueurEncoder:
    def encode_hand(self,cards):
        encoded_hand = [-1] * (4 * 8)
        couleur_encoding = {'♥': 0, '♦': 1, '♣': 2, '♠': 3}
        rang_encoding = {'7': 0, '8': 1, '9': 2, '10': 3, 'V': 4, 'D': 5, 'R': 6, 'A': 7}

        for carte in cards:
            couleur_index = couleur_encoding.get(carte.get_couleur().value)
            rang_index = rang_encoding.get(carte.get_rang().value)
            encoded_hand[8 * couleur_index + rang_index] = 1

        # A ameliorer: normaliser le score
        #encoded_hand.append(self.joueur.getScore())
        return encoded_hand

    def encode_card(self, card):
        encoded_hand = [-1] * (4 * 8)
        couleur_encoding = {'♥': 0, '♦': 1, '♣': 2, '♠': 3}
        rang_encoding = {'7': 0, '8': 1, '9': 2, '10': 3, 'V': 4, 'D': 5, 'R': 6, 'A': 7}

        couleur_index = couleur_encoding.get(card.get_couleur().value)
        rang_index = rang_encoding.get(card.get_rang().value)
        encoded_hand[8 * couleur_index + rang_index] = 1

        return encoded_hand


if __name__ == '__main__':
    cartes = [
        Carte(Couleur.TREFLES, Rang.VALET),
        Carte(Couleur.COEURS, Rang.ROI),
        Carte(Couleur.COEURS, Rang.AS),
        Carte(Couleur.COEURS, Rang.SEPT),
        Carte(Couleur.COEURS, Rang.DAME),
        Carte(Couleur.COEURS, Rang.HUIT),
        Carte(Couleur.COEURS, Rang.NEUF),
        Carte(Couleur.COEURS,Rang.DIX)
    ]
    j = JoueurEncoder()
    encoded_result = j.encode_hand(cartes)
    print(encoded_result)

