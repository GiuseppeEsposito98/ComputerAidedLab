import random
import numpy as np 
from math import factorial,log10,log
from scipy.stats import norm
from statistics import mean
import matplotlib.pyplot as plt

from time import time
np.random.seed(42)
random.seed(42)
def convolution(n, p):
    counter = 0
    for _ in range(n):
        u = random.uniform(0,1)
        if u < p:
            counter = counter + 1
    return counter

def inverse_transform(n,p):
    factorialN = dict()
    for i in range(n+1):
        factorialN[i] = factorial(i)
    fx = list()
    summ = 0
    for i in range(n+1):
        pi = (log10(factorialN[len(factorialN)-1])-(log10(factorialN[i])+log10(factorialN[n-i])))+i*log10(p)+(n-i)*log10(1-p)
        summ += 10**pi 
        fx.append(summ)
    u = random.uniform(0,1)
    for i in fx:
        if u < i:
            if fx.index(i) == 0:
                return 0
            else:
                return fx.index(i)-1

def method3 (n, p):
    m = 1
    q = 0
    while q < n: 
        u = random.uniform(0,1)
        g_m = np.ceil((log10(u))/(log10(1-p)))
        q = q + g_m 
        m = m + 1
    return m+1

def normal(a, b, c, k):
    list_ = list()
    for i in range(k):
        xi = random.uniform(a,b)    
        yi = random.uniform(0,c)
        z =  norm(0, 1).pdf(xi)
        if yi < z:
            list_.append(xi)
    return list_


def main():
    vals = []
    cases = [(10, 0.5), (100, 0.01)]#, (10**6, 10**(-5))]
    for case in cases:
        start1 = time()
        convolution(case[0], case[1])
        end1 = time()
        print(f"Execution time (convolution): {end1-start1}")
        start2 = time()
        vals.append(inverse_transform(case[0], case[1]))
        end2 = time()
        print(f"Execution time (inverse transform): {end2-start2}")
        start3 = time()
        method3(case[0], case[1])
        end3 = time()
        print(f"Execution time (method 3): {end3-start3}")
    start4 = time()
    values, z = normal(-8,8,10**-100, k = 10000)
    end4 = time()
    values.sort()
    xValueN = normal(-8,8,10**-100, k = 10000)
    empiricalMean = mean(xValueN)
    xValueN.sort()
    z = [norm(0,1).pdf(val) for val in xValueN]
    print(z)
    plt.plot(xValueN,z)
    plt.title('Arena 10x10', fontsize=14)
    plt.xlabel('Number of Players')
    plt.ylabel('Time to win')
    plt.grid(True)
    plt.show()




main()