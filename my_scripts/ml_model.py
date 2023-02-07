"""
Author: Andino Boerst
"""
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression

MODEL_OPTIONS = {"linear regression": LinearRegression}

class ML_model:
    def __init__(self, data, restart=False, model_name="linear regression") -> None:
        self.data = data
        if restart:
            self.load_restart()
        else:
            self.model_name = model_name
            self.model = MODEL_OPTIONS[self.model_name]
            self.train()

    def load_restart(self):
        with open('save_restart/my_ml_model.pickle', 'rb') as f:
            data = pickle.load(f)
        self.model_name = data["model_name"]
        self.model = MODEL_OPTIONS[self.model_name]
        self.models = data["models"]

    def save_restart(self):
        data = {"model_name": self.model_name, "models": self.models}
        with open('save_restart/my_ml_model.pickle', 'wb') as f:
            pickle.dump(data, f)

    def train(self):
        self.models = []
        for i in range(len(self.data.params)):
            self.models.append(self.model().fit(self.data.H, self.data.X[:,i]))
        self.save_restart()

    def predict(self, h):
        res = []
        for model in self.models:
            res.append(model.predict(h))
        return np.array(res).T