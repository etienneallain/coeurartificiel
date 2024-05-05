import random
from paquet import Paquet, Couleur
from pli import Pli


class Manche:
    def __init__(self, joueurs):
        self.ouvreur = None
        self.paquet = Paquet()
        self.joueurs = joueurs
        self.paquet.melanger_paquet()
        self.distribuer_cartes()
        self.cards_left = Paquet()

    def distribuer_cartes(self):
        for j in self.joueurs:
            for _ in range(8):
                j.add_card(self.paquet.prendre_carte())

    def play_to_update_random_dataset(self, dataset):
        self.ouvreur = random.randrange(0, 4)
        for i in range(8):
            pli = Pli(self.joueurs, self.ouvreur, self.cards_left, i)
            pli.play_trick_to_update_random_dataset()
            gagnant = self.gagnant_pli(pli)
            self.ouvreur = self.joueurs.index(gagnant)
            has_won_heart = any(card.get_couleur() == Couleur.COEURS for card in pli.get_pli())
            if has_won_heart:
                for player in self.joueurs:
                    if player != gagnant:
                        player.flag_hearts = -1
            for c in pli.get_pli():
                gagnant.add_remporte_carte(c)
                self.cards_left.remove_card(c)
        for j in self.joueurs:
            j.scoreCalc()
            j.set_dataset_score(j.getScore())
            dataset.add_dataset(j.get_input_data())

    def play_with_NN(self):
        self.ouvreur = random.randrange(0, 4)
        for i in range(8):
            pli = Pli(self.joueurs, self.ouvreur, self.cards_left, i)
            pli.play_trick_with_NN()
            gagnant = self.gagnant_pli(pli)
            self.ouvreur = self.joueurs.index(gagnant)
            has_won_heart = any(card.get_couleur() == Couleur.COEURS for card in pli.get_pli())
            if has_won_heart:
                for player in self.joueurs:
                    if player != gagnant:
                        player.flag_hearts = -1
            for c in pli.get_pli():
                gagnant.add_remporte_carte(c)
                self.cards_left.remove_card(c)
        for j in self.joueurs:
            j.scoreCalc()

    def play_to_update_nn_dataset(self, dataset):
        self.ouvreur = random.randrange(0, 4)
        for i in range(8):
            pli = Pli(self.joueurs, self.ouvreur, self.cards_left, i)
            pli.play_trick_to_update_nn_dataset()
            gagnant = self.gagnant_pli(pli)
            self.ouvreur = self.joueurs.index(gagnant)
            has_won_heart = any(card.get_couleur() == Couleur.COEURS for card in pli.get_pli())
            if has_won_heart:
                for player in self.joueurs:
                    if player != gagnant:
                        player.flag_hearts = -1
            for c in pli.get_pli():
                gagnant.add_remporte_carte(c)
                self.cards_left.remove_card(c)
        for j in self.joueurs:
            j.scoreCalc()
            j.set_dataset_score(j.getScore())
            dataset.add_dataset(j.get_input_data())

    def gagnant_pli(self, pli):
        carte_gagnante = None
        joueur = None
        j = 0
        cartes_pli = pli.get_pli()
        couleur = pli.get_couleur()
        for carte in cartes_pli:
            if carte.get_couleur() == couleur:
                if carte_gagnante is None or carte.get_order() > carte_gagnante.get_order():
                    carte_gagnante = carte
                    joueur = self.joueurs[j]
            j += 1
        return joueur

    def get_index(self, joueur):
        k = 0
        for j in self.joueurs:
            if j == joueur:
                return k
            k += 1
        return -1
