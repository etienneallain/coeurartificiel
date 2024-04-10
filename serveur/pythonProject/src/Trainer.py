import torch
from torch.utils.data import DataLoader
import numpy as np

from src.Player import RandomPlayer, NNPlayer
from src.manche import Manche


class Trainer:
    def __init__(self, model, dataset, batch_size=64, learning_rate=0.001, num_epochs=100):
        self.model = model
        self.dataset = dataset
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.num_epochs = num_epochs

    def train(self):
        dataloader = DataLoader(self.dataset, batch_size=self.batch_size, shuffle=True)
        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.learning_rate)
        losses = []

        for epoch in range(self.num_epochs):
            epoch_losses = []
            for inputs, targets in dataloader:
                outputs = self.model(inputs)
                from src.NeuralNetwork import squared_error_masked
                loss = squared_error_masked(targets, outputs)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                epoch_losses.append(loss.item())

            epoch_loss = np.mean(epoch_losses)
            losses.append(epoch_loss)
            print(f'Epoch [{epoch + 1}/{self.num_epochs}], Loss: {epoch_loss:.4f}')

        return losses


def test_model(model, num_manches):
    player_scores = {player.get_name(): 0 for player in
                     [RandomPlayer("pedro"), NNPlayer("Monster", model), RandomPlayer("pedrito"), RandomPlayer("pedri"),
                      ]}

    for i in range(num_manches):
        manche = Manche(
            [RandomPlayer("pedro"), RandomPlayer("pedrito"), RandomPlayer("pedri"), NNPlayer("Monster", model)],
        )
        manche.play_with_NN()

        # Update player scores
        for player in manche.joueurs:
            player_scores[player.get_name()] += player.getScore()

    # Calculate average scores
    total_players = len(player_scores)
    average_scores = {player: score / num_manches for player, score in player_scores.items()}

    # Print average scores
    print("Average scores:")
    for player, average_score in average_scores.items():
        print(f"{player}: {average_score}")


def test_model_NNs(model1, model2, num_manches):
    player_scores = {player.get_name(): 0 for player in
                     [NNPlayer("pedro1", model1), NNPlayer("pedrito1a", model1), NNPlayer("pedrito1b", model2),
                      NNPlayer("pedro1c", model2)]}

    for i in range(num_manches):
        manche = Manche(
            [NNPlayer("pedro1", model1), NNPlayer("pedrito1a", model1), NNPlayer("pedrito1b", model2),
             NNPlayer("pedro1c", model2)]
        )
        manche.play_with_NN()

        # Update player scores
        for player in manche.joueurs:
            player_scores[player.get_name()] += player.getScore()

    # Calculate average scores
    total_players = len(player_scores)
    average_scores = {player: score / num_manches for player, score in player_scores.items()}

    # Print average scores
    print("Average scores:")
    for player, average_score in average_scores.items():
        print(f"{player}: {average_score}")
