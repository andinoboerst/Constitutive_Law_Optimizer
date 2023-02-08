"""
Author: Andino Boerst
"""
import my_scripts.data as dt
import my_scripts.ml_model as ml


def main():
    restarted = False
    params = [{"id": 1, "name": "DENSITY", "lower": 2200, "upper": 2400},
              {"id": 2, "name": "YOUNG_MODULUS", "lower": 5500000, "upper": 6500000},
              {"id": 3, "name": "POISSON_RATIO", "lower": 0.28, "upper": 0.32}]
    # Step 1: Generate the data
    data = dt.MyData( params, restarted)
    #print(data)
    # Step 2: Train the ML model
    model = ml.ML_model(data, "knn regressor")
    #Step 3: Predict the new parameter combinations
    print(model.predict([[1, 2, 3], [1, 8, 3]]))

if __name__=="__main__":
    main()