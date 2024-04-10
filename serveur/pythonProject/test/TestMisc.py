import random
import unittest
from src.manche import Manche
from src.Player import RandomPlayer
from src.paquet import Paquet, Carte, Couleur, Rang
from src.pli import Pli


class TestManche(unittest.TestCase):
    def test_gagnant_pli(self):
        # Create players
        players = [RandomPlayer("Player 1"), RandomPlayer("Player 2"), RandomPlayer("Player 3"),
                   RandomPlayer("Player 4")]

        # Initialize a Manche
        manche = Manche(players)
        manche.ouvreur = 3

        # Initialize a pli
        pli = Pli(players, 3, None, 0)
        pli.cartes_du_pli = [
            Carte(Couleur.PIQUES, Rang.DAME),
            Carte(Couleur.PIQUES, Rang.ROI),
            Carte(Couleur.COEURS, Rang.AS),
            Carte(Couleur.PIQUES, Rang.AS)
        ]
        pli.couleur = Couleur.PIQUES

        # Call the method being tested
        winner = manche.gagnant_pli(pli)

        # Assert the winner
        print(winner)


if __name__ == '__main__':
    unittest.main()
