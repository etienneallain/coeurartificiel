from Deck import Deck
from Game import Game
from RandomPlayer import RandomPlayer
from MCTSPlayer import MCTSPlayer

if __name__ == "__main__":
    deck = Deck()
    deck.print_deck()

    p1 = RandomPlayer("RNG1")
    p2 = RandomPlayer("RNG2")
    p3 = RandomPlayer("RNG3")
    p4 = MCTSPlayer("MCTS")

    # Play Multiple Games
    number_of_games = 5000
    total_scores = [0] * 4
    game = Game(deck, p1, p2, p3, p4)
    for i in range(1, number_of_games + 1):
        print("\n--------------------------------------------")
        print("--------------------------------------------")
        print("--------------------------------------------")
        print("Playing Game #", i)
        print("--------------------------------------------")
        print("--------------------------------------------")
        print("--------------------------------------------\n")
        game.play_new_game()
        for j, player in enumerate([p1, p2, p3, p4]):
            total_scores[j] = player.get_points()

    print("\n--------------------------------------------")
    print("--------------------------------------------")
    print("Total Scores:")
    print("--------------------------------------------")
    for i, player in enumerate(["RNG1", "RNG2", "RNG3", "MCTS"]):
        print(player, ":", total_scores[i])

    print("\n--------------------------------------------")
    print("--------------------------------------------")
    print("Average Scores:")
    print("--------------------------------------------")
    average_scores = [total_score / number_of_games for total_score in total_scores]
    for i, player in enumerate(["RNG1", "RNG2", "RNG3", "MCTS"]):
        print(player, ":", average_scores[i])