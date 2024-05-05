from Player import RandomPlayer
from manche import Manche
import torch

SCORE_PERDANT = -199


class partie:
    def __init__(self, joueurs):
        self.joueurs = joueurs

    def match_fini(self):
        for joueur in self.joueurs:
            if joueur.getScore() < SCORE_PERDANT:
                print(str(joueur.getScore()) +"" + joueur.get_name())
                return True

    def jouer_partie(self):
        match_fini = False
        compt = 0
        while True:
            print(f"manche n{compt}")
            compt += 1
            Manche(self.joueurs).play_to_update_random_dataset()
            match_fini = self.match_fini()
            if match_fini:
                break
        ranked_players_list = self.rank_players(self.joueurs)
        ranked_players_list[0].set_dataset_score(3)
        ranked_players_list[0].print_dataset()


    def rank_players(self,players):
        # Sort players based on their scores in descending order
        ranked_players = sorted(players, key=lambda player: player.getScore(), reverse=True)
        return ranked_players

    def print_rank(self):
        ranked_players_list = self.rank_players(self.joueurs)

        # Print the ranked players
        for i, player in enumerate(ranked_players_list, start=1):
            print(f"Rank {i}: {player.name} - Score: {player.getScore()}")

    def jouer_une_manche(self):
        Manche(self.joueurs).play_to_update_random_dataset()

if __name__ == '__main__':
    partie = partie([RandomPlayer("pedro"), RandomPlayer("pedrito"), RandomPlayer("pedri"), RandomPlayer("pedru")])
    partie.jouer_partie()
    partie.print_rank()
