from carte import Carte
from paquet import Rang


class Joueur:

    def __init__(self, name):
        self.name = name
        self.cartes = []
        self.input_dataset = {}
        self.cartes_remportes = []
        self.score = 0

    def print_dataset(self):
        for input_data, output_data in self.input_dataset.items():
            print(f"Input: {input_data}, Output: {output_data}")
    def add_card(self, card):
        self.cartes.append(card)

    def add_remporte_carte(self, pli):
        self.cartes_remportes.append(pli)

    def get_cartes_remportes(self):
        return f"{self.name}: {', '.join(str(carte) for carte in self.cartes_remportes)}"

    def get_cartes(self):
        return self.cartes

    def getName(self):
        return self.name

    def __str__(self):
        return f"{self.name}: {', '.join(str(carte) for carte in self.cartes)} + encoded:" + f"{self.input_dataset}"

    def ouvrir(self):
        return self.cartes.pop()

    def jouer_carte_simple(self, couleur=None):
        if couleur == None:
            card = self.cartes.pop()
            self.couleur = card.get_couleur()
            return card
        else:
            for card in self.cartes:
                if card.get_couleur() == couleur:
                    self.cartes.remove(card)
                    return card
            # Si on trouve pas la couleur
            return self.cartes.pop()

    def scoreCalc(self):
        compteur_coeurs = 0
        for card in self.cartes_remportes:
            if card.get_couleur().value == '♥':
                compteur_coeurs = 1 + compteur_coeurs
                self.score = self.score - 5
        if compteur_coeurs == 8:
            self.score += 40
        self.cartes_remportes.clear()

    def getScore(self):
        return self.score

    def update_dataset(self,input,output):
        from JoueurEncoder import JoueurEncoder
        j = JoueurEncoder()
        encoded_input = j.encode_hand(input)
        input_tuple = tuple(encoded_input)
        encoded_output = j.encode_card(output)
        output_tuple = tuple(encoded_output)
        self.input_dataset[input_tuple] = output_tuple

    def set_dataset_score(self, score):
        for input_data in self.input_dataset:
            output = self.input_dataset[input_data]

            updated_output = [elem * score for elem in output]

            self.input_dataset[input_data] = updated_output
