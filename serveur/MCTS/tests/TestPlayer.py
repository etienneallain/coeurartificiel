import unittest
from main.Card import Card, Rank, Suit
from main.Deck import Deck
from main.Game import Game
from main.RandomPlayer import RandomPlayer
from main.State import State

class TestPlayer(unittest.TestCase):

    def test_add_to_hand(self):
        player = RandomPlayer("Test Player")
        player.add_to_hand(Card(Suit.SPADES, Rank.ACE))
        self.assertEqual(len(player.hand), 1, "La carte n'a pas été ajoutée à la main du joueur")

    def test_sort_hand(self):
        player = RandomPlayer("Test Player")
        player.add_to_hand(Card(Suit.HEARTS, Rank.ACE))
        player.add_to_hand(Card(Suit.SPADES, Rank.KING))
        player.add_to_hand(Card(Suit.DIAMONDS, Rank.QUEEN))
        player.sort_hand()
        self.assertEqual(player.hand, [Card(Suit.DIAMONDS, Rank.QUEEN), Card(Suit.HEARTS, Rank.ACE), Card(Suit.SPADES, Rank.KING)], "La main du joueur n'est pas correctement triée")

    def test_clear_hand(self):
        player = RandomPlayer("Test Player")
        player.add_to_hand(Card(Suit.HEARTS, Rank.ACE))
        player.clear_hand()
        self.assertEqual(len(player.hand), 0, "La main du joueur n'a pas été correctement vidée")

    def test_has_suit(self):
        player = RandomPlayer("Test Player")
        player.add_to_hand(Card(Suit.HEARTS, Rank.ACE))
        self.assertTrue(player.has_suit(Suit.HEARTS), "La méthode a_suit a renvoyé False alors que le joueur possède une carte de couleur coeur")
        self.assertFalse(player.has_suit(Suit.SPADES), "La méthode a_suit a renvoyé True alors que le joueur ne possède pas de carte de couleur pique")

    def test_first_suit(self):
        player = RandomPlayer("Test Player")
        trick = [Card(Suit.HEARTS, Rank.ACE), Card(Suit.SPADES, Rank.KING)]
        self.assertEqual(player.first_suit(trick), Suit.HEARTS, "La méthode first_suit n'a pas retourné la couleur attendue")

    def test_get_suit_range(self):
        player = RandomPlayer("Test Player")
        hand = [Card(Suit.HEARTS, Rank.ACE), Card(Suit.HEARTS, Rank.KING), Card(Suit.SPADES, Rank.QUEEN)]
        start, end = player.get_suit_range(Suit.HEARTS, hand)
        self.assertEqual((start, end), (0, 2), "Les indices de début et de fin de la couleur coeur ne sont pas corrects")

    def test_get_name(self):
        player = RandomPlayer("Test Player")
        self.assertEqual(player.get_name(), "Test Player", "Le nom du joueur retourné n'est pas correct")

    def test_add_points(self):
        player = RandomPlayer("Test Player")
        player.add_points(10)
        self.assertEqual(player.get_points(), 10, "Les points n'ont pas été correctement ajoutés au joueur")

    def test_get_moons(self):
        player = RandomPlayer("Test Player")
        self.assertEqual(player.get_moons(), 0, "Le nombre de lunes du joueur retourné n'est pas correct")
        player.moons = 2
        self.assertEqual(player.get_moons(), 2, "Le nombre de lunes du joueur retourné n'est pas correct")

    def test_clear_player(self):
        player = RandomPlayer("Test Player")
        player.add_to_hand(Card(Suit.HEARTS, Rank.ACE))
        player.add_points(10)
        player.clear_player()
        self.assertEqual(len(player.hand), 0, "La main du joueur n'a pas été correctement vidée lors de la réinitialisation")
        self.assertEqual(player.get_points(), 0, "Les points du joueur n'ont pas été correctement réinitialisés")
        self.assertEqual(player.get_moons(), 0, "Le nombre de lunes du joueur n'a pas été correctement réinitialisé")

    def test_integration_with_game(self):
        player_rng = RandomPlayer("Test Player")
        game = Game(Deck(), player_rng, RandomPlayer("Player 2"), RandomPlayer("Player 3"), RandomPlayer("Player 4"))
        game.init_game()
        
        for player_num in range(len(game.players_turn)):
            index = (game.first_player + player_num) % len(game.players_turn)
            current_player = game.players_turn[index]
            game_copy = State(game.played_cards, game.current_trick, game.points, index)
            played_card = current_player.do_action(game_copy)

            while not game.check_trick(played_card, index):
                current_player.add_to_hand(played_card)
                current_player.sort_hand()
                played_card = current_player.do_action(game_copy)

            game.current_trick.append(played_card)
            game.played_cards.add_card(played_card)
            
            self.assertTrue(len(player_rng.hand) < 8, f"Le joueur {player_rng} n'a pas réussi à jouer dans la partie.")

if __name__ == '__main__':
    unittest.main()
