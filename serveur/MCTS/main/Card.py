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