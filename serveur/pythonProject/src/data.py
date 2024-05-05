from Player import RandomPlayer, NNPlayer


class Data:
    def __init__(self):
        self.dataset = {}

    # A ameliorer: gerer les doublons
    def add_dataset(self, new_dataset):
        self.dataset.update(new_dataset)

    # def __str__(self):
    #     unique_keys = len(self.dataset)
    #     return f"Nombre de données: {unique_keys}"
    def simplify_key(self, key):
        return "(" + ",".join(str(x) for x in key[:5]) + ",...," + str(key[-5]) + ")"

    def __iter__(self):
        return iter(self.dataset.items())

    def __str__(self):
        result = ""
        for key, value in self.dataset.items():
            simplified_key = self.simplify_key(key)
            result += f"{simplified_key}: {value}\n"
        return result.strip()

    def get_dataset(self):
        return self.dataset

    def generate_random_player_data(self, num_tricks):
        from src.manche import Manche
        for i in range(num_tricks):
            manche = Manche(
                [RandomPlayer("pedro"), RandomPlayer("pedrito"), RandomPlayer("pedri"), RandomPlayer("pedru")]
            )
            manche.play_to_update_random_dataset(self)
            if i % 1000 == 0:
                print(i)
        return self

    def generate_NN_data(self, num_tricks, model):
        from src.manche import Manche
        for i in range(num_tricks):
            manche = Manche(
                [NNPlayer("pedro", model), NNPlayer("pedrito", model), NNPlayer("pedri", model),
                 NNPlayer("pedru", model)]
            )
            manche.play_to_update_nn_dataset(self)
            if i % 1000 == 0:
                print(i)

        return self
