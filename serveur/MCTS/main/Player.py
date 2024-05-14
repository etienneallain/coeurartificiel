from abc import ABC, abstractmethod
from enum import Enum

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