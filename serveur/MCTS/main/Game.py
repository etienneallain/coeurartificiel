from Card import Suit
from State import State

class Game:
    def __init__(self, deck, p1, p2, p3, p4):
        self.players_turn = [p1, p2, p3, p4]
        self.first_player = 0
        self.played_cards = deck
        self.current_trick = []
        self.points = [0, 0, 0, 0]

    def init_game(self):
        self.played_cards.shuffle_deck()
        for player in self.players_turn:
            player.clear_hand()
        for _ in range(8):
            for player in self.players_turn:
                player.add_to_hand(self.played_cards.draw_card())
        for player in self.players_turn:
            player.sort_hand()
            player.print_hand()
        print("\n")
        print(self.players_turn[self.first_player].get_name(), "will play first.\n")
        self.current_trick.clear()
        self.points = [0, 0, 0, 0]

    def print_trick(self, first_player):
        print("\nCards played this round:")
        print("------------------------")
        if not self.current_trick:
            print("No cards have been played this round.")
        for i, card in enumerate(self.current_trick):
            index = (i + first_player) % len(self.players_turn)
            print(f"{self.players_turn[index].get_name():15s} played {card.print_card_short():3s}")

    def check_trick(self, played_card, index):
        if not self.current_trick:
            return True
        first_suit = self.current_trick[0].get_suit()
        if self.players_turn[index].has_suit(first_suit) and played_card.get_suit() != first_suit:
            print(f"You still have a card that is {first_suit}. You must play that first.")
            return False
        return True

    def next_opener(self, first_player):
        first_suit = self.current_trick[0].get_suit()
        largest_rank = self.current_trick[0].get_rank()
        opener = first_player
        for i in range(len(self.players_turn)):
            index = (first_player + i) % len(self.players_turn)
            if self.current_trick[i].get_suit() == first_suit:
                if self.current_trick[i].get_rank().value > largest_rank.value:
                    opener = index
                    largest_rank = self.current_trick[i].get_rank()
        return opener % len(self.players_turn)

    def calculate_points(self):
        pts = 0
        for card in self.current_trick:
            if card.get_suit() == Suit.HEARTS:
                pts -= 5
        return pts

    def print_points(self):
        print("Points received this game:")
        print("--------------------------")

        for player, point in zip(self.players_turn, self.points):
            print(f"{player.get_name()} has {point} points.")
        print()

    def print_winner(self):
        largest_score = self.players_turn[0].get_points()
        index = 0
        for i, player in enumerate(self.players_turn):
            if largest_score < player.get_points():
                index = i
                largest_score = player.get_points()
        print(f"{self.players_turn[index].get_name()} is in the lead after this game.\n")

    def print_total_points(self):
        print("Total cumulative points between all games:")
        print("--------------------------")
        for player in self.players_turn:
            print(f"{player.get_name()} has {player.get_points()} points.")
        print()

    def print_total_moon(self):
        print("Total cumulative moons between all games:")
        print("--------------------------")
        for player in self.players_turn:
            print(f"{player.get_name()} has {player.get_moons()} moons.")
        print()

    def play_new_game(self):
        self.init_game()
        
        for trick_num in range(1, 9):
            print("--------------------------------------------")
            print("Trick #{}:".format(trick_num))
            print("--------------------------------------------")
            self.current_trick.clear()

            for player_num in range(len(self.players_turn)):
                index = (self.first_player + player_num) % len(self.players_turn)
                current_player = self.players_turn[index]
                game_copy = State(self.played_cards, self.current_trick, self.points, index)
                played_card = current_player.do_action(game_copy)

                while not self.check_trick(played_card, index):
                    print("This was an invalid play. Please pick a valid card.")
                    current_player.add_to_hand(played_card)
                    current_player.sort_hand()
                    played_card = current_player.do_action(game_copy)

                print("{} played {}.".format(current_player.get_name(), played_card.print_card_short()))

                self.current_trick.append(played_card)
                self.played_cards.add_card(played_card)

            print("--------------------------------------------")
            print("Trick {} Summary:".format(trick_num))
            print("--------------------------------------------")
            self.print_trick(self.first_player)

            self.first_player = self.next_opener(self.first_player)
            pts = self.calculate_points()
            self.points[self.first_player] += pts
            self.players_turn[self.first_player].add_points(pts)
            
            print("\n{} played the highest card and took {} points this round.\n".format(
                self.players_turn[self.first_player].get_name(), pts))
            
            for i, player in enumerate(self.players_turn):
                if self.points[i] == -40:
                    self.points[i] = 40
                    self.players_turn[i].add_points(80)

            self.print_points()

        print("------------------------------------------")
        print("Game Summary:")
        print("------------------------------------------\n")
        
        self.print_points()

        for i, pts in enumerate(self.points):
            if self.points[i] == 40:
                self.players_turn[i].moons += 1
        
        self.print_winner()
        self.print_total_points()
        self.print_total_moon()