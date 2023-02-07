import numpy as np
import os
import subprocess
import json

def run_sims(X, params):
    return np.apply_along_axis(launch_simulation, axis=1, arr=X, params=params)
    

def launch_simulation(x, params):
    path = f"{os.getcwd()}/my_files"

    # Here need to modify the ParticleMaterials.json file according to entries in x
    with open(f"{path}/ParticleMaterials.json", 'r') as f:
        json_data = json.load(f)

    for i, entry in enumerate(x):
        json_data["properties"][0]["Material"]["Variables"][params[i]["name"]] = entry

    with open(f"{path}/ParticleMaterials_new.json", 'w') as f:
        json.dump(json_data, f, indent=4, separators=(',', ': '))

    # Run the simulation with the given parameters
    subprocess.run(["/home/andinoboerst/anaconda3/envs/kratos_env/bin/python", f"{path}/MainKratos.py"], cwd=path)
    os.remove(f"{path}/ParticleMaterials_new.json")

    # Extract the h from the simulation results
    h = np.array([1, 2, 3])

    os.remove(f"{path}/falling_sand_ball_results.json")

    return h
