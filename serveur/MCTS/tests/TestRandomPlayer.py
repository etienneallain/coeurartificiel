import unittest
from main.Card import Card, Rank, Suit
from main.RandomPlayer import RandomPlayer
from main.State import State

class TestRandomPlayer(unittest.TestCase):

    def setUp(self):
        self.player = RandomPlayer("TestPlayer")

    def test_do_action_with_empty_trick(self):
        state = State([], [], [], 0)
        state.current_trick = []
        self.player.hand = [Card(Suit.HEARTS, Rank.KING), Card(Suit.CLUBS, Rank.SEVEN)]
        action = self.player.do_action(state)
        self.assertTrue(action == Card(Suit.HEARTS, Rank.KING) or action == Card(Suit.CLUBS, Rank.SEVEN))

    def test_do_action_with_nonempty_trick(self):
        state = State([], [], [], 0)
        state.current_trick = [Card(Suit.HEARTS, Rank.ACE)]
        self.player.hand = [Card(Suit.HEARTS, Rank.KING), Card(Suit.CLUBS, Rank.SEVEN)]
        action = self.player.do_action(state)
        self.assertEqual(action.get_suit(), Suit.HEARTS) # Le joueur a une carte de la couleur du pli
        self.player.hand = [Card(Suit.SPADES, Rank.KING), Card(Suit.CLUBS, Rank.SEVEN)]
        action = self.player.do_action(state)
        self.assertNotEqual(action.get_suit(), Suit.HEARTS) # Le joueur n'a pas de carte de la couleur du pli

    def test_do_action_with_single_card(self):
        state = State([], [], [], 0)
        state.current_trick = [Card(Suit.HEARTS, Rank.ACE)]
        self.player.hand = [Card(Suit.HEARTS, Rank.KING)]
        action = self.player.do_action(state)
        self.assertEqual(action, Card(Suit.HEARTS, Rank.KING))
        self.player.hand = [Card(Suit.CLUBS, Rank.KING)]
        action = self.player.do_action(state)
        self.assertEqual(action, Card(Suit.CLUBS, Rank.KING))

if __name__ == '__main__':
    unittest.main()
