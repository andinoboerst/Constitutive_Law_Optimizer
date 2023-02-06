import pandas as pd
import numpy as np
import pickle
import my_scripts.simulation as sim

class MyData:
    def __init__(self, restarted) -> None:
        if restarted:
            self.load_restart()
        else:
            self.initialize_data()

    def load_restart(self):
        with open('save_restart/my_data.pickle', 'rb') as f:
            data = pickle.load(f)
        self.H = data["H"]
        self.X = data["X"]

    def save_data(self):
        data = {"H": self.H, "X": self.X}
        with open('save_restart/my_data.pickle', 'wb') as f:
            pickle.dump(data, f)

    def initialize_data(self):
        self.define_H(60)
        self.X = sim.run_sims(self.H) # ouput parameters (In this case the material parameters to be varied)
        self.save_data()

    def define_H(self, num_points=10):
        self.H = np.array([[1, 2, 3], [4, 5, 6]]) # input parameters (In this case the y coordinates of my measurement points)
        print(self.H)