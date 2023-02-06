import numpy as np
import os
import subprocess

def run_sims(X, H=np.array([])):

    new_res = np.apply_along_axis(launch_simulation, axis=1, arr=X)
    if np.size(H)==0:
        return new_res
    else:
        return np.concatenate((H, np.apply_along_axis(launch_simulation, axis=1, arr=X)))
    

def launch_simulation(x):
    path = f"{os.getcwd()}/my_files"

    # Here need to modify the ParticleMaterials.json file according to entries in h

    # Run the simulation with the given parameters
    subprocess.run(["/home/andinoboerst/anaconda3/envs/kratos_env/bin/python", f"{path}/MainKratos.py"], cwd=path)

    # Extract the X from the simulation results
    H = np.array([1, 2, 3])

    os.remove(f"{path}/falling_sand_ball_results.json")

    return H
