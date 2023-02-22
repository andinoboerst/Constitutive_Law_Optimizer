"""
Author: Andino Boerst
"""
import numpy as np
import pickle
import warnings
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
import os

MODEL_OPTIONS = {"linear regression": LinearRegression, "knn regressor": KNeighborsRegressor}

PATH = f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}/save_restart"

class ML_model:
    def __init__(self, data=None, model_name: str="linear regression", restart: bool=False) -> None:
        if restart:
            if data != None:
                warnings.warn("Passed data object will not be considered on restart.")
            self.load_restart()
        else:
            if data == None:
                raise ValueError("Need to pass data object when starting new model.")
            if model_name not in MODEL_OPTIONS:
                self.model_name = "linear regression"
                warnings.warn("Model name not an option, using default linear regression model.")
            else:
                self.model_name = model_name
            self.data = data
            self.model = MODEL_OPTIONS[self.model_name]
            self.train()

    def load_restart(self) -> None:
        with open(f"{PATH}/my_ml_model.pickle", 'rb') as f:
            save_data = pickle.load(f)
        self.model_name = save_data["model_name"]
        self.model = MODEL_OPTIONS[self.model_name]
        self.models = save_data["models"]
        self.data = save_data["data"]
        print(f"Loaded ML model with: ml alg: {self.model_name}, len(data): {len(self.data.H)}.")

    def save_restart(self) -> None:
        save_data = {"model_name": self.model_name, "models": self.models, "data": self.data}
        with open(f"{PATH}/my_ml_model.pickle", 'wb') as f:
            pickle.dump(save_data, f)

    def train(self) -> None:
        self.models = []
        for i in range(len(self.data.params)):
            self.models.append(self.model().fit(self.data.H, self.data.X[:,i]))
        self.save_restart()

    def predict(self, h: list[list[float]]) -> None:
        res = []
        for model in self.models:
            res.append(model.predict(h))
        return np.array(res).T