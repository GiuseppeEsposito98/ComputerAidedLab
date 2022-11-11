import random
#from statistics import stdev, sqrt
from scipy.stats import t
import numpy as np
import pandas as pd
from simulation import *
# dict of possible days
# number of students
M = [10,20,40,80,100,200,400] 
#seeds for the run
seeds = [1313, 777, 23123]



def confidence_interval(run_results, confidence, dof):
    return t.interval(confidence=confidence, df=dof, loc=np.mean(run_results), scale=np.var(run_results))


run_results = list()
confidence = 0.95
for run in seeds:
    random.seed(run)
    np.random.seed(run)
    first_collision = list()
    for m in M:
        first_collision.append(simulation1(m, distribution="real"))
    avg = sum(first_collision)/len(first_collision)
    run_results.append(avg)

nu = len(run_results)-1
confidence_interval(run_results, confidence, nu)
# by means of this confidence interval because we are confident a ...% that the real value (theoretical one)
# is contained in the confidence interval.



#print(f"lower: {lower_bound}, run results:{[val for val in run_results]}, upper: {upper_bound}")




