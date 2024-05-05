import unittest
from copy import deepcopy
from Hearts import MCTSPlayer, State, Rank, Suit, Card

class TestNode(unittest.TestCase):
    def setUp(self):
        self.player = MCTSPlayer("TestPlayer")
        
    def test_create_node(self):
        state = State([], [], [], 0)
        hand = [Card(Suit.HEARTS, Rank.KING), Card(Suit.CLUBS, Rank.SEVEN)]
        node = self.player.Node(state, hand, None)
        self.assertEqual(node.state, state)
        self.assertEqual(node.current_hand, hand)
        self.assertEqual(node.best_reward, 0)
        self.assertEqual(node.nb_visits, 0)
        self.assertIsNone(node.parent)
        self.assertEqual(len(node.children), len(hand))
        self.assertEqual(node.depth, 0)