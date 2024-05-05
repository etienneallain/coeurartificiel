import time

import torch

from JoueurEncoder import JoueurEncoder
from paquet import Paquet

negative_infinity = float('-inf')


def standardize_score(score):
    min_score = -35
    max_score = 40

    min_scale = -1
    max_scale = 1

    scaled_score = (score - min_score) / (max_score - min_score)

    standardized_score = min_scale + (max_scale - min_scale) * scaled_score

    return standardized_score


class Player:
    def __init__(self, name):
        self.name = name
        self.cartes = []
        self.input_dataset = {}
        self.cartes_remportes = []
        self.score = 0
        self.flag_hearts = 1

    def __str__(self):
        return f"{self.name}: {' '.join(str(card) for card in self.cartes)}"

    def play_card(self, color, encoded_input_data):
        raise NotImplementedError("Method 'play_card' must be implemented by subclasses")

    def jouer_nn(self, carte):
        self.cartes.remove(carte)

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

    def get_name(self):
        return self.name

    def ouvrir(self):
        return self.cartes.pop()

    def scoreCalc(self):
        compteur_coeurs = 0
        for card in self.cartes_remportes:
            if card.get_couleur().value == '♥':
                compteur_coeurs = 1 + compteur_coeurs
                self.score = self.score - 5
        if compteur_coeurs == 8:
            self.score = 40
        self.cartes_remportes.clear()

    def getScore(self):
        return self.score

    def encode_input(self, numero_pli, cards_in_hand, playable_cards, cartes_du_pli, couleur, ordre_joueur,
                     flag_hearts):
        from JoueurEncoder import JoueurEncoder
        j1 = JoueurEncoder()
        all_encoded_data = []
        all_encoded_data.extend(j1.encode_cards(playable_cards))
        all_encoded_data.extend(j1.encode_cards(cards_in_hand))
        all_encoded_data.extend(j1.encode_cards(cartes_du_pli))
        all_encoded_data.extend(j1.encode_numero_pli(numero_pli))
        all_encoded_data.extend(j1.encode_ordre_joueur(ordre_joueur))
        all_encoded_data.extend(j1.encode_couleur(couleur))
        all_encoded_data.append(flag_hearts)
        return torch.tensor(all_encoded_data, dtype=torch.float)

    def update_dataset(self, numero_pli, cards_in_hand, playable_cards, cartes_du_pli, couleur, ordre_joueur,
                       flag_hearts, output):
        from JoueurEncoder import JoueurEncoder
        j = JoueurEncoder()
        all_encoded_data = []
        all_encoded_data.extend(j.encode_cards(playable_cards))
        all_encoded_data.extend(j.encode_cards(cards_in_hand))
        all_encoded_data.extend(j.encode_cards(cartes_du_pli))
        all_encoded_data.extend(j.encode_numero_pli(numero_pli))
        all_encoded_data.extend(j.encode_ordre_joueur(ordre_joueur))
        all_encoded_data.extend(j.encode_couleur(couleur))
        all_encoded_data.append(flag_hearts)
        encoded_output = j.encode_card(output)
        output_tuple = tuple(encoded_output)

        self.input_dataset[tuple(all_encoded_data)] = output_tuple

    def set_dataset_score(self, score):
        standardized_score = standardize_score(score)
        for input_data in self.input_dataset:
            output = self.input_dataset[input_data]
            updated_output = [elem * standardized_score if elem == 1 else 0 for elem in output]
            self.input_dataset[input_data] = updated_output

    def get_input_data(self):
        return self.input_dataset

    def get_true_count(self, trick_cards):
        return sum(card is not None for card in trick_cards)


class RandomPlayer(Player):

    def __init__(self, name):
        Player.__init__(self, name)

    def play_card(self, couleur, encoded_input_data):
        if couleur is None:
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


class NNPlayer(Player):

    def __init__(self, name, neural_network):
        super().__init__(name)
        self.neural_network = neural_network

    def play_card(self, color, encoded_input_data):

        static_pack = Paquet()
        cards_in_hand = self.get_cartes()
        has_color = False

        with torch.no_grad():
            output = self.neural_network(encoded_input_data.clone().detach().requires_grad_(True))
        for card in cards_in_hand:
            if card.get_couleur() == color:
                has_color = True
        if has_color:
            playable_mask = [1 if card in cards_in_hand and card.get_couleur() == color else negative_infinity for card
                             in static_pack.cartes]
        else:
            playable_mask = [1 if card in cards_in_hand else negative_infinity for card in static_pack.cartes]

        masked_output = output.clone()
        for i, value in enumerate(playable_mask):
            if value == negative_infinity:
                masked_output[i] = negative_infinity

        best_card_index = torch.argmax(masked_output).item()
        je = JoueurEncoder()
        best_card = je.decode_card_index(best_card_index)

        self.cartes.remove(best_card)

        return best_card
