"""
Author: Andino Boerst
"""
#import pandas as pd
import numpy as np
import pickle
import my_scripts.simulation as sim
import chaospy as cp
import os
import json
import warnings

NUM_START = 60
NUM_EXTENSIONS = 10

PATH = f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}/save_restart"

class MyData:
    def __init__(self, params: list[dict]=None, restart: bool=False) -> None:
        if restart:
            if params != None:
                warnings.warn("Will not use passed parameters since it is a restart.")
            self.load_restart()
        else:
            if params == None:
                raise ValueError("Need to pass parameters when starting with new data.")
            self.params = params
            self.initialize_data()

    def __str__(self) -> str:
        return f"parameters: {self.params},\nH: {self.H},\nX: {self.X}"

    def load_restart(self) -> None:
        with open(f"{PATH}/my_data.pickle", 'rb') as f:
            save_data = pickle.load(f)
        self.H = save_data["H"]
        self.X = save_data["X"]
        self.params = save_data["params"]
        print(f"Loaded data class with: len(H): {len(self.H)}, len(X): {len(self.X)}.")

    def save_restart(self) -> None:
        save_data = {"H": self.H, "X": self.X, "params": self.params}
        with open(f"{PATH}/my_data.pickle", 'wb') as f:
            pickle.dump(save_data, f)

    def initialize_data(self) -> None:
        self.X = np.array([]) # input parameters to the ML model (In this case the y coordinates of my measurement points)
        self.H = np.array([])
        self.define_X(NUM_START)
        self.H = sim.run_sims(self.X, self.params) # ouput parameters of the ML model (In this case the material parameters to be varied)
        self.save_restart()

    def define_X(self, num_points: int=NUM_EXTENSIONS) -> None:
        dists = np.empty(len(self.params), dtype=object)
        for i, param in enumerate(self.params):
            dists[i] = cp.Uniform(param["lower"], param["upper"])
        join_dist=cp.J(*dists)
        new_X = join_dist.sample(num_points+len(self.X), rule='halton').T
        if np.size(self.X)==0:
            self.X = new_X
        else:
            self.X = np.concatenate((self.X, new_X[self.X.shape[0]:]))
        self.save_restart()


    def extend_data(self, n_samples: int=NUM_EXTENSIONS) -> None:
        self.define_X(n_samples)
        self.H = np.concatenate((self.H, sim.run_sims(self.X[-n_samples:], self.params)))
        self.save_restart()

    def add_predefined_entries(self, H: np.array, X: np.array) -> None:
        self.add_predefined_H(H)
        self.add_predefined_X(X)

    def add_predefined_H(self, H: np.array) -> None:
        if np.size(self.H)==0:
            self.H = H
        else:
            self.H = np.concatenate((self.H, H))
        self.save_restart()

    def add_predefined_X(self, X: np.array) -> None:
        if np.size(self.X)==0:
            self.X = X
        else:
            self.X = np.concatenate((self.X, X))
        self.save_restart()

    def continue_simulations(self) -> None:
        if os.path.isfile(f"{PATH}/current_sim_results.json"):
            with open(f"{PATH}/current_sim_results.json", 'r') as f:
                existing_results = np.array(json.load(f)['results'])

            if np.size(self.H)==0:
                self.H = existing_results
            else:
                self.H = np.concatenate((self.H, existing_results))
            print(len(self.H))
            self.save_restart()
            os.remove(f"{PATH}/current_sim_results.json")

        start_sims = len(self.X) - len(self.H)
        self.H = np.concatenate((self.H, sim.run_sims(self.X[-start_sims:], self.params)))
        self.save_restart()
