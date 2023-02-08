"""
Author: Andino Boerst
"""
import numpy as np
import os
import subprocess
import json

PATH = f"{os.getcwd()}/my_files"

def run_sims(X, params):
    res = []
    for index, row in enumerate(X):
        # Here need to modify the ParticleMaterials.json file according to entries in x
        with open(f"{PATH}/ParticleMaterials.json", 'r') as f:
            json_data = json.load(f)

        for i, entry in enumerate(row):
            json_data["properties"][0]["Material"]["Variables"][params[i]["name"]] = entry

        with open(f"{PATH}/ParticleMaterials_new.json", 'w') as f:
            json.dump(json_data, f, indent=4, separators=(',', ': '))

        # Run the simulation with the given parameters
        print(f"Running simulation {index+1}/{len(X)}")
        status = subprocess.run(["/home/andinoboerst/anaconda3/envs/kratos_env/bin/python", f"{PATH}/MainKratos.py"], cwd=PATH, stdout=subprocess.DEVNULL)
        if status.returncode != 0:
            raise Exception("Simulation could not be run.")
        os.remove(f"{PATH}/ParticleMaterials_new.json")

        # Extract the h from the simulation results
        res.append(np.array([1, 2, 3]))

        os.remove(f"{PATH}/falling_sand_ball_results.json")

    return np.array(res)
