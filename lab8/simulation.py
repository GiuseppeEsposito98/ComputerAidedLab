import random
import numpy as np
import pandas as pd
import scipy.stats as st
from math import sqrt
import matplotlib.pyplot as plt
N = 366





def confidence_interval_avg(vector: list):
    conf_int = st.t.interval(alpha=.025, df=len(vector)-1, loc=sum(vector)/len(vector), scale=np.var(vector))
    return conf_int


def expected_value(n: int,
                    probabilities: list,
                     distribution = "uniform"):
    '''
    Compute the average minimum number of extractions such that a conflict occurs with probability 0.5
    '''
    # 366 keys because there is also 29 of february
    possible_choices = range(1,n+1)
    counter = 0
    days = dict.fromkeys(range(1,n+1), 0) 
    while True: 
        counter = counter + 1
        if distribution == "uniform":
            entrance_bd = random.randint(1,n)
        elif distribution == "real":
            entrance_bd = np.random.choice(possible_choices, p=probabilities)
        days[entrance_bd] = days[entrance_bd] + 1
        # if a conflict has occurred
        if days[entrance_bd] == 2:
            return counter 

def probability(n: int,
                probabilities: list,
                m: int,
                iterations: int,
                distribution= "uniform"):
    '''
    Compute, for each m, the probability that at least one conflict occurs
    '''
    possible_choices = range(1,n+1)
    counter = 0
    for _ in range(iterations):
        birthdays = set()
        for __ in range(m):
            if distribution == "uniform":
                birthday = np.random.randint(1,n)
            elif distribution == "real":
                birthday = np.random.choice(possible_choices, p=probabilities)
            # if there was at least a conflict
            if birthday in birthdays: 
                counter += 1
                break
            else:
                birthdays.add(birthday)
    p = counter / iterations # check this 1000
    return p

def confidence_interval_prob(probs:list, iterations: int): 
    '''
    Compute the consifence interval for the probability of conflict.
    '''
    #mean = statistics.mean(values)
    upper_bound = list()
    lower_bound = list()

    #guardando pag 31 di slide 09
    _ppf = st.norm(0,1).ppf(0.95)
    for p in probs:
        s_cappellino = sqrt(p*(1-p)/iterations)
        offset = s_cappellino*_ppf
        upper_bound.append(p+offset)
        lower_bound.append(p-offset)
    return lower_bound,upper_bound

def plot_prob(ax,
                probs: list,
                M: list, 
                theor_values: list,
                distr: str,
                iterations: int):
    '''
    Plot probabilities with respect to M and corresponding confidence interval
    '''
    probs = np.array(probs)
    ax.plot(M,probs, label=f'{distr}')
    lower_bound, upper_bound = confidence_interval_prob(probs, iterations)
    ax.plot(M, theor_values, label = "theor")
    ax.fill_between(M,lower_bound,upper_bound,alpha=.3, label = "confidence_inte")
    ax.set_xlabel("M (number of students per class)")
    ax.set_ylabel("Probabilities")
    ax.set_xticks(np.arange(min(M), max(M)+1, 10.0))
    ax.set_title(f'graphs/conflict_probabilities_{distr}_distribution-VS-class_size')
    ax.legend()
    ax.grid()

def plot_avgs(N: list,
                m_list: list,
                theor_values: float):
    '''
    Plot average minimum number of extractions with respect to possible extraction
    '''
    list_ = list()
    for i in range(len(m_list)):
        list_.append(np.mean(m_list[i]))
    arr = np.array(list_)
    fig, ax = plt.subplots(1,1)
    ax.plot(N, arr, label='avgs', marker = ".")
    ax.plot(N, theor_values, color = 'r', label = "theor", marker = ".")
    lower_bound, upper_bound = list(), list()
    for i in range(len(m_list)):
        ci = st.t.interval(alpha = 0.05, df = len(m_list)-1, loc = np.mean(m_list[i]), scale = np.var(m_list[i]))
        lower_bound.append(ci[0])
        upper_bound.append(ci[1])
    ax.fill_between(N,arr-lower_bound,arr+upper_bound,alpha=.3, label = "confidence_interval")
    ax.set_xlabel("N (number of possible extractions)")
    ax.set_ylabel("Average Minimum number of extractions")
    fig.suptitle(f'POSSIBLE_EXTRACTIONS VS AVERAGE_FIRST_COLLISIONS')
    ax.grid()
    ax.legend()
    fig.savefig(f'graphs/AVERAGE_FIRST_COLLISIONS VS POSSIBLE_EXTRACTIONS')
    fig.show()

def plot_prob_var(ax,
                all_p: list,
                M: list, 
                all_theor: list,
                iterations: int):
    '''
    Plot probabilities with respect to M and corresponding confidence interval for each n
    '''
    for probs, theor_values in zip(all_p, all_theor):
        ax.plot(M,probs)
        lower_bound, upper_bound = confidence_interval_prob(probs, iterations)
        ax.plot(M, theor_values, label = "theor")
        ax.fill_between(M,lower_bound,upper_bound,alpha=.3, label = "confidence_inte")
    ax.set_xlabel("M (number of students per class)")
    ax.set_ylabel("Probabilities")
    ax.set_xticks(np.arange(min(M), max(M)+1, 10.0))
    ax.set_title(f'PROBABILITY VARIATION')
    ax.legend()
    ax.grid()

def from_data_to_probs(filename):
    '''
    Format the dataset to extract probabilities and save it into a csv
    '''
    df = pd.read_csv(f"births_distribution/{filename}")

    # favourable cases
    grouped = df.groupby(["month", "date_of_month"])
    total_per_date = grouped.sum()


    # possible events
    total = total_per_date["births"].sum()

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


