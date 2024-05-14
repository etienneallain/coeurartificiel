class Player:
    def __init__(self):
        self.cards_left = ['A', 'B', 'C']  # Example attribute


class NNPlayer(Player):
    def __init__(self):
        super().__init__()

    def play_card(self):
        print(self.cards_left)  # Accessing the inherited attribute


if __name__ == '__main__':
    nn_player = NNPlayer()
    nn_player.play_card()
