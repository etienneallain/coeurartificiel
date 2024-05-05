import torch
import torch.nn as nn
import torch.nn.functional as F


input_size = 32
hidden_size = 64
output_size = 32
class HeartsNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(HeartsNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

model = HeartsNN(input_size, hidden_size, output_size)
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
