import io
import sys
import unittest
from main.Card import Rank, Suit, Card
from main.Deck import Deck
from main.Game import Game
from main.RandomPlayer import RandomPlayer
from main.State import State

class TestGame(unittest.TestCase):
    def test_init_game(self):
        # Create a game with a deck and players
        deck = Deck()
        p1 = RandomPlayer("Player 1")
        p2 = RandomPlayer("Player 2")
        p3 = RandomPlayer("Player 3")
        p4 = RandomPlayer("Player 4")
        game = Game(deck, p1, p2, p3, p4)
        
        game.init_game()
        
        # Vérifie que chaque joueur a bien 8 cartes dans sa main
        for player in game.players_turn:
            self.assertEqual(len(player.hand), 8)
        
        # Vérifie que chaque main soit triée
        for player in game.players_turn:
            self.assertTrue(all(player.hand[i] < player.hand[i+1] for i in range(len(player.hand)-1)))
        
        # Vérifie que le premier joueur est bien celui attendu
        self.assertEqual(game.players_turn[game.first_player], p1)
    
    def test_play_new_game(self):
        deck = Deck()
        p1 = RandomPlayer("Player 1")
        p2 = RandomPlayer("Player 2")
        p3 = RandomPlayer("Player 3")
        p4 = RandomPlayer("Player 4")
        game = Game(deck, p1, p2, p3, p4)
        
        game.play_new_game()
        
        # Vérifier que les points ont été mis à jour correctement
        total_points = sum(game.points)
        self.assertTrue(total_points == -40 or total_points == 40)  # Vérifie si la somme est égale à -40 ou 40
        
        # Vérifier que les points ne sont plus tous égaux à zéro
        self.assertFalse(all(points == 0 for points in game.points))  # Vérifie si tous les points ne sont pas égaux à zéro
        
    def test_check_trick(self):
        game = Game(Deck(), RandomPlayer("Player 1"), RandomPlayer("Player 2"), RandomPlayer("Player 3"), RandomPlayer("Player 4"))
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
            
            # Assertion pour vérifier que la carte ajoutée au pli est valide
            self.assertTrue(game.check_trick(played_card, index), f"La carte {played_card} ajoutée au pli n'est pas valide.")

    def test_check_trick2(self):
        game = Game(Deck(), RandomPlayer("Player 1"), RandomPlayer("Player 2"), RandomPlayer("Player 3"), RandomPlayer("Player 4"))
        game.init_game()
        
        for player_num in range(len(game.players_turn)):
            index = (game.first_player + player_num) % len(game.players_turn)
            current_player = game.players_turn[index]
            game_copy = State(game.played_cards, game.current_trick, game.points, index)
            
            played_card = current_player.do_action(game_copy)

            valid_move = game.check_trick(played_card, index)
            
            self.assertTrue(valid_move, f"La carte jouée {played_card} par {current_player.get_name()} n'est pas valide.")
            
            game.current_trick.append(played_card)
            game.played_cards.add_card(played_card)

    def test_calculate_points(self):
        game = Game(Deck(), RandomPlayer("Player 1"), RandomPlayer("Player 2"), RandomPlayer("Player 3"), RandomPlayer("Player 4"))
        game.current_trick = [Card(Suit.HEARTS, Rank.ACE), Card(Suit.HEARTS, Rank.KING), Card(Suit.SPADES, Rank.JACK), Card(Suit.CLUBS, Rank.TEN)]
        points = game.calculate_points()
        self.assertEqual(points, -10)
        
    def test_print_points(self):
        deck = Deck()
        p1 = RandomPlayer("Player 1")
        p2 = RandomPlayer("Player 2")
        p3 = RandomPlayer("Player 3")
        p4 = RandomPlayer("Player 4")
        game = Game(deck, p1, p2, p3, p4)
        game.points = [-10, -5, -25, 0]
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        game.print_points()
        
        sys.stdout = sys.__stdout__
        
        expected_output = "Points received this game:\n--------------------------\nPlayer 1 has -10 points.\nPlayer 2 has -5 points.\nPlayer 3 has -25 points.\nPlayer 4 has 0 points.\n\n"
        self.assertEqual(captured_output.getvalue(), expected_output)
        
    def test_print_winner(self):
        deck = Deck()
        p1 = RandomPlayer("Player 1")
        p2 = RandomPlayer("Player 2")
        p3 = RandomPlayer("Player 3")
        p4 = RandomPlayer("Player 4")
        game = Game(deck, p1, p2, p3, p4)
        p1.points = 10
        p2.points = -5
        p3.points = 20
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        game.print_winner()
        
        sys.stdout = sys.__stdout__
        
        expected_output = "Player 3 is in the lead after this game.\n\n"
        self.assertEqual(captured_output.getvalue(), expected_output)
        
    def test_print_total_points(self):
        deck = Deck()
        p1 = RandomPlayer("Player 1")
        p2 = RandomPlayer("Player 2")
        p3 = RandomPlayer("Player 3")
        p4 = RandomPlayer("Player 4")
        game = Game(deck, p1, p2, p3, p4)
        p1.points = 100
        p2.points = -50
        p3.points = 200

        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        game.print_total_points()
        
        sys.stdout = sys.__stdout__
        
        expected_output = "Total cumulative points between all games:\n--------------------------\nPlayer 1 has 100 points.\nPlayer 2 has -50 points.\nPlayer 3 has 200 points.\nPlayer 4 has 0 points.\n\n"
        self.assertEqual(captured_output.getvalue(), expected_output)

if __name__ == "__main__":
    unittest.main()
