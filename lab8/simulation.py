import random
import numpy as np
import pandas as pd
import scipy.stats as st
from math import sqrt
import matplotlib.pyplot as plt





def confidence_interval_avg(vector: list, alpha = 0.05):
    '''confidence interval for the averages. The averages are distributed as t-student'''
    conf_int = st.t.interval(alpha=alpha, df=len(vector)-1, loc=sum(vector)/len(vector), scale=np.var(vector))
    return conf_int


def expected_value(n: int,
                    probabilities = None,
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
                m: int,
                iterations: int,
                probabilities = None,
                distribution = "uniform"):
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

def confidence_interval_prob(probs:list, iterations: int, alpha = 0.05): 
    '''
    Compute the confidence interval for the probability of conflict. The probabilities are instances of a binomial
    random variable so we can use the estimate of the standard deviation and the gaussian quantile to compute the 
    confidence interval 
    '''

    upper_bound = list()
    lower_bound = list()

    ppf_ = st.norm(0,1).ppf(alpha)
    for p in probs:
        s_hat = sqrt(p*(1-p)/iterations)
        offset = s_hat*ppf_
        upper_bound.append(p+offset)
        lower_bound.append(p-offset)
    return lower_bound,upper_bound

def plot_prob(ax,
                probs: list,
                M: list, 
                theor_values: list,
                distr: str,
                iterations: int,
                alpha = 0.05):
    '''
    Plot probabilities with respect to M and corresponding confidence interval
    '''
    probs = np.array(probs)
    ax.plot(M,probs, label= 'experimental')
    lower_bound, upper_bound = confidence_interval_prob(probs, iterations, alpha=alpha)
    ax.plot(M, theor_values, label = "theoretical curve")
    ax.fill_between(M,lower_bound,upper_bound,alpha=.3, label = "confidence interval 95%")
    ax.set_xlabel("M (number of students per class)")
    ax.set_ylabel("Probabilities")
    ax.set_xticks(np.arange(min(M), max(M)+1, 10.0))
    ax.set_title(f'{distr} distribution')
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
    ax.plot(N, arr, label='averages', marker = ".")
    ax.plot(N, theor_values, color = 'r', label = "theoretical curve", marker = ".")
    lower_bound, upper_bound = list(), list()
    for i in range(len(m_list)):
        ci = st.t.interval(alpha = 0.05, df = len(m_list)-1, loc = np.mean(m_list[i]), scale = np.var(m_list[i]))
        lower_bound.append(ci[0])
        upper_bound.append(ci[1])
    ax.fill_between(N,arr-lower_bound,arr+upper_bound,alpha=.3, label = "confidence interval 97%")
    ax.set_xlabel("N (number of possible extractions)")
    ax.set_ylabel("Average Minimum number of extractions")
    fig.suptitle(f'POSSIBLE EXTRACTIONS VS AVERAGE FIRST COLLISIONS')
    ax.grid()
    ax.legend()
    fig.savefig(f'graphs/POSSIBLE EXTRACTIONS VS AVERAGE FIRST COLLISIONS')
    fig.show()

def plot_prob_var(ax,
                all_p: list,
                M: list, 
                all_theor: list,
                iterations: int,
                N: list):
    '''
    Plot probabilities with respect to M and corresponding confidence interval for each n
    '''
    for probs, theor_values, n in zip(all_p, all_theor, N):
        ax.plot(M,probs, label= f"probabilities for N = {n}")
        lower_bound, upper_bound = confidence_interval_prob(probs, iterations)
        ax.plot(M, theor_values, label = f"theorerical value for N = {n}")
        ax.fill_between(M,lower_bound,upper_bound,alpha=.3, label = f"confidence interval 95% for N = {n}")
    ax.set_xlabel("M (number of elements)")
    ax.set_ylabel("Probabilities")
    ax.set_xticks(np.arange(min(M), max(M)+1, 10.0))
    ax.set_title(f'Number of elements VS Conflict probabilities')
    ax.legend(fontsize = 'xx-small')
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
    
    fig, ax = plt.subplots(1, 1, figsize = (13,7))
    fig.suptitle("Probability istogram")
    plt.bar(range(0,366), probabilities.values)
    ax.set_xlabel("Day in a year")
    ax.set_ylabel("Probabilities")
    ax.set_xticks(np.arange(0, 366, 20.0))
    #ax.set_title(f'Number of possible extractions VS Conflict probabilities')
    ax.legend()
    ax.grid()
    fig.savefig("graphs/Probability distribution")
    fig.show()


    with open("births_distribution/probabilities.csv", "w") as csf:
        header = "mm/dd,probabilities\n"
        csf.write(header)


    with open("births_distribution/probabilities.csv", "a") as csf:
        for k,v in zip(probabilities.index, probabilities):
            csf.write(f"{k[0]}/{k[1]},{v}\n")


