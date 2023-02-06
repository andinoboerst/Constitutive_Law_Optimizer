import numpy as np
import os
import subprocess

def run_sims(H, X=np.array([])):

    new_res = np.apply_along_axis(launch_simulation, axis=1, arr=H)
    if np.size(X)==0:
        return new_res
    else:
        return np.concatenate((X, np.apply_along_axis(launch_simulation, axis=1, arr=H)))
    

def launch_simulation(h):
    path = f"{os.getcwd()}/my_files"

    # Here need to modify the ParticleMaterials.json file according to entries in h

    # Run the simulation with the given parameters
    subprocess.run(["/home/andinoboerst/anaconda3/envs/kratos_env/bin/python", f"{path}/MainKratos.py"], cwd=path)

    # Extract the X from the simulation results
    X = np.array([1, 2, 3])

    os.remove(f"{path}/falling_sand_ball_results.json")

    return X
