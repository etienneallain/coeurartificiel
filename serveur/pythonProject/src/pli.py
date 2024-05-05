import torch

from Player import RandomPlayer
from JoueurEncoder import JoueurEncoder
from paquet import Paquet


class Pli:
    def __init__(self, joueurs, ouvreur, cards_left, numero_pli):
        self.cartes_du_pli = [None, None, None, None]
        self.joueurs = joueurs
        self.ouvreur = ouvreur
        self.couleur = None
        self.cards_left = cards_left
        self.numero_pli = numero_pli
        self.static_pack = Paquet()

    def __str__(self):
        return ', '.join(str(carte) for carte in self.cartes_du_pli)

    def play_trick_to_update_random_dataset(self):
        for i in range(4):
            k = (self.ouvreur + i) % 4
            playable_cards = self.cards_left.cartes.copy()
            playable_cards = [card for card in playable_cards if card not in self.joueurs[k].get_cartes()]
            c = self.joueurs[k].play_card(self.couleur, None)
            if k == self.ouvreur:
                self.couleur = c.get_couleur()
            self.cartes_du_pli[k] = c

            # 1. les cartes dans la main du joueur
            cards_in_hand = self.joueurs[k].get_cartes()

            self.joueurs[k].update_dataset(self.numero_pli, cards_in_hand, playable_cards, self.cartes_du_pli,
                                           self.couleur, self.get_true_count(), self.joueurs[k].flag_hearts, c)

    def play_trick_with_NN(self):
        for i in range(4):
            k = (self.ouvreur + i) % 4

            cards_in_hand = self.joueurs[k].get_cartes()
            playable_cards = self.cards_left.cartes.copy()
            playable_cards = [card for card in playable_cards if card not in self.joueurs[k].get_cartes()]
            encoded_input_data = self.encode_input(
                self.numero_pli, cards_in_hand, playable_cards, self.cartes_du_pli, self.couleur, self.get_true_count(),
                self.joueurs[k].flag_hearts)
            stre = ""
            for card in self.cartes_du_pli:
                stre += str(card)
            if self.joueurs[k].name == "Monster":
                 print(self.joueurs[k])
            c = self.joueurs[k].play_card(self.couleur, encoded_input_data)

            if self.joueurs[k].name == "Monster":

                 print("cartes du pli "+stre)
                 print("carte jouee:"+str(c))

            if k == self.ouvreur:
                self.couleur = c.get_couleur()

            self.cartes_du_pli[k] = c

    def play_trick_to_update_nn_dataset(self):
        for i in range(4):
            k = (self.ouvreur + i) % 4

            cards_in_hand = self.joueurs[k].get_cartes()
            playable_cards = self.cards_left.cartes.copy()
            playable_cards = [card for card in playable_cards if card not in self.joueurs[k].get_cartes()]

            encoded_input_data = self.encode_input(
                self.numero_pli, cards_in_hand, playable_cards, self.cartes_du_pli, self.couleur,
                self.get_true_count(), self.joueurs[k].flag_hearts)

            c = self.joueurs[k].play_card(self.couleur, encoded_input_data)

            # Update the dataset for the NN player
            self.joueurs[k].update_dataset(self.numero_pli, cards_in_hand, playable_cards, self.cartes_du_pli,
                                           self.couleur, self.get_true_count(), self.joueurs[k].flag_hearts, c)

            if k == self.ouvreur:
                self.couleur = c.get_couleur()

            self.cartes_du_pli[k] = c

    def encode_input(self, numero_pli, cards_in_hand, playable_cards, cartes_du_pli, couleur, ordre_joueur,
                     flag_hearts):
        return self.joueurs[0].encode_input(numero_pli, cards_in_hand, playable_cards, cartes_du_pli, couleur,
                                            ordre_joueur, flag_hearts)

    def get_pli(self):
        return self.cartes_du_pli

    def get_couleur(self):
        return self.couleur

    def set_couleur(self, couleur):
        self.couleur = couleur

    def get_true_count(self):
        return sum(card is not None for card in self.cartes_du_pli)
