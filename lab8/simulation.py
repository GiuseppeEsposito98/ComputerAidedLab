import random
import numpy as np
import pandas as pd

probabilities = pd.read_csv("probabilities.csv")
# probabilities of the real distribution for each date
print(probabilities["probabilities"])


def simulation1(m, distribution = "uniform"):
    # 366 keys because there is also 29 of february
    days = dict.fromkeys(range(1,367), 0) 
    for i in range(m):
        if distribution == "uniform":
            entrance_bd = random.randint(0,366)
        elif distribution == "real":
            entrance_bd = np.random.choice(range(1,367), p=probabilities["probabilities"].tolist())
        days[entrance_bd] = days[entrance_bd] + 1
        if days[entrance_bd] == 2:
            print(f"for m: {m} we got: {max(days.values())}, in position: {entrance_bd}")
            return i
    print(f"for m: {m} i'm returning 0")
    return 0


# - we neglect gap years (i.e. n=365)
# - the distrbution of birthdays is taken as to be unifom at first and then from real statistics
# - we use the Taylor-based linear approximation e^(-ax)=1-ax, accurate for small values of x
# - to compute the avarage number of people to have a conflict, we run K1 times a simulation that "generates" birthdays until I have a
#   conflict, then take the avarages of this simulations
# - to compute the probability of having a conflict over m birthdays, we extract m<=n elements with repetition from the birthday distribution
#   and check whether a conflict was found; for each m we repeat the simulation K2 times and define the empirical probability of having a
#   conflict over m people to be the avarage of the K2 results

# num_successes = 0
# birthdays = empty_set
# for iteration = 1:K2
#     for i = 1:m
#         birthday = extract_birthday
#         if birthday in birthdays
#             success ++
#         else
#             birthdays.add(birthday)
# p_conflict[m] = success/K2

      

# 6 - possible extensions

# - try to use approximations different from the Taylor-based one