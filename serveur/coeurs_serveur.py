from flask import Flask, request, jsonify
import random
from flask_cors import CORS
from pythonProject.src.paquet import json_to_cards
from pythonProject.src.Play import select_best_card_with_NN
from pythonProject.src.paquet import transform_color_name
from pythonProject.src.paquet import parsing_of_card_to_return

app = Flask(__name__)
CORS(app)
listOfPossibleCards = [...]
listOfIa = {}

@app.route('/initialisation', methods=['POST'])
def initialisation():
    global listOfIa

    data = request.json

    if 'ia_players' in data:
        ia_players = data['ia_players']

        for joueur in ia_players:
            id_joueur = joueur.get('id')
            type_joueur = joueur.get('type')

            listOfIa[id_joueur] = type_joueur
            print(listOfIa)
        return 'Initialisation réussie'

    else:
        return 'Données JSON invalides', 400



@app.route('/play_move', methods=['POST'])
def play_move():
    global listOfPossibleCards

    # Récupère la taille envoyée par le client
    data = request.json
    taille = data.get('taille')
    trick_number = data.get('trick_number')
    cards_in_hand = data.get('cards_in_hand')
    card_played_in_trick=data.get('card_played_in_trick')
    trump_color = data.get('trump_color')
    order_of_play = data.get('order_of_play')
    playable_cards = data.get('playable_cards')
    flag = data.get('flag')
    parsed_cards_in_hand = json_to_cards(cards_in_hand)
    parsed_card_played_in_trick = json_to_cards(card_played_in_trick)
    parsed_playable_cards = json_to_cards(playable_cards)
    parsed_color_name = transform_color_name(trump_color)
    card_to_be_played = select_best_card_with_NN(trick_number,parsed_cards_in_hand,parsed_playable_cards,parsed_card_played_in_trick,parsed_color_name,order_of_play,flag)
    print(card_to_be_played)
    suit,rank = parsing_of_card_to_return(card_to_be_played)
    print(suit)
    print(rank)
    return jsonify({'suit': suit,'rank': rank})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
