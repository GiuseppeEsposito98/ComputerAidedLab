import numpy as np
import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def expected_value_uniform(num_itr, n,p=0.5):
    print("===== EXPECTED VALUE - UNIFORM =====")
    Em = []
    for _ in range(num_itr):
        year = np.zeros(n)
        m = 0
        while True:
            i = random.randint(0, n-1)
            if int(year[i]) == 1:
                #print(f"iteration: {i} - m: {m}")
                Em.append(m)
                break
            else:
                year[i] += 1
            m += 1
    print(f"E[m] = {sum(Em)/len(Em)}")
    print(f"Theoretical E[m]: {np.sqrt(2*n*np.log(1/(1-p)))}")

def expected_value_real(num_itr, n, cdf_probs, p=0.5):
    print("===== EXPECTED VALUE - REAL DISTRIBUTION =====")
    Em = []
    for _ in range(num_itr):
        year = np.zeros(n)
        m = 0
        x = 0
        while True:
            i = random.randint(0, n-1)
            for j in range(len(cdf_probs)-1):
                if i>cdf_probs[j] and i<=cdf_probs[j+1]:
                    x = j+1
            if int(year[x]) == 1:
                Em.append(m)
                break
            else:
                year[x] += 1
            m += 1
    print(f"E[m] = {sum(Em)/len(Em)}")
    print(f"Theoretical E[m]: {np.sqrt(2*n*np.log(1/(1-p)))}")

def probability_uniform(num_itr, mm, n):
    print("===== PROBABILITY - UNIFORM =====")
    probs = {}
    # probs['th'] = {}
    tmp_list = []
    # for m in mm:
    #     probs['th'][m] = 1- np.exp(-(m**2)/(2*n))
    for i in range(num_itr):
        probs[i] = {}
        for m in mm:
            conflict = 0
            year = np.zeros(n)
            for k in range(m):
                j = random.randint(0, n-1)
                if int(year[j]) == 1:
                    #conflict = k
                    conflict +=1
                else:
                    year[j] += 1
            probs[i][m] = conflict/m
            tmp_list.append(probs[i][m])
    M = []
    for _ in range(num_itr):
        for i in range(len(mm)):
            M.append(mm[i])

    df = pd.DataFrame([M, tmp_list])
    df = df.transpose()

    fig, ax = plt.subplots(figsize=(20, 10), nrows=1)

    sns.lineplot(
            ax=ax,
            x=df.iloc[:, 0],
            y=df.iloc[:, 1],
            data=df,
            errorbar="ci",
            linewidth=1.5
    )

    ax.set_title("Probabilities of conflict and confidence interval", fontweight = "bold")
    ax.set_xlabel("m")
    ax.set_ylabel("95% CI")
    ax.grid()
    plt.show()

def probability_real(num_itr, mm, n, cdf_probs):
    print("===== PROBABILITY - REAL DISTRIBUTION =====")
    probs = {}
    # probs['th'] = {}
    tmp_list = []
    # for m in mm:
    #     probs['th'][m] = 1- np.exp(-(m**2)/(2*n))
    for i in range(num_itr):
        probs[i] = {}
        for m in mm:
            conflict = 0
            year = np.zeros(n)
            x = 0
            for k in range(m):
                j = random.randint(0, n-1)
                for l in range(len(cdf_probs)-1):
                    if j>cdf_probs[l] and j<=cdf_probs[l+1]:
                        x = l+1
                if int(year[x]) == 1:
                    conflict +=1
                else:
                    year[x] += 1
            probs[i][m] = conflict/m
            tmp_list.append(probs[i][m])

    M = []
    for _ in range(num_itr):
        for i in range(len(mm)):
            M.append(mm[i])
    
    df = pd.DataFrame([M, tmp_list])
    df = df.transpose()

    fig, ax = plt.subplots(figsize=(20, 10), nrows=1)

    sns.lineplot(
            ax=ax,
            x=df.iloc[:, 0],
            y=df.iloc[:, 1],
            data=df,
            errorbar="ci",
            linewidth=1.5
    )

    ax.set_title("Probabilities of conflict and confidence interval", fontweight = "bold")
    ax.set_xlabel("m")
    ax.set_ylabel("95% CI")
    ax.grid()
    plt.show()


def real_values_import(filename, year):
    birth = pd.read_csv(filename)
    probs_birth = {}
    for i in range(2000,2014+1):
        df = birth[birth['year']==i]
        num_birth_year = sum(df['births'])
        tmp = df["births"].tolist()
        pb = np.zeros(len(tmp))
        for j in range(len(tmp)):
            pb[j] = tmp[j]/num_birth_year
        probs_birth[i] = pb
    return(probs_birth[year])

def cdf(real_probs):
    cdf_probs = np.zeros(len(real_probs))
    for i in range(len(real_probs)):
        cdf_probs[i] = real_probs[:i].sum()
    return cdf_probs

cdfs = list()
for year in range(2000, 2015):
    cdfs.append(cdf(real_values_import("births_distribution/US_births_2000-2014_SSA.csv", year)))

for cdf in cdfs:
    if len(cdf) == 365:
        for i in range(365):
            cdf[i]