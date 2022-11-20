import random
from math import exp
import numpy as np
from simulation import *
from time import time
random.seed(423)
np.random.seed(423) 

def main():
    filename = "US_births_2000-2014_SSA.csv"
    from_data_to_probs(filename)
    # input parameters
    M = [0, 10,20,30,40,50,60,70,80,90,100]
    # this is an algorithm which has a very low computational cost, so in order to make the experiment repeatible 
    # we can decide to run for a specific number of iterations and be sure that the runs will not share the same results
    # since the pseudo-random number generator of python uses the current last generation as seed of the new generation.
    ITERATIONS = 200
    N = [100, 300, 500, 1000]
    print(f"=====MAIN EXPERIMENT=====")
    print("Input parameter:")
    print(f"M (List of class sizes): {M}")
    print(f"Iterations: {ITERATIONS}")
    # probabilities of the real distribution for each date
    probabilities = pd.read_csv(f"births_distribution/probabilities.csv")["probabilities"].tolist()

    # Average minimum number such that a conflict occurs - uniform distribution
    first_collisions_unif = list()
    exp1_time_start = time()
    for _ in range(ITERATIONS):
        first_collisions_unif.append(expected_value(n = 366, distribution="uniform"))
    
    #theoretical value of the mean of first collisions
    theoretical_avg = 1.25*sqrt(366)

    # confidence interval of the first collisions collected for each iteration
    ci = confidence_interval_avg(first_collisions_unif, alpha = 0.015)
    exp1_time_end = time()
    print(f"UNIFORM DISTRIBUTION (confidence interval 97%) - lower bound : {ci[0]} theoretical value: {theoretical_avg}, upper bound: {ci[1]}")
    print(f"Simulation time for the first experimen with uniform distributiont: {exp1_time_end - exp1_time_start}")
    print()
    # Average minimum number such that a conflict occurs - real distribution
    first_collisions_real = list()
    exp2_time_start = time()
    for _ in range(ITERATIONS):
        first_collisions_real.append(expected_value(n = 366, probabilities = probabilities, distribution="real"))

    # confidence interval of the first collisions collected for each iteration
    ci = confidence_interval_avg(first_collisions_real, alpha = 0.015)
    exp2_time_end = time()
    print(f"REAL DISTRIBUTION (confidence interval 97%) - lower bound : {ci[0]} theoretical value: {theoretical_avg}, upper bound: {ci[1]}")
    print(f"Simulation time for the first experiment with real distribution: {exp2_time_end - exp2_time_start}")
    print()
    # M VS Probability of conflict - uniform distribution
    tmp_unif = list()
    theor_vals = list()
    exp3_time_start = time()
    for m in M:
        theor_vals.append(1-exp(-(m**2)/(2*365)))
        p = probability(n = 366, m = m, iterations = ITERATIONS, distribution="uniform")
        tmp_unif.append(p)
    exp3_time_end = time()
    print(f"Simulation time for the second experiment with uniform distribution: {exp3_time_end - exp3_time_start}")
    print()
    # M VS Probability of conflict - real distribution
    tmp_real = list()
    theor_vals = list()
    exp4_time_start = time()
    for m in M:
        theor_vals.append(1-exp(-(m**2)/(2*365)))
        # probability to observe at least a conflict
        p = probability(n = 366, m = m, iterations = ITERATIONS, probabilities=probabilities, distribution="real")
        tmp_real.append(p)
    exp4_time_end = time()
    print(f"Simulation time for the second experiment with real distribution: {exp4_time_end - exp4_time_start}")

    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (13,7))
    fig.suptitle("Probability to have at least one conflict")
    plot_prob(ax1, tmp_unif, M, theor_vals, "uniform", ITERATIONS, alpha = 0.05)
    plot_prob(ax2, tmp_real, M, theor_vals, "real", ITERATIONS, alpha = 0.05)
    fig.savefig("graphs/Class size VS Probabiity of conflict")
    fig.show()

    # ============EXTENSION============
    # for what concernes the average we will consider only the uniform distribution case because we so not have the 
    # real distribution for n != 365
    # Average minimum number such that a conflict occurs - uniform distribution
    print()
    print(f"=====EXTENSION=====")
    print("Input parameter:")
    print(f"M (List of class sizes): {M}")
    print(f"Iterations: {ITERATIONS}")
    print(f"N (list of class possible extractions): {N}")
    m_lists = list()
    theor_avg_list = list()
    exp5_time_start = time()
    
    for n in N:
        # repeat the first experiment for different values of n keeping the distribution fixed to uniform
        first_collisions_unif_var = list()
        for _ in range(ITERATIONS):
            first_collisions_unif_var.append(expected_value(n = n, distribution="uniform"))
        m_lists.append(first_collisions_unif_var)
        theoretical_avg_var = 1.25*sqrt(n)
        theor_avg_list.append(theoretical_avg_var)
    plot_avgs(N, np.array(m_lists), theor_avg_list)

    tmp_unif_var = list()
    theor_vals_var = list()
    all_p = list()
    all_theor = list()
    for n in N:
        # repeat the second experiment for different values of n keeping the distribution fixed to uniform
        tmp_unif_var = list()
        theor_vals_var = list()
        for m in M:
            theor_vals_var.append(1-exp(-(m**2)/(2*n)))
            p = probability(n = n, m = m, iterations = ITERATIONS, distribution="uniform")
            tmp_unif_var.append(p)
        # a list containing 7 lists (one for each n) of 11 probabilities (one for each m)
        all_p.append(tmp_unif_var)
        all_theor.append(theor_vals_var)
    exp5_time_end = time()
    print(f"Simulation time for the general case of the birthday paradox: {exp5_time_end - exp5_time_start}")
    print()
    print(f"Time of the whole simulation: {exp5_time_end + exp4_time_end + exp3_time_end + exp2_time_end + exp1_time_end - exp5_time_start - exp4_time_start - exp3_time_start- exp2_time_start - exp1_time_start}")
    fig, ax = plt.subplots(1, 1)
    fig.suptitle("Probability to have at least one conflict for different values of n")
    plot_prob_var(ax, all_p, M, all_theor, ITERATIONS, N)
    fig.savefig("graphs/Probability extension")
    fig.show()

if __name__ == '__main__':
    main()





