class Data:
    def __init__(self):
        # structure: {input: output}
        self.dataset = {}

    def add_data(self, input_data, output_data):
        self.dataset[input_data] = output_data

    def set_data_victory(self):
        for input_data in self.dataset:
            self.dataset[input_data] = 1

    def set_data_defeat(self):
        for input_data in self.dataset:
            self.dataset[input_data] = 0
