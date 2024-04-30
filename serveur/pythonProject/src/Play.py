import torch

from src.JoueurEncoder import JoueurEncoder
from src.NeuralNetwork import load_model
from src.paquet import Paquet


def select_best_card_with_NN(numero_pli, cards_in_hand, playable_cards, cartes_du_pli, couleur, ordre_joueur, flag_hearts):
    static_pack = Paquet()
    neural_network= load_model(112, 32, "trained_model_1.pth")
    # Encode the input data
    encoded_input_data = encode_input(numero_pli, cards_in_hand, playable_cards, cartes_du_pli, couleur, ordre_joueur,flag_hearts)

    # Pass input data through the neural network
    with torch.no_grad():
        output = neural_network(encoded_input_data.clone().detach().requires_grad_(True))

    playable_mask = [1 if card in cards_in_hand else -100 for card in static_pack.cartes]

    # Apply the mask to the output
    masked_output = output.clone()  # Create a copy of the output tensor
    for i, value in enumerate(playable_mask):
        if value == -100:
            masked_output[i] = -100
    # Select the index of the card with the highest score
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