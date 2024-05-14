import random
from Card import Suit

class State:
    def __init__(self, deck, trick, scores, index):
        self.played_cards = deck.copy()
        self.current_trick = trick.copy()
        self.points = scores.copy()
        self.player_turn = index
        self.rng = random.Random()

    def get_trick_number(self):
        return len(self.played_cards.cards) // 4 + 1

    def valid_game(self):
        return len(self.played_cards.invert_deck) > 0

    def valid_trick(self):
        return len(self.current_trick) < 4

    def get_points(self):
        return self.points[self.player_turn]
    
    def get_ranking(self):
        player_score = self.points[self.player_turn]
        num_players = len(self.points)
        better_players = sum(score > player_score for score in self.points)
        equal_players = sum(score == player_score for score in self.points)

        if better_players == 0:
            return 1  # Votre joueur est le meilleur, donc classé en premier
        elif better_players + equal_players == num_players:
            return num_players  # Votre joueur est le pire, donc classé en dernier
        else:
            return better_players + 1  # Votre joueur est classé entre les autres joueurs avec un score différent

    def is_in_my_hand(self, card, simulation_hand):
        return card in simulation_hand

    def play_card(self, card):
        for c in self.played_cards.invert_deck:
            if c == card:
                self.played_cards.cards.append(c)
                self.played_cards.invert_deck.remove(c)
                self.current_trick.append(c)
                break

    def valid_move(self, card, simulation_hand):
        if not self.current_trick:
            return True
        first_suit = self.current_trick[0].get_suit()
        if first_suit != card.get_suit():
            if any(c.get_suit() == first_suit for c in simulation_hand):
                return False
        return True
    
    def calculate_points(self):
        pts = 0
        for card in self.current_trick:
            if card.get_suit() == Suit.HEARTS:
                pts -= 5
        return pts

    def next_opener(self, first_player):
        first_suit = self.current_trick[0].get_suit()
        largest_rank = self.current_trick[0].get_rank()
        opener = first_player
        for i in range(len(self.points)):
            index = (first_player + i) % len(self.points)
            if self.current_trick[i].get_suit() == first_suit:
                if self.current_trick[i].get_rank().value > largest_rank.value:
                    opener = index
                    largest_rank = self.current_trick[i].get_rank()
        return opener % len(self.points)

    def advance(self, card, simulation_hand):
        #self.played_cards.print_invert_deck()
        if not self.valid_move(card, simulation_hand):
            return -1

        play_turn = len(self.current_trick)
        self.play_card(card)
        #self.played_cards.print_invert_deck()

        while self.valid_trick() and self.played_cards.invert_deck:
            first_suit = self.current_trick[0].get_suit()
            possible_cards = [c for c in self.played_cards.invert_deck if c.get_suit() == first_suit]
            if possible_cards:  # If there are cards of the right suit left
                possible_cards_out_of_my_hand = [c for c in possible_cards if not self.is_in_my_hand(c, simulation_hand)]
                if possible_cards_out_of_my_hand: # If there are some of them that are not in my hand -> play one of them
                    index = self.rng.randint(0, len(self.played_cards.invert_deck) - 1)
                    while self.played_cards.invert_deck[index] not in possible_cards_out_of_my_hand:
                        index = self.rng.randint(0, len(self.played_cards.invert_deck) - 1)
                else: # If all of them are in my hand -> play any card that is not in my hand no matter of the suit
                    index = self.rng.randint(0, len(self.played_cards.invert_deck) - 1)
                    while self.is_in_my_hand(self.played_cards.invert_deck[index], simulation_hand):
                        index = self.rng.randint(0, len(self.played_cards.invert_deck) - 1)
            else:  # No cards of the right suit left -> play any card that is not in my hand
                index = self.rng.randint(0, len(self.played_cards.invert_deck) - 1)
                while self.is_in_my_hand(self.played_cards.invert_deck[index], simulation_hand):
                    index = self.rng.randint(0, len(self.played_cards.invert_deck) - 1)

            self.play_card(self.played_cards.invert_deck[index])
            #self.played_cards.print_invert_deck()


        first_player = (self.player_turn - play_turn + len(self.points)) % len(self.points)
        reward = self.calculate_points()
        opener = self.next_opener(first_player)
        self.points[opener] += reward
        if self.points[opener] == -40:
            self.points[opener] = 40

        return_points = reward if opener == self.player_turn else 0

        self.current_trick.clear()

        if self.valid_game():
            while opener != self.player_turn:
                if len(self.current_trick) == 0:  # First card of the trick to be played -> any suit but not a card that is in my hand
                    index = self.rng.randint(0, len(self.played_cards.invert_deck) - 1)
                    while self.is_in_my_hand(self.played_cards.invert_deck[index], simulation_hand):
                        index = self.rng.randint(0, len(self.played_cards.invert_deck) - 1)
                else:
                    first_suit = self.current_trick[0].get_suit()
                    possible_cards = [c for c in self.played_cards.invert_deck if c.get_suit() == first_suit]
                    if possible_cards:  # If there are cards of the right suit left
                        possible_cards_out_of_my_hand = [c for c in possible_cards if not self.is_in_my_hand(c, simulation_hand)]
                        if possible_cards_out_of_my_hand: # If there are some of them that are not in my hand -> play one of them
                            index = self.rng.randint(0, len(self.played_cards.invert_deck) - 1)
                            while self.played_cards.invert_deck[index] not in possible_cards_out_of_my_hand:
                                index = self.rng.randint(0, len(self.played_cards.invert_deck) - 1)
                        else: # If all of them are in my hand -> play any card that is not in my hand no matter of the suit
                            index = self.rng.randint(0, len(self.played_cards.invert_deck) - 1)
                            while self.is_in_my_hand(self.played_cards.invert_deck[index], simulation_hand):
                                index = self.rng.randint(0, len(self.played_cards.invert_deck) - 1)
                    else:  # No cards of the right suit left -> play any card that is not in my hand
                        index = self.rng.randint(0, len(self.played_cards.invert_deck) - 1)
                        while self.is_in_my_hand(self.played_cards.invert_deck[index], simulation_hand):
                            index = self.rng.randint(0, len(self.played_cards.invert_deck) - 1)

                self.play_card(self.played_cards.invert_deck[index])
                #self.played_cards.print_invert_deck()
                opener = (opener + 1) % len(self.points)

        return return_points