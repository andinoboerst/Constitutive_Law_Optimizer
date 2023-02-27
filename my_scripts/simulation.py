"""
Author: Andino Boerst
"""
import numpy as np
import os, sys, subprocess, shutil, asyncio
import json, vtk
from vtk.util import numpy_support
import re
#import progressbar

TOLERANCE = 0.001
TO_CHECK = (0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4)

LAUNCH_ON_SERVER = False
PROGRESS_BAR_LENGTH = 50

PATH = f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}/my_files"
P_REGEX = re.compile('TIME:  (\d+.\d+|\d+e[+-]\d+)')
PYTHON_PATH = "/home/andinoboerst/anaconda3/envs/kratos_env/bin/python"

def run_sims(X, params) -> np.array:

    with open(f"{PATH}/ProjectParameters.json", 'r') as f:
        end_time = json.load(f)["problem_data"]["end_time"]

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

        # launch the simulations and extract the results
        if LAUNCH_ON_SERVER:
            res.append(launch_sim_server())
        else:
            res.append(launch_sim_local(end_time))

        with open(f"{os.path.dirname(PATH)}/save_restart/current_sim_results.json", 'w') as f:
            json_dict = {"results": res}
            json.dump(json_dict, f, indent=4)

        shutil.rmtree(f"{PATH}/vtk_output")

    os.remove(f"{os.path.dirname(PATH)}/save_restart/current_sim_results.json")
    return np.array(res)


def launch_sim_local(end_time):
    try:
        #sim_bar = progressbar.ProgressBar(maxval=1.00001)
        #sim_bar.start()
        process = subprocess.Popen(f"{PYTHON_PATH} -u {PATH}/MainKratos.py", shell=True, cwd=PATH, stdout=asyncio.subprocess.PIPE, text=True)
        for line in iter(process.stdout.readline, ''):
            if "TIME" in line:
                curr_time = float(P_REGEX.search(line.rstrip()).group(1))
                completion_perc = curr_time/end_time
                sys.stdout.write(f"\r[{'='*int(PROGRESS_BAR_LENGTH*completion_perc):<{PROGRESS_BAR_LENGTH}}] {completion_perc:.0%}")
                sys.stdout.flush()
                #sim_bar.update(curr_time/end_time)
        status = process.wait()
        #sim_bar.finish()
    except subprocess.CalledProcessError as e:
        print(e.output)
    if status != 0:
        raise Exception("Simulation could not be run.")
    
    os.remove(f"{PATH}/ParticleMaterials_new.json")

    return extract_results_local() # return the extracted results

def extract_results_local() -> list[float]:
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


def launch_sim_server():
    return []


if __name__=="__main__":
    print(extract_results_local())
