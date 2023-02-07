"""
Author: Andino Boerst
"""
import numpy as np
from sklearn.linear_model import LinearRegression

MODEL_OPTIONS = {"linear regression": LinearRegression}

class ML_model:
    def __init__(self, data, model_name="linear regression") -> None:
        self.data = data
        self.model_name = model_name
        self.model = MODEL_OPTIONS[self.model_name]
        self.train()

    def train(self):
        self.models = []
        for i in range(len(self.data.params)):
            self.models.append(self.model().fit(self.data.H, self.data.X[:,i]))

    def predict(self, h):
        res = []
        for model in self.models:
            res.append(model.predict(h))
        return np.array(res).T