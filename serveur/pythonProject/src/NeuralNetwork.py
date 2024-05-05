import os
import pickle

import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
import matplotlib.pyplot as plt

from JoueurEncoder import JoueurEncoder
from Trainer import Trainer, test_model, test_model_NNs
from data import Data
from Player import RandomPlayer, NNPlayer
from manche import Manche
from paquet import Paquet


class CustomDataset(Dataset):
    def __init__(self, data):
        self.inputs = [torch.tensor(item[0]).clone().detach().float() for item in data]
        self.outputs = [torch.tensor(item[1]).clone().detach().float() for item in data]

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        return self.inputs[idx], self.outputs[idx]


# class NeuralNetwork(torch.nn.Module):
#     def __init__(self, input_size, output_size):
#         super(NeuralNetwork, self).__init__()
#         self.fc1 = torch.nn.Linear(input_size, 64)
#         self.fc2 = torch.nn.Linear(64, 64)
#         self.fc3 = torch.nn.Linear(64, output_size)
#
#         self.activation = torch.nn.ELU()
#
#         self.tanh = torch.nn.Tanh()
#
#     def forward(self, x):
#         x = self.activation(self.fc1(x))
#         x = self.activation(self.fc2(x))
#         x = self.fc3(x)
#         return x

class NeuralNetwork(torch.nn.Module):
    def __init__(self, input_size, output_size):
        super(NeuralNetwork, self).__init__()
        self.input_size = input_size
        self.output_size = output_size

        # Define the layers based on the provided structure
        self.fc1 = torch.nn.Linear(input_size, 384)
        self.fc2 = torch.nn.Linear(384, 384)
        self.fc3 = torch.nn.Linear(384, 256)
        self.fc4 = torch.nn.Linear(256, 128)
        self.fc5 = torch.nn.Linear(128, 32)

        self.activation = torch.nn.ELU()

        self.tanh = torch.nn.Tanh()

    def forward(self, x):
        # Pass through the layers
        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        x = self.activation(self.fc3(x))
        x = self.activation(self.fc4(x))
        x = self.tanh(self.fc5(x))

        return x

class NeuralNetwork2(torch.nn.Module):
    def __init__(self, input_size, output_size):
        super(NeuralNetwork2, self).__init__()
        self.input_size = input_size
        self.output_size = output_size

        # Define the layers based on the provided structure
        self.fc1 = torch.nn.Linear(input_size, 384)
        self.fc2 = torch.nn.Linear(384, 384)
        self.fc3 = torch.nn.Linear(384, 256)
        self.fc4 = torch.nn.Linear(256, 128)
        self.fc5 = torch.nn.Linear(128, 32)

        self.activation = torch.nn.LeakyReLU()

        self.tanh = torch.nn.Tanh()

    def forward(self, x):
        # Pass through the layers
        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        x = self.activation(self.fc3(x))
        x = self.activation(self.fc4(x))
        x = self.tanh(self.fc5(x))

        return x


def load_dataset_from_file(dataset_filename):
    """Load dataset from a .pkl file."""
    with open(dataset_filename, 'rb') as file:
        dataset = pickle.load(file)
    return dataset


def train_model_with_dataset(dataset_filename, model, input_size, output_size, learning_rate, batch_size, num_epochs):
    """Train a neural network model using a dataset loaded from a .pkl file."""
    # Load dataset from file
    dataset = load_dataset_from_file(dataset_filename)

    # Create an instance of the Trainer class
    trainer = Trainer(model, dataset, batch_size=batch_size, learning_rate=learning_rate, num_epochs=num_epochs)

    # Train the model using the Trainer instance
    losses = trainer.train()

    # Return the losses
    return losses


def squared_error_masked(y_true, y_pred, scale_factor=1.0):
    """ Squared error of elements where y_true is not 0 """
    mask = y_true != 0
    err = y_pred - (y_true * scale_factor)
    masked_err = err[mask]
    return torch.sum(masked_err ** 2)


def train_model(model, dataloader, optimizer, num_epochs):
    losses = []
    for epoch in range(num_epochs):
        epoch_losses = []
        for inputs, targets in dataloader:
            outputs = model(inputs)
            loss = squared_error_masked(targets, outputs)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            epoch_losses.append(loss.item())
        epoch_loss = np.mean(epoch_losses)
        losses.append(epoch_loss)
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {epoch_loss:.4f}')
    return losses


def save_model(model, filepath):
    torch.save(model.state_dict(), filepath)


def load_model(input_size, output_size, filepath):
    model = NeuralNetwork(input_size, output_size)
    model.load_state_dict(torch.load(filepath))
    return model

#
if __name__ == '__main__':
    initial_model = NeuralNetwork(113, 32)
    initial_model.load_state_dict(torch.load("good_nns/good_boy_3b.pth"))
    initial_model.train()

    new_dataset = CustomDataset(Data().generate_NN_data(50000, initial_model))
    trainer = Trainer(initial_model, new_dataset, batch_size=32, learning_rate=0.001, num_epochs=10)
    losses = trainer.train()

    torch.save(initial_model.state_dict(), "amazing_boy_3a.pth")

    initial_model = NeuralNetwork(113, 32)
    initial_model.load_state_dict(torch.load("good_nns/good_boy_3b.pth"))
    initial_model.train()

    new_dataset = CustomDataset(Data().generate_NN_data(25000, initial_model))
    trainer = Trainer(initial_model, new_dataset, batch_size=32, learning_rate=0.001, num_epochs=10)
    losses = trainer.train()

    torch.save(initial_model.state_dict(), "amazing_boy_3b.pth")

    initial_model = NeuralNetwork(113, 32)
    initial_model.load_state_dict(torch.load("good_nns/heeeelnaaw3.pth"))
    initial_model.train()

    new_dataset = CustomDataset(Data().generate_NN_data(25000, initial_model))
    trainer = Trainer(initial_model, new_dataset, batch_size=32, learning_rate=0.001, num_epochs=10)
    losses = trainer.train()

    torch.save(initial_model.state_dict(), "bad_boy_3a.pth")

    initial_model = NeuralNetwork(113, 32)
    initial_model.load_state_dict(torch.load("good_nns/heeeelnaaw3.pth"))
    initial_model.train()

    new_dataset = CustomDataset(Data().generate_NN_data(1000, initial_model))
    trainer = Trainer(initial_model, new_dataset, batch_size=32, learning_rate=0.001, num_epochs=10)
    losses = trainer.train()

    torch.save(initial_model.state_dict(), "bad_boy_3c.pth")

    initial_model = NeuralNetwork(113, 32)
    initial_model.load_state_dict(torch.load("good_nns/heeeelnaaw3.pth"))
    initial_model.train()

    new_dataset = CustomDataset(Data().generate_NN_data(1000, initial_model))
    trainer = Trainer(initial_model, new_dataset, batch_size=32, learning_rate=0.001, num_epochs=10)
    losses = trainer.train()

    torch.save(initial_model.state_dict(), "bad_boy_3d.pth")

    initial_model = NeuralNetwork(113, 32)
    initial_model.load_state_dict(torch.load("good_nns/heeeelnaaw3.pth"))
    initial_model.train()

    new_dataset = CustomDataset(Data().generate_NN_data(1000, initial_model))
    trainer = Trainer(initial_model, new_dataset, batch_size=32, learning_rate=0.001, num_epochs=10)
    losses = trainer.train()

    torch.save(initial_model.state_dict(), "bad_boy_3e.pth")

    initial_model = NeuralNetwork(113, 32)
    initial_model.load_state_dict(torch.load("good_nns/heeeelnaaw3.pth"))
    initial_model.train()

    new_dataset = CustomDataset(Data().generate_NN_data(1000, initial_model))
    trainer = Trainer(initial_model, new_dataset, batch_size=32, learning_rate=0.001, num_epochs=10)
    losses = trainer.train()

    torch.save(initial_model.state_dict(), "bad_boy_3f.pth")

    initial_model = NeuralNetwork(113, 32)
    initial_model.load_state_dict(torch.load("good_nns/heeeelnaaw3.pth"))
    initial_model.train()

    new_dataset = CustomDataset(Data().generate_NN_data(1000, initial_model))
    trainer = Trainer(initial_model, new_dataset, batch_size=32, learning_rate=0.001, num_epochs=10)
    losses = trainer.train()

    torch.save(initial_model.state_dict(), "good_nns/bad_boy_3g.pth")

    initial_model = NeuralNetwork(113, 32)
    initial_model.load_state_dict(torch.load("good_nns/heeeelnaaw3.pth"))
    initial_model.train()

    new_dataset = CustomDataset(Data().generate_NN_data(1000, initial_model))
    trainer = Trainer(initial_model, new_dataset, batch_size=32, learning_rate=0.001, num_epochs=10)
    losses = trainer.train()

    torch.save(initial_model.state_dict(), "bad_boy_3h.pth")





# if __name__ == '__main__':
#
#     dataset = Data()
#     dataset = CustomDataset(dataset.generate_random_player_data(10000))
#
#     # PARAMETRES #
#     input_size = 113
#     output_size = 32
#     learning_rate = 0.001
#     batch_size = 32
#     num_epochs = 10
#     num_models = 6
#     data_points_per_model = [100000,1000,100000,100000,1]
#     model_filepaths = ['whaaaat_test_model_{}.pth'.format(i) for i in range(num_models)]
#
#     for i in range(num_models):
#         print("Training 2nd Model", i)
#
#         # Initialize or load the model
#         if os.path.exists(model_filepaths[i]):
#             model = load_model(input_size, output_size, model_filepaths[i])
#             print("Model loaded.")
#         else:
#             model = NeuralNetwork(input_size, output_size)
#             optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
#             trainer = Trainer(model, dataset, batch_size, learning_rate, num_epochs)
#             losses = trainer.train()
#             save_model(model, model_filepaths[i])
#             print("Model trained and saved.")
#
#         # Generate a new dataset using the current model
#         new_dataset = Data()
#         new_dataset = CustomDataset(new_dataset.generate_NN_data(data_points_per_model[i], model))
#
#         dataset = new_dataset
