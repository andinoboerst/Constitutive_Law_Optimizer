"""
Author: Andino Boerst
"""
import my_scripts.data as dt
import my_scripts.ml_model as ml
import my_scripts.simulation as sm
import numpy as np

PARAMS = [{"id": 1, "name": "DENSITY", "lower": 2200, "upper": 2400},
          {"id": 2, "name": "YOUNG_MODULUS", "lower": 5500000, "upper": 6500000},
          {"id": 3, "name": "POISSON_RATIO", "lower": 0.28, "upper": 0.32}]

def start_new() -> ml.ML_model:
    # Step 1: Generate the data
    data = dt.MyData(PARAMS)
    #print(data)
    # Step 2: Train the ML model
    model = ml.ML_model(data, "knn regressor")
    return model
    

def add_more(n_samples: int) -> ml.ML_model:
    data = dt.MyData(restart=True)
    data.extend_data(n_samples)

    model = ml.ML_model(data, "knn regressor", restart=False)
    return model

def load_model() -> ml.ML_model:
    return ml.ML_model(restart=True)

def load_data() -> dt.MyData:
    return dt.MyData(restart=True)

def continue_sims() -> ml.ML_model:
    data = dt.MyData(restart=True)
    data.continue_simulations()

    model = ml.ML_model(data, "knn regressor", restart=False)
    return model

def validate_model(to_predict: list[list[float]]) -> float:
    model = load_model()

    return model.validate_model(to_predict)


def main():
    model = start_new()
    #model = add_more(5)
    #model = continue_sims()
    #model = load_model()

    #Step 3: Predict the new parameter combinations
    print(model.predict([[0.08, 0.067, 0.06, 0.043, 0.037, 0.02, 0.008]]))

    #print(validate_model([[0.08, 0.067, 0.06, 0.043, 0.037, 0.02, 0.008]]))


if __name__=="__main__":
    main()