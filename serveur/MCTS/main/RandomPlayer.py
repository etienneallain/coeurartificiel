import random
from Player import Player

class RandomPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.rng = random.Random()
        print(f"Random Player ({name}) initialized.")

    def do_action(self, state):
        first_suit = self.first_suit(state.current_trick)

        if first_suit is None:
            index = self.rng.randint(0, len(self.hand) - 1)
            return self.hand.pop(index)

        range_start, range_end = self.get_suit_range(first_suit, self.hand)

        if range_end - range_start == 0:
            return self.hand.pop(self.rng.randint(0, len(self.hand) - 1))
        
        index = self.rng.randint(0, range_end - range_start - 1)
        return self.hand.pop(range_start + index)