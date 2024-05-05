import time

import torch
from matplotlib import pyplot as plt

from NeuralNetwork import load_model
from Trainer import test_model_NNs, test_model


#
#
#
if __name__ == '__main__':

    model = load_model(113, 32, "good_nns/good_boy_3b.pth")
    #
    model1 = load_model(113, 32, "amazing_boy_3b.pth")
    model2 = load_model(113, 32, "amazing_boy_3a.pth")
    model3 = load_model(113, 32, "bad_boy_3a.pth")
    # model3 = load_model(113, 32, "bad_boy_3c.pth")
    # model4 = load_model(113, 32, "bad_boy_3d.pth")
    # model5 = load_model(113, 32, "bad_boy_3e.pth")
    # model6 = load_model(113, 32, "bad_boy_3f.pth")

    test_model(model,10000)
    # test_model(model7,5000)
    #test_model(model1,1000)
    #test_model(model2,10000)


    # test_model_NNs(model,model1,500)
    # test_model_NNs(model,model2,500)
    # test_model_NNs(model,model3,500)
    # test_model_NNs(model,model4,500)
    # test_model_NNs(model,model5,500)
    # test_model_NNs(model,model6,500)
    # test_model_NNs(model,model7,10000)
    # test_model_NNs(model,model8,500)


    print("Model loaded.")
    #test_model(model4,10000)
    print("Test finished.")



# if __name__ == '__main__':
#     model_files = ["traineeed_model_0.pth", "traineeed_model_1.pth", "traineeed_model_2.pth",
#                    "traineeed_model_3.pth"]
#     num_manches = 1000
#
#     scores = []
#
#     for model_file in model_files:
#         model = load_model(113, 32, model_file)
#         print(f"Testing model {model_file}...")
#         avg_score = test_model(model, num_manches)
#         scores.append(avg_score)
#
#     # Plot the scores
#     plt.figure(figsize=(8, 6))
#     plt.bar(range(len(scores)), scores, color='blue')
#     plt.xlabel('Model Index')
#     plt.ylabel('Average Score')
#     plt.title('Average Scores of Models')
#     plt.xticks(range(len(scores)), ['Model 0', 'Model 1', 'Model 2','Model 3'])
#     plt.grid(axis='y', linestyle='--', alpha=0.7)
#     plt.show()
#
#     print("Test finished.")