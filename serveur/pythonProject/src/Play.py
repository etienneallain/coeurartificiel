import torch

from JoueurEncoder import JoueurEncoder
from NeuralNetwork import load_model
from paquet import Paquet
from Player import negative_infinity

def select_best_card_with_NN(numero_pli, cards_in_hand, playable_cards, cartes_du_pli, couleur, ordre_joueur, flag_hearts):
    static_pack = Paquet()
    neural_network= load_model(113, 32, "good_nns/good_boy_3b.pth")
    # Encode the input data
    encoded_input_data = encode_input(numero_pli, cards_in_hand, playable_cards, cartes_du_pli, couleur, ordre_joueur,flag_hearts)

    has_color = False

    with torch.no_grad():
        output = neural_network(encoded_input_data.clone().detach().requires_grad_(True))
    for card in cards_in_hand:
        if card.get_couleur() == couleur:
            has_color = True
    if has_color:
        playable_mask = [1 if card in cards_in_hand and card.get_couleur() == couleur else negative_infinity for card
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

    return best_card


def encode_input(numero_pli, cards_in_hand, playable_cards, cartes_du_pli, couleur, ordre_joueur,
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