import unittest
from copy import deepcopy
from Hearts import State, Deck, Card, Suit, Rank

class TestState(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()
        self.card = self.deck.draw_card()
        self.trick = [Card(Suit.HEARTS, Rank.ACE), Card(Suit.CLUBS, Rank.SEVEN), Card(Suit.HEARTS, Rank.SEVEN)]
        self.scores = [0, 0, 0, 0]
        self.index = 0
        self.state = State(self.deck, self.trick, self.scores, self.index)

    def test_get_trick_number(self):
        self.assertEqual(self.state.get_trick_number(), 8)

    def test_valid_game(self):
        self.assertTrue(self.state.valid_game())
        self.state.played_cards.add_card(self.card)
        self.assertFalse(self.state.valid_game())

    def test_valid_trick(self):
        self.state.current_trick = [Card(Suit.HEARTS, Rank.KING)]
        self.assertTrue(self.state.valid_trick())
        self.state.current_trick = [Card(Suit.HEARTS, Rank.KING), Card(Suit.HEARTS, Rank.QUEEN)]
        self.assertTrue(self.state.valid_trick())
        self.state.current_trick = [Card(Suit.HEARTS, Rank.KING), Card(Suit.HEARTS, Rank.QUEEN), Card(Suit.HEARTS, Rank.JACK)]
        self.assertTrue(self.state.valid_trick())
        self.state.current_trick = [Card(Suit.HEARTS, Rank.KING), Card(Suit.HEARTS, Rank.QUEEN), Card(Suit.HEARTS, Rank.JACK), Card(Suit.HEARTS, Rank.TEN)]
        self.assertFalse(self.state.valid_trick())

    def test_get_points(self):
        self.assertEqual(self.state.get_points(), 0)
        self.state.points = [10, 0, 0, 0]
        self.assertEqual(self.state.get_points(), 10)

    def test_get_ranking(self):
        self.assertEqual(self.state.get_ranking(), 1)
        self.state.points = [10, 10, 0, 0]
        self.assertEqual(self.state.get_ranking(), 1)
        self.state.points = [10, 15, 0, 0]
        self.assertEqual(self.state.get_ranking(), 2)
        self.state.points = [0, 10, 0, 0]
        self.assertEqual(self.state.get_ranking(), 4)
        self.state.points = [10, 20, 15, 0]
        self.assertEqual(self.state.get_ranking(), 3)
        self.state.points = [10, 10, 20, 0]
        self.assertEqual(self.state.get_ranking(), 2)

    def test_is_in_my_hand(self):
        simulation_hand = [Card(Suit.HEARTS, Rank.SEVEN), Card(Suit.HEARTS, Rank.EIGHT)]
        self.assertTrue(self.state.is_in_my_hand(Card(Suit.HEARTS, Rank.SEVEN), simulation_hand))
        self.assertFalse(self.state.is_in_my_hand(Card(Suit.HEARTS, Rank.TEN), simulation_hand))

    def test_play_card(self):
        card = self.card
        self.state.play_card(card)
        self.assertIn(card, self.state.played_cards.cards)
        self.assertNotIn(card, self.state.played_cards.invert_deck)
        self.assertIn(card, self.state.current_trick)

    def test_valid_move(self):
        simulation_hand = [Card(Suit.HEARTS, Rank.NINE), Card(Suit.HEARTS, Rank.EIGHT)]
        self.assertTrue(self.state.valid_move(Card(Suit.HEARTS, Rank.TEN), simulation_hand))
        self.assertFalse(self.state.valid_move(Card(Suit.DIAMONDS, Rank.JACK), simulation_hand))
        simulation_hand = [Card(Suit.CLUBS, Rank.NINE), Card(Suit.DIAMONDS, Rank.EIGHT)]
        self.assertTrue(self.state.valid_move(Card(Suit.CLUBS, Rank.TEN), simulation_hand))

    def test_calculate_points(self):
        self.state.current_trick = [Card(Suit.HEARTS, Rank.SEVEN), Card(Suit.HEARTS, Rank.EIGHT), Card(Suit.HEARTS, Rank.NINE)]
        self.assertEqual(self.state.calculate_points(), -15)

    def test_next_opener(self):
        card = self.card
        self.state.play_card(card)
        first_player = 2
        self.assertEqual(self.state.next_opener(first_player), 2)

    def test_advance(self):
        simulation_hand = []
        card = self.card
        self.assertEqual(self.state.advance(card, simulation_hand), self.state.calculate_points())
        self.assertEqual(self.state.get_points(), self.state.calculate_points())
        self.assertEqual(len(self.state.current_trick), 0)

if __name__ == '__main__':
    unittest.main()
