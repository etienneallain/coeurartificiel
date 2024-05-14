import unittest
from main.Card import Card, Rank, Suit
from main.Deck import Deck

class TestDeck(unittest.TestCase):

    def test_init_deck(self):
        deck = Deck()
        expected_card_count = 32
        self.assertEqual(len(deck.cards), expected_card_count)
        suits = [Suit.SPADES, Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS]
        ranks = [Rank.SEVEN, Rank.EIGHT, Rank.NINE, Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING, Rank.ACE]
        for suit in suits:
            for rank in ranks:
                self.assertIn(Card(suit, rank), deck.cards)

    def test_shuffle_deck(self):
        deck = Deck()
        original_order = deck.cards.copy()
        deck.shuffle_deck()
        self.assertNotEqual(deck.cards, original_order)

    def test_draw_card(self):
        deck = Deck()
        card = deck.draw_card()
        self.assertIsInstance(card, Card)
        self.assertEqual(len(deck.cards), 31)
        for _ in range(31):
            deck.draw_card()
        with self.assertRaises(IndexError):
            deck.draw_card()

    def test_add_card(self):
        deck = Deck()
        card = Card(Suit.SPADES, Rank.SEVEN)
        deck.add_card(card)
        self.assertIn(card, deck.cards)
        self.assertEqual(len(deck.cards), 33)

    def test_check_deck(self):
        deck = Deck()
        self.assertTrue(deck.check_deck())
        deck.add_card(Card(Suit.SPADES, Rank.SEVEN))
        self.assertFalse(deck.check_deck())

    def test_copy(self):
        deck = Deck()
        deck_copy = deck.copy()
        self.assertEqual(len(deck.cards), len(deck_copy.cards))
        self.assertEqual(deck.cards, deck_copy.cards)

if __name__ == '__main__':
    unittest.main()
