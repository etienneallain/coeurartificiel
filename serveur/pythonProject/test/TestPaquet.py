import unittest
from unittest.mock import patch
from src.paquet import Paquet,Carte,Couleur,Rang

class TestPaquetMethods(unittest.TestCase):
    def setUp(self):
        self.paquet = Paquet()

    def test_remove_card_found(self):
        # Test when removing a card that exists in the paquet
        test_card = Carte(Couleur.COEURS, Rang.SEPT)
        self.paquet.cartes = [test_card, Carte(Couleur.CARREAUX, Rang.AS), Carte(Couleur.TREFLES, Rang.VALET)]

        with patch('builtins.print') as mock_print:
            removed_card = self.paquet.remove_card(test_card)

        self.assertEqual(removed_card, test_card)
        self.assertNotIn(test_card, self.paquet.cartes)
        mock_print.assert_not_called()

    def test_remove_card_not_found(self):
        # Test when removing a card that does not exist in the paquet
        test_card = Carte(Couleur.PIQUES, Rang.DAME)
        self.paquet.cartes = [Carte(Couleur.TREFLES, Rang.NEUF), Carte(Couleur.CARREAUX, Rang.ROI)]

        with patch('builtins.print') as mock_print:
            removed_card = self.paquet.remove_card(test_card)

        self.assertIsNone(removed_card)
        mock_print.assert_called_once_with("Card not found in the paquet.")

    def test_remove_cards_found(self):
        test_cards = [
            Carte(Couleur.COEURS, Rang.SEPT),
            Carte(Couleur.CARREAUX, Rang.AS),
            Carte(Couleur.TREFLES, Rang.VALET)
        ]

        self.paquet.cartes = test_cards + [Carte(Couleur.PIQUES, Rang.DAME)]

        with patch('builtins.print') as mock_print:
            removed_cards = self.paquet.remove_cards(test_cards)

        self.assertEqual(removed_cards, test_cards)
        for card in test_cards:
            self.assertNotIn(card, self.paquet.cartes)
        mock_print.assert_not_called()

if __name__ == '__main__':
    unittest.main()
