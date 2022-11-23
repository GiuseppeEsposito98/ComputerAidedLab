import numpy as np
from scipy.stats import norm, t
import matplotlib.pyplot as plt

np.random.seed(30179)
class Client:
    def __init__(self,
    typ: str,
    arrival_time: int,
    id_client: int) :
        self.typ = typ
        self.arrival_time= arrival_time
        self.id_client = id_client
        self.delay_time = 0


    def __str__(self) -> str:
        return f"id: {self.id_client}"

    def set_(self, status: str):
        self.typ = status

class Event():
    def __init__(self, time, typ) -> None:
        self.time = time
        self.typ = typ
        self.client = Client("arrival", 0, 0)

    def assignClient(self, client:Client):
        self.client = client
    def __str__(self):
        return f"time = {self.time}, type = {self.typ}, client: {self.client.id_client}"

    def __lt__(self, other):
        return self.time < other.time

def cum_mean(arr):
    '''
    This function compute the cumulative mean weighted on the number of events. The structure of the resulting array is
    the following:
    [
        cum_mean_1 = delay1 / 1,
        cum_mean_2 = (delay1 + delay2) / 2,
        ...
        cum_mean_n =() delay1 + delay2 + delay3 + ... + delay_n) / total_number_of_departure
    ]
    '''
    cum_sum = np.cumsum(arr,axis=0)
    for i in range(cum_sum.shape[0]):
        if i == 0:
            continue
        cum_sum[i] = cum_sum[i]/(i+1)
    return cum_sum

def remove_transient(arr, u, distribution):
    '''
    Given a signal, this function detects the transient and then it returns the index of the signal 
    after which the warm-up transient is removed and then returns also the signal cut in than point.
    To remove the transient I decided to consider the gap between the min and the max value over
    the current window, so if their ratio min/max is over a threshold it means that they are too far
    from eachother and then we still are in the transient. 
    '''
    # compute the desired len window with respect to the utilization
    len_window = int(u*1500)
    # compute consequently the number of window
    num_windows = int(len(arr)/len_window)
    # adapt the threshold with respect of u (this will represent the accuracy level)
    if distribution=='deterministic_process' or distribution=='exponential':
        thr = 0.95
    else:
        thr = 0.90
    for i in range(num_windows):
        # check whether the considered index of the signal is not out of bounf
        if i*len_window >= len(arr):
            break
        else:
            # consider winfow per winfow
            window = arr[i*len_window: (i+1)*len_window]
            if window != []:
                # compute max and min over that window
                min1, max1 = min(window), max(window)
                # i computed it as the ratio and not the difference in order to normalize with respect to
                # the height of the window on the graph 
                normalized_gap = min1/max1
            if normalized_gap > thr:
                arr = arr[(i+1)*len_window:]
                return arr, len_window*(i+1)

def find_batches(arr, u, initial_n = 10, confidence=.95):
    '''
    Given a function where the transient is removed this function finds the correct number of batches in which
    the remaining function must be devided to apply the batch means algorithm.
    '''
    arr = np.array(arr)
    while True:
        batches = np.array_split(arr, initial_n)
        for batch in batches: # ma questo non lo fa solo una volta?
            # compute the mean over the current batch 
            x = np.mean(batch)
            # compute the confidence interval with confidence level at 95%
            confidence_interval = t.interval(confidence = confidence, df= len(batches)-1, loc = x, scale = np.std(batch))
            z = confidence_interval[1] - x
            # if the confidence is not small enough with respect to a given value 
            if (2*z/x) > u*0.4: # accuracy
                # collect another batch
                initial_n += 1
                break
            # if the interval is small enough
            else: 
                print(f'for u: {u} corresponding n: {initial_n}')
                return initial_n

def batch_means(arr, correct_num_batches, confidence=.95):
    '''
    Given the correct number of bins computed in find_batches() the confidence interval can be then computed 
    taking as reference the t-student distribution and also the meaan for each batch.
    '''
    means = list()
    ci_lower = list()
    ci_upper = list()
    # cast to numpy array 
    arr = np.array(arr)
    # split the delay array without warm-up transient in batches
    batches = np.array_split(arr, correct_num_batches)
    for batch in batches:
        # compute the mean over the current batch
        x = np.mean(batch)
        # compute the confidence interval
        ci = t.interval(confidence, len(batches)-1, x, np.std(batch))
        # save bounds of confidence inteval
        ci_lower.append(ci[0])
        ci_upper.append(ci[1])
        means.append(x)
    
    return means, ci_lower, ci_upper

def generate_hyperexponential():
    '''
    Generate numbers from an hyperexponential distribution
    '''
    # this value is to garantee the same probability to choose the l1 or l2
    p = 0.5 
    lam1 = 1/6 
    lam2 = 1/8 
    u = np.random.uniform(0,1)
    if u <= p:
        service = np.random.exponential(1/lam1)
    else:
        service = np.random.exponential(1/lam2)
     # actually it should be 1/scale
    return service


def plot_metric(fig,
                ax,
                list_per_event: list,
                label: str,
                marker: str = None,
                log_scale: bool = False
                ):
    
    '''
    This function plot a generic array of delays with standard functions of matplotlib.pyplot when a confidence interval 
    is not requested
    '''
    ax.plot(list_per_event, label = label, marker = marker)
    ax.set_xlabel('Event')
    ax.set_ylabel('Delays')
    ax.grid(True)
    if log_scale:
        ax.xscale("log")
        ax.yscale("log")
    ax.legend()


def plot_metric_with_ci(ax,
                list_per_event: list,
                label: str,
                ci_lower: list,
                ci_upper: list,
                marker: str = None,
                log_scale: bool = False
                ):
    '''
        This function plot a generic array of delays with standard functions of matplotlib.pyplot
        when a confidence interval is requested
    '''
    ax.plot(list_per_event, label = label, marker = marker)
    ax.set_xlabel('Event')
    ax.set_ylabel('Delays')
    ax.grid(True)
    # plot confidence interval
    ax.fill_between([x for x in range(len(list_per_event))], ci_lower, ci_upper, alpha = .5)
    if log_scale:
        ax.xscale("log")
        ax.yscale("log")
    ax.legend()


def generate_arrival_time(frequency : float) -> float:
    """
    This function returns an exponential arrival time
    """
    return np.random.exponential(frequency)

def generate_service_time(lam : float) -> float:
    """
    This function returns an exponential service time
    """
    return np.random.exponential(1/lam)

def generate_exponential_service_time() -> float:
    """
    This function return an exponential service time according to the problem's specifications.
    """
    return generate_service_time(1)
