"""
Author: Andino Boerst
"""
import my_scripts.data as dt



def main():
    print("Start script")
    restarted = False
    params = [{"id": 1, "name": "DENSITY", "lower": 2200, "upper": 2400},
              {"id": 2, "name": "YOUNG_MODULUS", "lower": 5500000, "upper": 6500000},
              {"id": 3, "name": "POISSON_RATIO", "lower": 0.28, "upper": 0.32}]
    # Step 1: Generate the data
    data = dt.MyData( params, restarted)
    # Step 2: Train the ML model

if __name__=="__main__":
    main()