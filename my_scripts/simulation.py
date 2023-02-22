"""
Author: Andino Boerst
"""
import numpy as np
import os
import subprocess
import json
import vtk
from vtk.util import numpy_support
import re
import shutil
import sys
import asyncio

TOLERANCE = 0.001
TO_CHECK = (0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4)

PATH = f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}/my_files"

def run_sims(X, params):

    with open(f"{PATH}/ProjectParameters.json", 'r') as f:
        end_time = json.load(f)["problem_data"]["end_time"]

    p = re.compile('TIME:  (\d+.\d+|\d+e-\d+)')

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
        process = subprocess.Popen(f"/home/andinoboerst/anaconda3/envs/kratos_env/bin/python -u {PATH}/MainKratos.py", shell=True, cwd=PATH, stdout=asyncio.subprocess.PIPE, text=True)
        for line in iter(process.stdout.readline, ''):
            if "TIME" in line:
                curr_time = float(p.search(line.rstrip()).group(1))
                completion_perc = curr_time/end_time
                sys.stdout.write(f"\r[{'='*int(100*completion_perc):<100}] {completion_perc:.0%}")
                sys.stdout.flush()
        status = process.wait()
        print("\n")
        if status != 0:
            raise Exception("Simulation could not be run.")

        os.remove(f"{PATH}/ParticleMaterials_new.json")

        # Extract the h from the simulation results
        res.append(extract_results())

        shutil.rmtree(f"{PATH}/vtk_output")

    return np.array(res)

def extract_results():
    results_folder = PATH + "/vtk_output"
    files = os.listdir(results_folder)
    p = re.compile('^MPM_Material(\d+).*\.vtu$')
    mat_files = [p.search(f) for f in files]
    step_ind = [int(r.group(1)) for r in mat_files if r]
    file_name = f"{PATH}/vtk_output/MPM_Material{max(step_ind)}.vtu"

    reader = vtk.vtkXMLUnstructuredGridReader()
    reader.SetFileName(file_name)
    reader.Update()
    output = reader.GetOutput()
    point_coordinates = numpy_support.vtk_to_numpy(output.GetPoints().GetData())
    split_coordinates = np.hsplit(point_coordinates, np.array([1,2]))
    x_coord = split_coordinates[0].T[0]
    y_coord = split_coordinates[1].T[0]
    
    # measure max y coord at different points of x: {0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4} -> with a tolerance of 0.001
    # the sandbox starts with a box from (0,0) to (0.2, 0.1) and the grid is a box from (0,0) to (0.55,0.15)
    y_max = []
    for point in TO_CHECK:
        indices = (x_coord > (point-TOLERANCE)) & (x_coord < (point+TOLERANCE))
        if np.any(indices):
            y_max.append(np.max(y_coord[indices]))
        else:
            y_max.append(0)

    return y_max


if __name__=="__main__":
    print(extract_results())
