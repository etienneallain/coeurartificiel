from carte import Carte
from joueur import Joueur


class Pli:
    def __init__(self, joueurs, ouvreur):
        self.pli = [None, None, None, None]
        self.joueurs = joueurs
        self.ouvreur = ouvreur
        self.couleur = None

    def __str__(self):
        return ', '.join(str(carte) for carte in self.pli)

    def jouer_pli(self):
        print("\n")
        for i in range(4):
            k = (self.ouvreur + i) % 4
            c = self.joueurs[k].jouer_carte_simple()
            if k == self.ouvreur:
                self.couleur = c.get_couleur()
            self.pli[k] = c
            self.joueurs[k].update_dataset(self.joueurs[k].get_cartes(),c)
            #self.joueurs[k].print_dataset()
            print(self.joueurs[k])


    def get_pli(self):
        return self.pli

    def get_couleur(self):
        return self.couleur

    def set_couleur(self, couleur):
        self.couleur = couleur
