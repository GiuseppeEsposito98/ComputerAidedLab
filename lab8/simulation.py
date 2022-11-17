import random
import numpy as np
import pandas as pd
import scipy.stats as st
from math import sqrt
import matplotlib.pyplot as plt
N = 366


possible_choices = range(1,N+1)



def expected_value(probabilities: list,
                     distribution = "uniform"):
    '''
    Compute the average minimum number of extractions such that a conflict occurs with probability 0.5
    '''
    # 366 keys because there is also 29 of february
    counter = 0
    days = dict.fromkeys(range(1,N+1), 0) 
    while True: 
        counter = counter + 1
        if distribution == "uniform":
            entrance_bd = random.randint(1,N)
        elif distribution == "real":
            entrance_bd = np.random.choice(possible_choices, p=probabilities)
        days[entrance_bd] = days[entrance_bd] + 1
        # if a conflict has occurred
        if days[entrance_bd] == 2:
            return counter 

def probability(probabilities: list,
                m: int,
                distribution= "uniform"):
    '''
    Compute, for each m, the probability that at least one conflict occurs
    '''
    counter = 0
    for _ in range(1000):
        if distribution == "uniform":
            birthdays = np.random.randint(1,N, m)
        elif distribution == "real":
            birthdays = np.random.choice(possible_choices, p=probabilities, size=m)
        unique_birthdays = set(birthdays)
        coincidence = (len(unique_birthdays) !=len(birthdays))
        # if there was at least a conflict
        if coincidence: 
            counter += 1
    p = counter / 1000 # check this 1000
    return p

def confidence_interval(probs:list): 
    '''
    Compute the consifence interval for the probability of conflict.
    '''
    #mean = statistics.mean(values)
    upper_bound = list()
    lower_bound = list()

    #guardando pag 31 di slide 09
    _ppf = st.norm(0,1).ppf(0.95)
    for p in probs:
        s_cappellino = sqrt(p*(1-p)/len(probs))
        offset = s_cappellino*_ppf
        upper_bound.append(p+offset)
        lower_bound.append(p-offset)
    return lower_bound,upper_bound

def plot_prob(probs: list,
                M: list, 
                theor_values: list,
                distr: str):
    '''
    Plot probabilities with respect to M and corresponding confidence interval
    '''
    probs = np.array(probs)
    plt.plot(M,probs, label=f'{distr}')
    lower_bound, upper_bound = confidence_interval(probs)
    plt.plot(M, theor_values, label = "theor")
    plt.fill_between(M,lower_bound,upper_bound,alpha=.3)
    plt.grid()
    plt.legend()
    plt.savefig(f'graphs/{distr}_distribution.png')
    plt.show()

def plot_avgs(first_collisions: list,
                theor_avg: float,
                iteration: int,
                label_: str):
    '''
    Plot average minimum number of extractions with respect to number of iterations
    '''
    plt.plot(first_collisions, label='avg_min')
    plt.axhline(y = theor_avg, color = 'r', linestyle = '-', label = "theor")
    plt.grid()
    plt.legend()
    plt.savefig(f'graphs/{label_}_AVG-VS-ITERATIONS.png')
    plt.show()

def from_data_to_probs(filename):
    df = pd.read_csv(f"births_distribution/{filename}")

    # favourable cases
    grouped = df.groupby(["month", "date_of_month"])
    total_per_date = grouped.sum()


    # possible events
    total = total_per_date["births"].sum()
    print(total)

    # frequentist probability
    probabilities = total_per_date["births"].apply(lambda x: x/total)
    #print(probabilities)


    with open("births_distribution/probabilities.csv", "w") as csf:
        header = "mm/dd,probabilities\n"
        csf.write(header)


    with open("births_distribution/probabilities.csv", "a") as csf:
        for k,v in zip(probabilities.index, probabilities):
            csf.write(f"{k[0]}/{k[1]},{v}\n")


# - we neglect gap years (i.e. n=365)
# - the distrbution of birthdays is taken as to be unifom at first and then from real statistics
# - we use the Taylor-based linear approximation e^(-ax)=1-ax, accurate for small values of x
# - to compute the avarage number of people to have a conflict, we run K1 times a simulation that "generates" birthdays until I have a
#   conflict, then take the avarages of this simulations
# - to compute the probability of having a conflict over m birthdays, we extract m<=n elements with repetition from the birthday distribution
#   and check whether a conflict was found; for each m we repeat the simulation K2 times and define the empirical probability of having a
#   conflict over m people to be the avarage of the K2 results

# - try to use approximations different from the Taylor-based one