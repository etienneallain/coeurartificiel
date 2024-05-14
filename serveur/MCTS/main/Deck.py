import random
from Card import Rank, Suit, Card

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