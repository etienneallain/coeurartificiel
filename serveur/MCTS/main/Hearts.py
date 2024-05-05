from enum import Enum

class Rank(Enum):
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

class Suit(Enum):
    CLUBS = 'Clubs'
    DIAMONDS = 'Diamonds'
    SPADES = 'Spades'
    HEARTS = 'Hearts'

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.shorthand = self.set_shorthand()

    def set_shorthand(self):
        rank_dict = {
            Rank.SEVEN: "7",
            Rank.EIGHT: "8",
            Rank.NINE: "9",
            Rank.TEN: "10",
            Rank.JACK: "J",
            Rank.QUEEN: "Q",
            Rank.KING: "K",
            Rank.ACE: "A"
        }
        suit_dict = {
            Suit.SPADES: "\u2660",
            Suit.HEARTS: "\u2661",
            Suit.DIAMONDS: "\u2662",
            Suit.CLUBS: "\u2663"
        }
        return rank_dict[self.rank] + suit_dict[self.suit]
    
    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def print_card(self):
        return f"{self.rank} of {self.suit}"

    def print_card_short(self):
        return self.shorthand
    
    def __lt__(self, other):
        if self.suit == other.get_suit():
            return self.rank.value < other.get_rank().value
        return self.suit.value < other.get_suit().value

    def __eq__(self, other):
        return self.suit == other.get_suit() and self.rank == other.get_rank()

    def copy(self):
        return Card(self.suit, self.rank)

import random

class Deck:
    def __init__(self, to_copy=None):
        if to_copy:
            self.init_counter = to_copy.init_counter
            self.cards = to_copy.cards.copy()
            self.invert_deck = to_copy.invert_deck.copy()
        else:
            self.init_counter = True
            self.cards = []
            self.invert_deck = []
            self.init_deck()
            self.shuffle_deck()

    def init_deck(self):
        if self.init_counter:
            for suit in Suit:
                for rank in Rank:
                    self.cards.append(Card(suit, rank))
            self.init_counter = False

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def print_deck(self):
        for card in self.cards:
            print(card.print_card_short(), end=" ")
        print("\nSize of Deck:", len(self.cards), "\n")

    def print_invert_deck(self):
        for card in self.invert_deck:
            print(card.print_card_short(), end=" ")
        print("\nSize of Invert Deck:", len(self.invert_deck), "\n")

    def draw_card(self):
        if self.cards:
            top_card = self.cards.pop()
            self.invert_deck.append(top_card)
            return top_card
        else:
            raise IndexError("The deck is empty; cannot draw from it!")


    def size(self):
        return len(self.cards)

    def add_card(self, returned):
        self.cards.append(returned)
        for i, card in enumerate(self.invert_deck):
            if card == returned:
                self.invert_deck.pop(i)
                break

    def check_deck(self):
        if len(self.cards) == 32 and len(self.invert_deck) == 0:
            return True
        return False
    
    def copy(self):
        copied_deck = Deck()
        copied_deck.init_counter = self.init_counter
        copied_deck.cards = self.cards.copy()
        copied_deck.invert_deck = self.invert_deck.copy()
        return copied_deck
    
class Game:
    def __init__(self, deck, p1, p2, p3, p4):
        self.players_turn = [p1, p2, p3, p4]
        self.first_player = 0
        self.played_cards = deck
        self.current_trick = []
        self.points = [0, 0, 0, 0]

    def init_game(self):
        self.played_cards.shuffle_deck()
        for player in self.players_turn:
            player.clear_hand()
        for _ in range(8):
            for player in self.players_turn:
                player.add_to_hand(self.played_cards.draw_card())
        for player in self.players_turn:
            player.sort_hand()
            player.print_hand()
        print("\n")
        print(self.players_turn[self.first_player].get_name(), "will play first.\n")
        self.current_trick.clear()
        self.points = [0, 0, 0, 0]

    def print_trick(self, first_player):
        print("\nCards played this round:")
        print("------------------------")
        if not self.current_trick:
            print("No cards have been played this round.")
        for i, card in enumerate(self.current_trick):
            index = (i + first_player) % len(self.players_turn)
            print(f"{self.players_turn[index].get_name():15s} played {card.print_card_short():3s}")

    def check_trick(self, played_card, index):
        if not self.current_trick:
            return True
        first_suit = self.current_trick[0].get_suit()
        if self.players_turn[index].has_suit(first_suit) and played_card.get_suit() != first_suit:
            print(f"You still have a card that is {first_suit}. You must play that first.")
            return False
        return True

    def next_opener(self, first_player):
        first_suit = self.current_trick[0].get_suit()
        largest_rank = self.current_trick[0].get_rank()
        opener = first_player
        for i in range(len(self.players_turn)):
            index = (first_player + i) % len(self.players_turn)
            if self.current_trick[i].get_suit() == first_suit:
                if self.current_trick[i].get_rank().value > largest_rank.value:
                    opener = index
                    largest_rank = self.current_trick[i].get_rank()
        return opener % len(self.players_turn)

    def calculate_points(self):
        pts = 0
        for card in self.current_trick:
            if card.get_suit() == Suit.HEARTS:
                pts -= 5
        return pts

    def print_points(self):
        print("Points received this game:")
        print("--------------------------")

        for player, point in zip(self.players_turn, self.points):
            print(f"{player.get_name()} has {point} points.")
        print()

    def print_winner(self):
        largest_score = self.players_turn[0].get_points()
        index = 0
        for i, player in enumerate(self.players_turn):
            if largest_score < player.get_points():
                index = i
                largest_score = player.get_points()
        print(f"{self.players_turn[index].get_name()} is in the lead after this game.\n")

    def print_total_points(self):
        print("Total cumulative points between all games:")
        print("--------------------------")
        for player in self.players_turn:
            print(f"{player.get_name()} has {player.get_points()} points.")
        print()

    def print_total_moon(self):
        print("Total cumulative moons between all games:")
        print("--------------------------")
        for player in self.players_turn:
            print(f"{player.get_name()} has {player.get_moons()} moons.")
        print()

    def play_new_game(self):
        self.init_game()
        
        for trick_num in range(1, 9):
            print("--------------------------------------------")
            print("Trick #{}:".format(trick_num))
            print("--------------------------------------------")
            self.current_trick.clear()

            for player_num in range(len(self.players_turn)):
                index = (self.first_player + player_num) % len(self.players_turn)
                current_player = self.players_turn[index]
                game_copy = State(self.played_cards, self.current_trick, self.points, index)
                played_card = current_player.do_action(game_copy)

                while not self.check_trick(played_card, index):
                    print("This was an invalid play. Please pick a valid card.")
                    current_player.add_to_hand(played_card)
                    current_player.sort_hand()
                    played_card = current_player.do_action(game_copy)

                print("{} played {}.".format(current_player.get_name(), played_card.print_card_short()))

                self.current_trick.append(played_card)
                self.played_cards.add_card(played_card)

            print("--------------------------------------------")
            print("Trick {} Summary:".format(trick_num))
            print("--------------------------------------------")
            self.print_trick(self.first_player)

            self.first_player = self.next_opener(self.first_player)
            pts = self.calculate_points()
            self.points[self.first_player] += pts
            self.players_turn[self.first_player].add_points(pts)
            
            print("\n{} played the highest card and took {} points this round.\n".format(
                self.players_turn[self.first_player].get_name(), pts))
            
            for i, player in enumerate(self.players_turn):
                if self.points[i] == -40:
                    self.points[i] = 40
                    self.players_turn[i].add_points(80)

            self.print_points()

        print("------------------------------------------")
        print("Game Summary:")
        print("------------------------------------------\n")
        
        self.print_points()

        for i, pts in enumerate(self.points):
            if self.points[i] == 40:
                self.players_turn[i].moons += 1
        
        self.print_winner()
        self.print_total_points()
        self.print_total_moon()

from abc import ABC, abstractmethod
from enum import Enum
import random

class Player(ABC):
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.moons = 0
        self.hand = []

    @abstractmethod
    def do_action(self, state):
        pass

    def add_to_hand(self, card):
        self.hand.append(card)

    def sort_hand(self):
        self.hand.sort()

    def clear_hand(self):
        self.hand.clear()

    def has_suit(self, suit):
        return any(card.get_suit() == suit for card in self.hand)

    def first_suit(self, current_trick):
        if not current_trick:
            return None
        return current_trick[0].get_suit()

    def get_suit_range(self, suit, current_hand):
        range_start = -1
        range_end = -1
        if suit is None:
            return range_start, range_end
        for i, card in enumerate(current_hand):
            if range_start == -1 and card.get_suit() == suit:
                range_start = i
            if range_start != -1 and card.get_suit() != suit:
                range_end = i
                break
        if range_start != -1 and range_end == -1:
            range_end = len(current_hand)
        return range_start, range_end

    def print_hand(self):
        print(f"\n{self.name}'s hand ({len(self.hand)} cards):")
        print("|", end="")
        for i in range(len(self.hand)):
            print(f"{i:3}|", end="")
        print("\n|", end="")
        for card in self.hand:
            print(f"{card.print_card_short():3}|", end="")
        print("")

    def get_name(self):
        return self.name

    def add_points(self, p):
        self.points += p

    def get_points(self):
        return self.points
    
    def get_moons(self):
        return self.moons

    def clear_player(self):
        self.clear_hand()
        self.points = 0
        self.moons = 0

from copy import deepcopy
import random
import time

class MCTSPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        print("MCTSPlayer AI ({}) initialized.".format(name))
        self.simulation_hand = []

        self.root = None
        self.rng = random.Random()

    class Node:
        def __init__(self, state, hand, parent):
            self.state = state
            self.current_hand = hand
            self.best_reward = 0
            self.nb_visits = 0
            self.parent = parent
            self.children = [None] * len(hand)
            self.depth = parent.depth + 1 if parent else 0

    def run_mcts(self, origin, duration_seconds):
        self.root = self.Node(origin, self.simulation_hand, None)
        start_time = time.time()
        while time.time() - start_time < duration_seconds:
            expanded = self.selection(self.root)
            value_change = self.simulation(expanded)
            self.back_prop(expanded, value_change)
        return self.best_reward_child(self.root)


    def selection(self, root):
        this_node = root
        while this_node.state.valid_game(): # and self.all_children_explored(this_node)
            first_suit = self.first_suit(this_node.state.current_trick)
            range_start, range_end = self.get_suit_range(first_suit, this_node.current_hand)

            if first_suit is None:
                range_start, range_end = 0, len(this_node.current_hand)
            elif range_start == -1:
                range_start, range_end = 0, len(this_node.current_hand)

            for i in range(range_start, range_end):
                if this_node.children[i] is None:
                    return self.expansion(this_node, i)

            this_node = self.best_child_uct(this_node, 1.4)

        return this_node

    def all_children_explored(self, node):
        for child in node.children:
            if child is None:
                return False
        return True

    def expansion(self, parent, child_num):
        child_state = deepcopy(parent.state)
        child_hand = parent.current_hand[:]
        play_card = child_hand.pop(child_num)
        debug = child_state.advance(play_card, child_hand)
        if debug == -1:
            print("Error, we've made a mistake.")
        parent.children[child_num] = self.Node(child_state, child_hand, parent)
        return parent.children[child_num]

    def best_child_uct(self, parent, weight):
        best_index = 0
        best_value = -float('inf')
        total_visits = parent.nb_visits

        for i, child in enumerate(parent.children):
            if child is not None:
                reward = child.best_reward
                child_visits = child.nb_visits
                this_value = (reward / child_visits) + weight * (2 * (total_visits ** 0.5) / child_visits) ** 0.5
                if this_value > best_value:
                    best_value = this_value
                    best_index = i

        return parent.children[best_index]

    def simulation(self, start):
        final_state = deepcopy(start.state)
        final_hand = deepcopy(start.current_hand)

        while final_state.valid_game():
            first_suit = self.first_suit(final_state.current_trick)
            range_start, range_end = self.get_suit_range(first_suit, final_hand)
            #print(first_suit)
            #print(final_hand)

            if first_suit is None:
                while True:
                    if not final_hand:
                        break
                    index = self.rng.randint(0, len(final_hand) - 1)
                    play_card = final_hand.pop(index)
                    debug = final_state.advance(play_card, final_hand)
                    if debug != -1:
                        break
                    else:
                        final_hand.append(play_card)
                        final_hand.sort()
            else:
                if range_end - range_start == 0:
                    play_card = final_hand.pop(self.rng.randint(0, len(final_hand) - 1))
                    final_state.advance(play_card, final_hand)
                else:
                    index = range_start + self.rng.randint(0, range_end - range_start - 1)
                    play_card = final_hand.pop(index)
                    final_state.advance(play_card, final_hand)
        
        rank = final_state.get_ranking()
        if rank == 1:
            return 1
        if rank == 4:
            return -1
        else:
            return 0

    def back_prop(self, start, reward):
        node = start
        while node is not None:
            node.nb_visits += 1
            node.best_reward += reward
            node = node.parent

    def best_reward_child(self, root):
        highest_reward = -float('inf')
        best_child_num = 0

        for i, child in enumerate(root.children):
            if child is not None and child.best_reward > highest_reward:
                highest_reward = child.best_reward
                best_child_num = i

        return best_child_num

    def do_action(self, state):
        self.simulation_hand.clear()
        self.simulation_hand.extend(self.hand)

        if len(self.hand) == 1:
            return self.hand.pop()

        return self.hand.pop(self.run_mcts(state, 10))

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

import random

class RandomPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.rng = random.Random()
        print(f"Random Player ({name}) initialized.")

    def do_action(self, state):
        first_suit = self.first_suit(state.current_trick)

        if first_suit is None:
            index = self.rng.randint(0, len(self.hand) - 1)
            return self.hand.pop(index)

        range_start, range_end = self.get_suit_range(first_suit, self.hand)

        if range_end - range_start == 0:
            return self.hand.pop(self.rng.randint(0, len(self.hand) - 1))
        
        index = self.rng.randint(0, range_end - range_start - 1)
        return self.hand.pop(range_start + index)

if __name__ == "__main__":
    deck = Deck()
    deck.print_deck()

    p1 = RandomPlayer("RNG1")
    p2 = RandomPlayer("RNG2")
    p3 = RandomPlayer("RNG3")
    p4 = MCTSPlayer("MCTS")

    # Play Multiple Games
    number_of_games = 5000
    total_scores = [0] * 4
    game = Game(deck, p1, p2, p3, p4)
    for i in range(1, number_of_games + 1):
        print("\n--------------------------------------------")
        print("--------------------------------------------")
        print("--------------------------------------------")
        print("Playing Game #", i)
        print("--------------------------------------------")
        print("--------------------------------------------")
        print("--------------------------------------------\n")
        game.play_new_game()
        for j, player in enumerate([p1, p2, p3, p4]):
            total_scores[j] = player.get_points()

    print("\n--------------------------------------------")
    print("--------------------------------------------")
    print("Total Scores:")
    print("--------------------------------------------")
    for i, player in enumerate(["RNG1", "RNG2", "RNG3", "MCTS"]):
        print(player, ":", total_scores[i])

    print("\n--------------------------------------------")
    print("--------------------------------------------")
    print("Average Scores:")
    print("--------------------------------------------")
    average_scores = [total_score / number_of_games for total_score in total_scores]
    for i, player in enumerate(["RNG1", "RNG2", "RNG3", "MCTS"]):
        print(player, ":", average_scores[i])