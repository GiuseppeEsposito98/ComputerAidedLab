import random
from statistics import stdev, sqrt
from scipy.stats import t
import numpy as np
import pandas as pd
# dict of possible days
# number of students
M = [10,20,40,80,100,200,400] 
#seeds for the run
seeds = [10,30,50]

# care about the probability value 
probabilities_per_dmy = pd.read_csv("probabilities.csv")
# these are the probabilities to be born in a specific date in a specific year so we have to sum these probabilities
probabilities_dm = probabilities_per_dmy.groupby(["mm/dd"]).sum()["probabilities"]
print(probabilities_dm)




'''
def simulation1(m, distribution = "uniform"):
    days = dict.fromkeys(range(365), 0)
    for i in range(m):
        if distribution == "uniform":
            entrance_bd = random.randint(0,365)
        elif distribution == "real":
            entrance_bd = random.choice()
        days[entrance_bd] = days[entrance_bd] + 1
        if days[entrance_bd]9 == 2:
            print(f"for m: {m} we got: {max(days.values())}, in position: {entrance_bd}")
            return i
    print(f"for m: {m} i'm returning 0")
    return 0
        



run_results = list()
# perchè se aumento la confidenza si allarga l'intervallo? risponderà il Bepi del futuro
#confidence = 0.95
for run in seeds:
    random.seed(run)
    first_collision = list()
    for m in M:
        first_collision.append(simulation1(m))
    avg = sum(first_collision)/len(first_collision)
    run_results.append(avg)

std_dev = stdev(run_results)
nu = len(run_results)-1

experimental_mean = sum(run_results)/len(run_results)
for confidence in [0.99, 0.98, 0.97, 0.96, 0.95]:
    t_crit = np.abs(t.ppf((1-confidence)/2,nu))
    lower_bound = experimental_mean-(t_crit*(std_dev/sqrt(len(run_results))))
    upper_bound = experimental_mean+(t_crit*(std_dev/sqrt(len(run_results))))
    print(f"for confidence: {confidence}, lower: {lower_bound}, upper: {upper_bound}")

#print(f"lower: {lower_bound}, run results:{[val for val in run_results]}, upper: {upper_bound}")
'''



