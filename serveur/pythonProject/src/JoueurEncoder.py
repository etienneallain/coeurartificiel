import torch

from paquet import Couleur, Rang, Carte


class JoueurEncoder:

    def __init__(self):
        self.couleur_encoding = {'♥': 0, '♦': 1, '♣': 2, '♠': 3}
        self.rang_encoding = {'7': 0, '8': 1, '9': 2, '10': 3, 'V': 4, 'D': 5, 'R': 6, 'A': 7}
        self.inverse_couleur_encoding = {v: k for k, v in self.couleur_encoding.items()}
        self.inverse_rang_encoding = {v: k for k, v in self.rang_encoding.items()}

    def decode_card_index(self, index):
        couleur_index = index // 8
        rang_index = index % 8

        couleur = self.inverse_couleur_encoding[couleur_index]
        rang = self.inverse_rang_encoding[rang_index]

        return Carte(Couleur(couleur), Rang(rang))

    def encode_cards(self, cards):
        encoded_hand = [-1] * (4 * 8)

        for carte in cards:
            if carte is None:
                continue
            couleur_index = self.couleur_encoding.get(carte.get_couleur().value)
            rang_index = self.rang_encoding.get(carte.get_rang().value)
            encoded_hand[8 * couleur_index + rang_index] = 1

        return encoded_hand

    def encode_card(self, card):
        return self.encode_cards([card])

    def encode_numero_pli(self, numero_pli):
        encoded_numero_pli = [-1] * 8
        encoded_numero_pli[numero_pli] = 1
        return encoded_numero_pli

    def encode_couleur(self, couleur):
        if couleur is None:
            return [0] * 4
        encoded_couleur = [-1] * 4
        color_lower = couleur.value.lower()
        index = self.couleur_encoding.get(color_lower, -1)

        if index != -1:
            encoded_couleur[index] = 1

        return encoded_couleur

    def encode_ordre_joueur(self, ordre_joueur):
        encoded_ordre_joueur = [-1] * 4
        encoded_ordre_joueur[ordre_joueur - 1] = 1
        return encoded_ordre_joueur


if __name__ == '__main__':
    j = JoueurEncoder()
    card_index = 29  # Example index out of 32
    card = j.decode_card_index(card_index)
    print(card)
