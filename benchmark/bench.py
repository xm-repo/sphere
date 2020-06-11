import time
import os, glob
import psutil
import subprocess
from subprocess import Popen, PIPE
import pandas as pd
import numpy as np
import json

SOLVERS_DIR = "executables/"
CNF_DIR = "../formulas/"

def run_solver(cmd):
    
    t1 = time.time()
    
    with subprocess.Popen([cmd], stdout=PIPE, shell=True) as proc:
       
        p = psutil.Process(proc.pid)
        p.memory_info().rss
        p.memory_info().vms

        while proc.poll():
            time.sleep(.01)

    t2 = time.time()

    return t2 - t1

if __name__ == "__main__":

    formulas = glob.glob(f"{CNF_DIR}/*.10.cnf")
    solvers = glob.glob(f"{SOLVERS_DIR}/*")

    tmp = []

    for solver in solvers:
        tmp.append(os.path.basename(solver))

    solvers = tmp[:]
    
    
    for solver in solvers:
        
        results = {}
        results["preamble"] = {}
        results["preamble"]["program"] = solver
        results["preamble"]["prog_alias"] = solver
        results["preamble"]["prog_args"] = solver
        results["preamble"]["benchmark"] = "10"        

        results["stats"] = {}

        for formula in formulas:        

            cmd = "./" + SOLVERS_DIR + solver + " " + CNF_DIR + formula
            rtime = run_solver(cmd)

            problem = os.path.basename(formula)[:-4]
            results["stats"][problem] = {}
            results["stats"][problem]["status"] = True
            results["stats"][problem]["rtime"] = rtime

            print(solver + " " + problem)

        with open("mkplot/" + solver + ".json", "w") as outfile:
            json.dump(results, outfile)