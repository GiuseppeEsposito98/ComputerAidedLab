import random
import numpy as np 
from math import factorial,log10,sqrt, log, cos, sin
from scipy.stats import norm, rice
from statistics import mean, variance
import matplotlib.pyplot as plt

def convolution(n, p):
    '''
    We can use this because the binomial is the sum of N bernoulli distribution
    '''
    counter = 0
    for _ in range(n):
        u = random.uniform(0,1)
        if u < p:
            counter = counter + 1
    return counter

def inverse_transform(n,p):
    '''
    This is feasible for low values of n and p since the 
    computational cost depends on the complexity of the inverse function
    '''
    factorialN = dict()
    for i in range(n+1):
        factorialN[i] = factorial(i)
    fx = list()
    summ = 0
    for i in range(n+1):
        '''
         in order to reduce the computational cost we tried to compute the logarithm of the pdf
         so that the multiplications are transformed in sums and in the end compute the exponential
        ''' 
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

def normal_acceptance_rejection(k, a = -8, b = 8, c = 10**-100, mu=0, sigma=1):
    list_ = list()
    for _ in range(k):
        # a, b and c defines the are of the rectangle of possible randomly generated values
        xi = random.uniform(a,b)    
        yi = random.uniform(0,c)
        z =  norm(mu, sigma).pdf(xi)
        if yi < z: 
        # check if the randomly generated value yi is below the curve so in the acceptance area
            list_.append(xi)
    return list_


def poisson(a):
    '''
    is a discrete probability distribution that expresses the probabilities for the number of events that occur successively 
    and independently in a given time interval, knowing that on average a lambda number of events occur.
    '''
    n = 0
    q = 1
    while True:
        u = random.uniform(0,1)
        q = q*u
        if q < np.exp(-a):
            return n
        else:
            n = n+1
    

def chi_square(n):
    '''
    By definition it is the sum of n random variables distributed as a standard normal
    '''
    normals = normal_acceptance_rejection(k = n)
    for i in range(len(normals)):
        normals[i] = normals[i]**2
    return sum(normals)

def rice_(ni, sigma, k):
    '''
    The rice distribution (which generalizes the Rayleight distribution) describes the distance of a point P from Q
    The parameters of this distribution are (ni, sigma_squared) where ni is the distance of Q from the origin and sigma_squared is the 
    variance of the distributions from which p and x are extracted.
    '''
    out = list()
    for _ in range(k):
        p = poisson(ni**2/(2*sigma**2))
        x = chi_square(2*p+2)
        out.append(sigma*np.sqrt(x))
    return out