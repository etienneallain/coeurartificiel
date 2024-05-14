import unittest
from main.Card import Card, Rank, Suit

class TestCard(unittest.TestCase):
    def test_creation(self):
        card = Card(Suit.HEARTS, Rank.SEVEN)
        self.assertEqual(card.get_suit(), Suit.HEARTS)
        self.assertEqual(card.get_rank(), Rank.SEVEN)

    def test_set_shorthand(self):
        card = Card(Suit.HEARTS, Rank.SEVEN)
        self.assertEqual(card.set_shorthand(), "7♡")

    def test_get_suit_and_rank(self):
        card = Card(Suit.SPADES, Rank.JACK)
        self.assertEqual(card.get_suit(), Suit.SPADES)
        self.assertEqual(card.get_rank(), Rank.JACK)

    def test_print_card(self):
        card = Card(Suit.DIAMONDS, Rank.ACE)
        self.assertEqual(card.print_card(), "Rank.ACE of Suit.DIAMONDS")

    def test_print_card_short(self):
        card = Card(Suit.CLUBS, Rank.TEN)
        self.assertEqual(card.print_card_short(), "10♣")

    def test_comparison_methods(self): # Suit order is : CLUBS, DIAMONDS, HEARTS, SPADES
        card1 = Card(Suit.HEARTS, Rank.SEVEN)
        card2 = Card(Suit.HEARTS, Rank.TEN)
        card3 = Card(Suit.SPADES, Rank.SEVEN)
        card4 = Card(Suit.HEARTS, Rank.SEVEN)
        self.assertTrue(card1 < card2)
        self.assertTrue(card1 < card3)
        self.assertTrue(card1 != card2)
        self.assertTrue(card1 == card4)

    def test_copy_method(self):
        original_card = Card(Suit.DIAMONDS, Rank.QUEEN)
        copied_card = original_card.copy()
        self.assertEqual(original_card.get_suit(), copied_card.get_suit())
        self.assertEqual(original_card.get_rank(), copied_card.get_rank())

if __name__ == '__main__':
    unittest.main()
