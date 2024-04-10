from src.NeuralNetwork import load_model
from src.Trainer import test_model_NNs, test_model

if __name__ == '__main__':
    model = load_model(112, 32, "trained_model_2.pth")
    model2 = load_model(112, 32, "trained_model_1.pth")
    print("Model loaded.")
    test_model_NNs(model, model2, 1000)
    test_model(model,500)
    print("Test finished.")
