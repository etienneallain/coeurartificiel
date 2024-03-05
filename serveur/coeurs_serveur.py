#from flask import Flask, request, jsonify
import random
#from flask_cors import CORS

#app = Flask(__name__)
#CORS(app)

listOfPossibleCards = [...]

listOfIa = {}


class Suit:
    hearts, diamonds, clubs, spades = range(4)

class Rank:
    seven, eight, nine, ten, jack, queen, king, ace = range(8)


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank


class Player:
    def __init__(self, number):
        self.number = number
        self.hand = []
        self.list_of_trick = {}

    def get_cards_in_suit(self, suit):
        return [card for card in self.hand if card.suit == suit]

    def move_allowed(self, played_card, current_trick):
        if not current_trick:
            return True
        
        lead_suit = current_trick[0].suit
        
        if played_card.suit == lead_suit:
            return True
        else:
            cards_in_lead_suit = self.get_cards_in_suit(lead_suit)
            if not cards_in_lead_suit:
                return True
            else:
                return False

    def play_card(self, card, current_trick):
        if card in self.hand and self.move_allowed(card, current_trick):
            self.hand.remove(card)
            return True
        else:
            return False

    def get_possible_cards(self, current_trick):
        lead_suit = current_trick[0].suit if current_trick else None
        
        if lead_suit is None:
            return list(self.hand)
        else:
            cards_in_lead_suit = self.get_cards_in_suit(lead_suit)
            if cards_in_lead_suit:
                return list(cards_in_lead_suit)
            else:
                return list(self.hand)


class Trick:
    def __init__(self):
        self.trick = []

    def is_empty(self):
        return not self.trick

    def add_card(self, card):
        self.trick.append(card)


class HeartsGame:
    def __init__(self, player_numbers, current_player):
        self.players = [Player(player_number) for player_number in player_numbers]
        self.deck = [Card(suit, rank) for suit in range(4) for rank in range(8)]
        self.trick_map = {}
        self.turn = 0
        self.current_trick = Trick()
        self.current_player = current_player
        self.scores = [0, 0, 0, 0]

    def check_winner_trick(self, trick):
        if not trick:
            return -1

        lead_suit = trick[0].suit
        winning_card = trick[0]
        winning_player_index = 0

        for i in range(1, len(trick)):
            current_card = trick[i]
            if current_card.suit == lead_suit and current_card.rank > winning_card.rank:
                winning_card = current_card
                winning_player_index = i

        return winning_player_index

    def end_of_game(self):
        return all(len(player.hand) == 0 for player in self.players)

    def play_card(self, player, card):
        if player.play_card(card, self.current_trick):
            self.current_trick.add_card(card)
        else:
            return

        if self.turn % 4 == 3:
            self.current_player = self.check_winner_trick(self.current_trick)
            print(f'Trick Winner: Player {self.current_player}')
            self.players[self.current_player].list_of_trick[len(self.trick_map)] = self.current_trick
            self.score()
            self.trick_map[len(self.trick_map)] = self.current_trick
            self.current_trick = Trick()
            self.turn = 0
        else:
            self.current_player = (self.current_player + 1) % 4
            self.turn += 1

    def score(self):
        for i in range(4):
            nb_hearts = sum(1 for trick in self.players[i].list_of_trick.values() for card in trick if card.suit == Suit.hearts)
            res = -nb_hearts * 5
            if nb_hearts == 8:
                res += 40
            self.scores[i] = res


# @app.route('/initialisation', methods=['POST'])
# def initialisation():
#     global listOfIa
#
#     data = request.json
#
#     if 'ia_players' in data:
#         ia_players = data['ia_players']
#
#         for joueur in ia_players:
#             id_joueur = joueur.get('id')
#             type_joueur = joueur.get('type')
#
#             listOfIa[id_joueur] = type_joueur
#             print(listOfIa)
#         return 'Initialisation réussie'
#
#     else:
#         return 'Données JSON invalides', 400
#
#
#
# @app.route('/play_move', methods=['POST'])
# def play_move():
#     global listOfPossibleCards
#
#     # Récupère la taille envoyée par le client
#     data = request.json
#     taille = data.get('taille')
#     print("la taille est : "+ str(taille))
#     random_index = random.randint(0, taille - 1)
#     print("le nombre choisi est : "+ str(random_index))
#     return jsonify({'nombre_aleatoire': str(random_index)})
#
#
# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=5000)
