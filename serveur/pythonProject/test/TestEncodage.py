import unittest
from src.JoueurEncoder import JoueurEncoder
from src.paquet import (Carte, Couleur, Rang)


class TestJoueurEncoder(unittest.TestCase):
    def setUp(self):
        self.joueur_encoder = JoueurEncoder()

    def test_encode_cards(self):
        cards = [
            Carte(Couleur.COEURS, Rang.SEPT),
            Carte(Couleur.CARREAUX, Rang.AS),
            Carte(Couleur.PIQUES, Rang.DAME)
            # Add more cards or None values as needed
        ]

        encoded_hand = self.joueur_encoder.encode_cards(cards)

        self.assertEqual(len(encoded_hand), 4 * 8)
        # 7 coeurs
        self.assertEqual(encoded_hand[0], 1)
        # As careraux
        self.assertEqual(encoded_hand[15], 1)
        # Dame piques
        self.assertEqual(encoded_hand[29], 1)
        # autres cartes
        self.assertEqual(encoded_hand[1], -1)
        self.assertEqual(encoded_hand[20], -1)

    def test_encode_card(self):
        card = Carte(Couleur.PIQUES, Rang.DAME)

        encoded_hand = self.joueur_encoder.encode_card(card)

        self.assertEqual(len(encoded_hand), 4 * 8)
        self.assertEqual(encoded_hand[29], 1)

    def test_encode_numero_pli(self):
        numero_pli = 3

        encoded_numero_pli = self.joueur_encoder.encode_numero_pli(numero_pli)
        self.assertEqual(len(encoded_numero_pli), 8)
        self.assertEqual(encoded_numero_pli[3], 1)

    def test_encode_ordre_joueur(self):
        ordre_joueur = 2

        encoded_ordre_joueur = self.joueur_encoder.encode_ordre_joueur(ordre_joueur)
        print(encoded_ordre_joueur)
        self.assertEqual(len(encoded_ordre_joueur), 4)
        self.assertEqual(encoded_ordre_joueur[2], 1)

    def test_encode_couleur(self):
        couleur = Couleur.PIQUES
        encoded_couleur = self.joueur_encoder.encode_couleur(couleur)
        self.assertEqual(encoded_couleur[3], 1)


if __name__ == '__main__':
    unittest.main()
