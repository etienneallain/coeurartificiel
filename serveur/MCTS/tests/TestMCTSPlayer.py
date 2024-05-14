import unittest
from copy import deepcopy
from main.Card import Card, Rank, Suit
from main.Deck import Deck
from main.MCTSPlayer import MCTSPlayer
from main.State import State

class TestMCTSPlayer(unittest.TestCase):
    def setUp(self):
        self.player = MCTSPlayer("TestPlayer")

    def test_selection(self):
        # Situation 1: Parent is the first node created for selection
        deck = Deck()
        card = deck.draw_card()
        parent_state = State(deck, [Card(Suit.HEARTS, Rank.KING), Card(Suit.CLUBS, Rank.SEVEN), Card(Suit.HEARTS, Rank.SEVEN)], [0, 0, 0, 0], 0)
        parent_hand = [card]
        parent_node = self.player.Node(parent_state, parent_hand, None)
        selected_node = self.player.selection(parent_node)
        self.assertEqual(selected_node, parent_node.children[0])

        # Situation 2: All children have rewards and visits set, and the first child has the highest UCT value
        parent_state = State(Deck(), [], [], 0)
        parent_hand = [Card(Suit.HEARTS, Rank.KING), Card(Suit.CLUBS, Rank.SEVEN)]
        parent_node = self.player.Node(parent_state, parent_hand, None)
        parent_node.children = [self.player.Node(parent_state, parent_hand, parent_node) for _ in range(len(parent_hand))]
        for i, child in enumerate(parent_node.children):
            child.best_reward = i + 1  # Set rewards
            child.nb_visits = 10 * (i + 1)  # Set visits
        selected_node = self.player.selection(parent_node)
        highest_uct_child = parent_node.children[0]
        self.assertEqual(selected_node.state, highest_uct_child.state)
        self.assertEqual(selected_node.current_hand, highest_uct_child.current_hand)

    def test_expansion(self):
        # Situation: After calling expansion method, a node is created at the specified index
        deck = Deck()
        card = deck.draw_card()
        parent_state = State(deck, [Card(Suit.HEARTS, Rank.KING), Card(Suit.CLUBS, Rank.SEVEN), Card(Suit.HEARTS, Rank.SEVEN)], [0, 0, 0, 0], 0)
        parent_hand = [card]
        parent_node = self.player.Node(parent_state, parent_hand, None)
        child_num = 0
        selected_node = self.player.expansion(parent_node, child_num)
        self.assertIsNotNone(selected_node)
        self.assertEqual(selected_node.parent, parent_node)
        self.assertIsInstance(parent_node.children[child_num], self.player.Node)
        self.assertEqual(len(selected_node.current_hand), len(parent_hand) - 1)

    def test_best_child_uct(self):
        # Situation: Create a node with children, set their rewards and visits, 
        # and verify that the node with the highest UCT value is returned
        parent_state = State([], [], [], 0)
        parent_hand = [1, 2, 3]
        parent_node = self.player.Node(parent_state, parent_hand, None)
        
        rewards = [10, 20, 15]
        visits = [5, 10, 8]
        children = []
        for i in range(len(rewards)):
            child_state = deepcopy(parent_state)
            child_hand = parent_hand[:]
            child_node = self.player.Node(child_state, child_hand, parent_node)
            child_node.best_reward = rewards[i]
            child_node.nb_visits = visits[i]
            children.append(child_node)
        parent_node.children = children
        
        total_visits = sum(visits)
        expected_best_index = max(range(len(rewards)), key=lambda i: (rewards[i] / visits[i]) + 1.4 * (2 * (total_visits ** 0.5) / visits[i]) ** 0.5)
        
        best_child = self.player.best_child_uct(parent_node, 1.4)
        
        self.assertEqual(best_child, parent_node.children[expected_best_index])

    def test_back_prop(self):        
        root_node = self.player.Node(state=None, hand=[], parent=None)
        child_node1 = self.player.Node(state=None, hand=[], parent=root_node)
        child_node2 = self.player.Node(state=None, hand=[], parent=root_node)
        grandchild_node1 = self.player.Node(state=None, hand=[], parent=child_node1)
        grandchild_node2 = self.player.Node(state=None, hand=[], parent=child_node1)
        
        root_node.nb_visits = 1
        root_node.best_reward = 0
        child_node1.nb_visits = 2
        child_node1.best_reward = 2
        child_node2.nb_visits = 1
        child_node2.best_reward = 1
        grandchild_node1.nb_visits = 1
        grandchild_node1.best_reward = 1
        grandchild_node2.nb_visits = 1
        grandchild_node2.best_reward = 0
        
        self.player.back_prop(grandchild_node1, 1)
        
        self.assertEqual(root_node.nb_visits, 2)
        self.assertEqual(root_node.best_reward, 1)
        self.assertEqual(child_node1.nb_visits, 3)
        self.assertEqual(child_node1.best_reward, 3)
        self.assertEqual(child_node2.nb_visits, 1)
        self.assertEqual(child_node2.best_reward, 1)
        self.assertEqual(grandchild_node1.nb_visits, 2)
        self.assertEqual(grandchild_node1.best_reward, 2)
        self.assertEqual(grandchild_node2.nb_visits, 1)
        self.assertEqual(grandchild_node2.best_reward, 0)

    def test_best_reward_child(self):
        root_node = self.player.Node(state=None, hand=[], parent=None)
        
        child_node1 = self.player.Node(state=None, hand=[], parent=root_node)
        child_node2 = self.player.Node(state=None, hand=[], parent=root_node)
        child_node3 = self.player.Node(state=None, hand=[], parent=root_node)
        
        child_node1.best_reward = 5
        child_node2.best_reward = 10
        child_node3.best_reward = 3
        
        root_node.children = [child_node1, child_node2, child_node3]
        
        best_child_index = self.player.best_reward_child(root_node)
        
        self.assertEqual(best_child_index, 1)  # Child node 2 has the highest reward

if __name__ == '__main__':
    unittest.main()
