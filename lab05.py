import random
from matplotlib.font_manager import X11FontDirectories
import numpy as np 
from math import factorial,log10,sqrt, log, cos, sin
from scipy.stats import norm, rice
from statistics import mean, variance
import matplotlib.pyplot as plt

from time import time

from sklearn.covariance import empirical_covariance
np.random.seed(42)
random.seed(42)
def convolution(n, p):
    '''
    We can use this because the binomial is the sum of N bernoully distribution
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
        # in order to reduce the computational cost we tried to compute the logarithm of the pdf
        # so that the multiplications are transformed in sums and in the end compute the exponential 
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
    for i in range(k):
        # a, b and c defines the are of the rectangle of possible randomly generated values
        xi = random.uniform(a,b)    
        yi = random.uniform(0,c)
        z =  norm(mu, sigma).pdf(xi)
        if yi < z: 
        # check if the randomly generated value yi is below the curve so in the acceptance area
            list_.append(xi)
    return list_

def normal_polar_coordinates(mu, sigma):
    '''
    This method allows us to exploit the polar coordinates to generate a pair 
    which represents the coordinate of a point in the eucledian space
    '''
    u = random.uniform(0,1)
    v = random.uniform(0,1)
    b = sqrt(-2*(log(u)))
    theta = 2*np.pi*v
    z1 = b * cos(theta)
    z2 = b * sin(theta)
    # here we pass from the coordinates generated from a normal standard distribution to a normal one.
    x1 = mu + (sigma * z1)
    x2 = mu + (sigma * z2)
    return x1, x2


def poisson(a):
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


def main():
    vals = []
    # for n = 10**6 and p = 10**-5 i wasn't able to find any algorithm that has less computational cost.
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
    '''
    The lim for x that tends to infinit of the pdf, tends to zero, this means that we have to truncate the pdf in [a,b].
    Then as c (height of the rectangle of possible generations from uniform distribution) tends to zero the probability to generate a number that lies in the 
    acceptance region increases.
    In the end of course the more numbers we generate, the higher is the probability to compute an empirical average that is close to the 
    theoretical one as proof of the low of large numbers
    '''
    # pdf line graph
    values= normal_acceptance_rejection(a = -8, b = 8, c = 10**-100, k = 10000, mu = 0, sigma = 1)
    values.sort()
    z = [norm(0,1).pdf(val) for val in values]
    print(z)
    plt.plot(values,z)
    plt.title('Normal distribution of generated points', fontsize=14)
    plt.xlabel('x')
    plt.ylabel('pdf(x)')
    plt.grid(True)
    plt.show()

    # pdf bar graph
    plt.bar(values, z, color ='blue', width = 0.4)
    plt.title('Normal distribution of generated points', fontsize=14)
    plt.xlabel('x')
    plt.ylabel('pdf(x)')
    plt.grid(True)
    plt.show()

    # cumulant line graph
    cdf = np.cumsum(z)
    plt.plot(values, cdf, label="CDF")
    plt.title('Cumulant normal distribution of generated points', fontsize=14)
    plt.xlabel('x')
    plt.ylabel('cdf(x)')
    plt.grid(True)
    plt.show()

    empirical_mean = mean(values)
    empirical_variance = variance(values)**2
    print(f"empirical mean: {empirical_mean}")
    print(f"empirical variance: {empirical_variance}")

    rices_generations = rice_(1,2, 1000)
    rices_generations.sort()

    # pdf bar graph
    print(rice.pdf(rices_generations, 0.6))
    pdf_rice = rice.pdf(rices_generations, 2)
    #plt.plot(rices_generations, pdf_rice, label="PDF")
    plt.bar(rices_generations, pdf_rice, color ='blue', width = 0.4)
    plt.title('Rice distribution of generated points', fontsize=14)
    plt.xlabel('x')
    plt.ylabel('pdf(x)')
    plt.grid(True)
    plt.show()

main()