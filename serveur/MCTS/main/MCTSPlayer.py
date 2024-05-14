from copy import deepcopy
import random
import time
from Player import Player

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