"""
Author: Andino Boerst
"""
#import pandas as pd
import numpy as np
import pickle
import my_scripts.simulation as sim
import chaospy as cp

NUM_START = 60
NUM_EXTENSIONS = 10

class MyData:
    def __init__(self, params, restart=False) -> None:
        self.params = params
        if restart:
            self.load_restart()
        else:
            self.initialize_data()

    def __str__(self) -> str:
        return f"parameters: {self.params},\nH: {self.H},\nX: {self.X}"

    def load_restart(self):
        with open('save_restart/my_data.pickle', 'rb') as f:
            data = pickle.load(f)
        self.H = data["H"]
        self.X = data["X"]
        self.params = data["params"]

    def save_restart(self):
        data = {"H": self.H, "X": self.X, "params": self.params}
        with open('save_restart/my_data.pickle', 'wb') as f:
            pickle.dump(data, f)

    def initialize_data(self):
        self.X = np.array([]) # input parameters to the ML model (In this case the y coordinates of my measurement points)
        self.define_X(NUM_START)
        self.H = sim.run_sims(self.X, self.params) # ouput parameters of the ML model (In this case the material parameters to be varied)
        self.save_restart()

    def define_X(self, num_points=NUM_EXTENSIONS):
        dists = np.empty(len(self.params), dtype=object)
        for i, param in enumerate(self.params):
            dists[i] = cp.Uniform(param["lower"], param["upper"])
        join_dist=cp.J(*dists)
        new_X = join_dist.sample(num_points, rule='halton').T
        if np.size(self.X)==0:
            self.X = new_X
        else:
            self.X = np.concatenate((self.X, new_X[self.X.shape[0]:]))


    def extend_data(self, n_samples=NUM_EXTENSIONS):
        self.define_X()
        self.H = np.concatenate((self.H, sim.run_sims(self.X[-n_samples:], self.params)))
        self.save_restart()

    def add_predefined_entries(self, H, X):
        self.add_predefined_H(H)
        self.add_predefined_X(X)

    def add_predefined_H(self, H):
        if np.size(self.H)==0:
            self.H = H
        else:
            self.H = np.concatenate((self.H, H))
        self.save_restart()

    def add_predefined_X(self, X):
        if np.size(self.X)==0:
            self.X = X
        else:
            self.X = np.concatenate((self.X, X))
        self.save_restart()

