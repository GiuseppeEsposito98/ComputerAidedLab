import random
from math import exp
import numpy as np
from simulation import *

random.seed(423)
np.random.seed(423)

def main():
    filename = "US_births_2000-2014_SSA.csv"
    from_data_to_probs(filename)
    # input parameters
    M = [10,20,30,40,50,60,70,80,90]
    ITERATIONS = 100
    N = 366
    # a possible extension could be to evaluate, for each value of M the avg number of first_collisions
    # probabilities of the real distribution for each date
    probabilities = pd.read_csv(f"births_distribution/probabilities.csv")["probabilities"].tolist()

    # Average minimum number such that a conflict occurs - uniform distribution
    first_collisions_unif = list()
    for _ in range(ITERATIONS):
        first_collisions_unif.append(expected_value(probabilities, distribution="uniform"))
    avg = sum(first_collisions_unif)/len(first_collisions_unif)

    theoretical_avg = 1.25*sqrt(N)
    plot_avgs(first_collisions_unif, theoretical_avg, ITERATIONS, "uniform")

    print(f"UNIFORM DISTRIBUTION - experimental value: {avg}, expected value: {theoretical_avg}")

    # Average minimum number such that a conflict occurs - real distribution
    first_collisions_real = list()
    for _ in range(ITERATIONS):
        first_collisions_real.append(expected_value(probabilities, distribution="real"))
    avg = sum(first_collisions_real)/len(first_collisions_real)
    plot_avgs(first_collisions_real, theoretical_avg, ITERATIONS, "real")

    print(f"REAL DISTRIBUTION - experimental value: {avg}, expected value: {theoretical_avg}")

    # M VS Probability of conflict - uniform distribution
    tmp_unif = list()
    theor_vals = list()
    for m in M:
        theor_vals.append(1-exp(-(m**2)/(2*N)))
        p = probability(probabilities, m, distribution="uniform")
        tmp_unif.append(p)

    plot_prob(tmp_unif, M, theor_vals, "uniform")

    # M VS Probability of conflict - real distribution
    tmp_real = list()
    theor_vals = list()
    for m in M:
        theor_vals.append(1-exp(-(m**2)/(2*N)))
        p = probability(probabilities, m, distribution="real")
        tmp_real.append(p)

    plot_prob(tmp_real, M, theor_vals, "real")


if __name__ == '__main__':
    main()

# ASSUMPTIONS
    
# - we neglect gap years (i.e. n=365)
# - the distrbution of birthdays is taken as to be unifom at first and then from real statistics
# - we use the Taylor-based linear approximation e^(-ax)=1-ax, accurate for small values of x
# - to compute the avarage number of people to have a conflict, we run K1 times a simulation that "generates" birthdays until I have a
#   conflict, then take the avarages of this simulations
# - to compute the probability of having a conflict over m birthdays, we extract m<=n elements with repetition from the birthday distribution
#   and check whether a conflict was found; for each m we repeat the simulation K2 times and define the empirical probability of having a
#   conflict over m people to be the avarage of the K2 results
# - we compare all of our empirical results with the theoretical ones
# - consider also anni bisestili




