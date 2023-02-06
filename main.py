"""
Author: Andino Boerst
"""
import my_scripts.data as dt



def main():
    print("Start script")
    restarted = False
    params = [{"id": "p1", "name": "something", "lower": 2, "upper": 5},
              {"id": "p2", "name": "something2", "lower": 3, "upper": 20},
              {"id": "p3", "name": "something3", "lower": 80, "upper": 100}]
    # Step 1: Generate the data
    data = dt.MyData( params, restarted)
    # Step 2: 

if __name__=="__main__":
    main()