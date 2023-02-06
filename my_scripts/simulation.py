import numpy as np
import os
import subprocess

def run_sims(H, X=np.array([])):
    print("running sims")
    np.append(X, np.apply_along_axis(launch_simulation, axis=1, arr=H))

    print(X)
    return X

def launch_simulation(x):
    path = f"{os.getcwd()}/my_files"
    print(path)
    subprocess.run(["/home/andinoboerst/anaconda3/envs/kratos_env/bin/python", f"{path}/MainKratos.py"], cwd=path)
    input("press smth")
