import time
import os, glob
import psutil
import subprocess
from subprocess import Popen, PIPE
import pandas as pd
import numpy as np

SOLVERS_DIR = "executables/"
CNF_DIR = "../formulas/"

Ns = [72, 132, 192, 212, 282, 358, 372, 382, 390, 932, 400]
examples = []

for N in Ns:
    examples.append(str(N) + ".g2.10.cnf")
    examples.append(str(N) + ".g2.9.cnf")
    examples.append(str(N) + ".g2.8.cnf")

if __name__ == "__main__":

    solvers = glob.glob(f"{SOLVERS_DIR}/*")

    tmp = []

    for solver in solvers:
        tmp.append(os.path.basename(solver))

    solvers = tmp[:]

    
    for example in examples:

        results = []

        print(example)

        for solver in solvers:
            
            cmd = "./" + SOLVERS_DIR + solver + " " + CNF_DIR + example
            
            timers = dict()
            timers["solver"] = solver
            timers["example"] = example

            print(solver)

            for i in range(10):
                t1 = time.time()
                with subprocess.Popen([cmd], stdout=PIPE, shell=True) as proc:
                    
                    p = psutil.Process(proc.pid)
                    p.memory_info().rss
                    p.memory_info().vms

                    while proc.poll():
                        time.sleep(.01)

                t2 = time.time()

                timers[i] = t2 - t1

                #print(f"{solver}: {t2 - t1}")

            results.append(timers)

        df = pd.DataFrame(results)
        print(df.head())
        df.to_csv(example + ".csv", index=False)