import torch
import unittest
from src.NeuralNetwork import NeuralNetwork

class TestNN(unittest.TestCase):
    def test_squared_error_masked(self):
        # Define input tensors
        y_true = torch.tensor([0, -3, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=torch.float32)
        y_pred = torch.tensor([0, -2, 1, -1, 2, 3, 4, 0, 0, 0, 0], dtype=torch.float32)

        # Set scale factor
        scale_factor = 1.0

        # Calculate the expected loss manually
        mask = y_true != 0
        err = y_pred - (y_true * scale_factor)
        masked_err = err[mask]
        expected_loss = torch.sum(masked_err ** 2)

        # Call the squared_error_masked function
        loss = NeuralNetwork.squared_error_masked(y_true, y_pred, scale_factor)
        print(loss)
        # Assert that the calculated loss matches the expected loss
        self.assertTrue(torch.allclose(loss, expected_loss))