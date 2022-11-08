import matplotlib.pyplot as plt
from dropping_policy import simulation
import numpy as np


N = [100, 1000, 10000, 10**5, 10**6]#, 10**7]
D = [1,2,4]

#initialize 3 dictionary: one for each metric to plot whose keys are the value of d
max_values = dict.fromkeys(D, [])
acc_values = dict.fromkeys(D, [])
theor_vals = dict.fromkeys(D, [])
header="D,N,max occupancy,theoretical,accuracy,min occupancy, avg occupancy \n"
with open("results.csv", "w") as csvf_header:
    csvf_header.write(header)

with open("results.csv", "a") as csvf:
    for d in D:
        maxs =list() # list of max levels for each n
        accs = list() # list of accuracies for each n
        theors = list() # list of theoretical max levels for each n
        for n in N:
            max_occ, min_occ, avg_occ, bins = simulation(n, policy= d)
            maxs.append(max_occ)
            print(f"for d: {d} and N: {n}, min occupancy = {min_occ}, avg occupancy = {avg_occ}")
            # for each policy we have differenct values of the theoretical max occupancy level
            if d == 1: # if policy == random dropping
                theoretical = (np.log(n)/(np.log(np.log(n))))
                theors.append(theors) 
            if d != 1: # if policy == random load balancing
                theoretical = (np.log(np.log(n))/(np.log(d)))
                theors.append(theors)
            acc = theoretical/max_occ
            accs.append(acc)
            csvf.write(f"{d},{n},{max_occ},{theoretical},{acc},{min_occ},{avg_occ}\n")
        acc_values[d] = accs
        max_values[d] = maxs
        theor_vals[d] = theors
    


fig, ax = plt.subplots(2, 1, figsize=(20, 15))
for key_m in max_values.keys():
    ax[0].plot(N, max_values[key_m])
    ax[0].set_label(f"d: {key_m}")

ax[0].set_ylabel("Max occupancy levels")
ax[0].set_xlabel("Number of elements")
ax[0].set_xscale("log")

ax[0].legend(labels= [f"d: {d}" for d in acc_values.keys()])
ax[0].grid()
for key in acc_values.keys():
    ax[1].plot(N, acc_values[key])
    ax[1].set_label(f"d: {key}")

ax[1].set_ylabel("Accuracy level")
ax[1].set_xlabel("Number of elements")
ax[1].set_xscale("log")
ax[1].grid()
ax[1].legend(labels= [f"d: {d}" for d in acc_values.keys()])

plt.savefig("graphs/N-occupancy_level.png")
