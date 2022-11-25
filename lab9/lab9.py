import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, t


def arrival(time, FES, queue_, users, u, id_client, distribution= 'exponential'):
    '''
    This function computes a random instance of time,
    add an even to the FES (Future Event Set),
    add a client to the queue whose label is 'arrival' and whose id is a constantly increasing counter
    '''

    if distribution == 'hyperexponential':
        lam = generate_hyperexponential()
    elif distribution == 'deterministic_process':
        lam = 1
    elif distribution == 'exponential':
        lam=1

    # inter arrival time
    t_ia = np.random.exponential(lam/u)
    e = Event(time +t_ia, "arrival")
    # id_client is used to check whether a specific client has just one arrival and one departure (debugging purposes)
    id_client = id_client + 1 
    client_arr = Client("arrival", time, id_client)
    # i'm taking track of the corresponding client in the event object
    e.assignClient(client_arr)
    FES.append(e)
    # increase the counter of users in the system
    users = users +1
    queue_.append(client_arr)
    # is there is exactly one user in the queue make the server busy
    if(users == 1):
        # the distribution can be either ['hyperexponential', 'uniform']
        if distribution == 'hyperexponential':
            service_time = generate_hyperexponential()
        elif distribution == 'deterministic_process':
            service_time = 1
        elif distribution == 'exponential':
            service_time = np.random.exponential(1)
        client_dep = Client("departure", time+ service_time, id_client)
        e1 = Event(time + service_time, "departure")
        e1.assignClient(client_dep)
        FES.append(e1)
    return users

# Departure function
def departure(time, FES, queue_, users, delays, distribution= 'exponential'):
    # when a user is leaving decrease the user counter
    users = users - 1
    # remove the first client added in the queue (FIFO policy)
    client_dep = queue_.pop(0)
    # delays are time the client just popped from the queue has spent in the queue
    delays.append(time-client_dep.arrival_time)
    # is the queue counter is greater than 0 make the serve busy
    if users > 0:
        # the distribution can be either ['hyperexponential', 'uniform']
        if distribution == 'hyperexponential':
            service_time = generate_hyperexponential()
        elif distribution == 'deterministic_process':
            service_time = 1
        elif distribution == 'exponential':
            service_time = np.random.exponential(1)
        e2 = Event(time + service_time, "departure")
        # set the label of the client just popped to 'departure'
        client_dep.set_("departure")
        e2.assignClient(client_dep)
        FES.append(e2)
    return users, delays


class Client:
    '''
    This class manages the customers entering in the system.
    '''
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
    '''
    This class defines the events that can be either 'arrival' or 'departure' keeping track of the client they are releted
    '''
    def __init__(self, time, typ) -> None:
        self.time = time
        # departure or arrival
        self.typ = typ
        # this is the first client
        self.client = Client("arrival", 0, 0)

    def assignClient(self, client:Client):
        '''
        Assign the corrsponding client to this object
        '''
        self.client = client
    def __str__(self):
        return f"time = {self.time}, type = {self.typ}, client: {self.client.id_client}"

    def __lt__(self, other):
        '''
        This is required to sort the FES
        '''
        return self.time < other.time

def cum_mean(arr):
    '''
    This function compute the cumulative mean weighted on the number of events. The structure of the resulting array is
    the following:
    [
        cum_mean_1 = delay1 / 1,
        cum_mean_2 = (delay1 + delay2) / 2,
        ...
        cum_mean_n =(delay1 + delay2 + delay3 + ... + delay_n) / total_number_of_departure
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
        thr = 0.98
    else:
        thr = 0.90
    for i in range(num_windows):
        # check whether the considered index of the signal is not out of bounf
        if i*len_window >= len(arr):
            break
        else:
            # consider winfow per winfow
            window = arr[i*len_window: (i+1)*len_window]
            if len(window) != 0:
                # compute max and min over that window
                min1, max1 = min(window), max(window)
                # i computed it as the ratio and not the difference in order to normalize with respect to
                # the height of the window on the graph 
                normalized_gap = min1/max1
            if normalized_gap > thr:
                arr = arr[(i+1)*len_window:]
                return arr, len_window*(i+1), thr

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
            if (2*z/x) > u*0.2: 
                # collect another batch
                initial_n += 1
                break
            # if the interval is small enough
            else:
                print(f'Result for batch means algorithm: number of beans = {initial_n}')
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

    return service


def plot_metric(fig,
                ax,
                list_per_event: list,
                label: str,
                marker: str = None,
                log_scale: bool = False,
                x_label = 'Event'
                ):
    
    '''
    This function plot a generic array of delays with standard functions of matplotlib.pyplot when a confidence interval 
    is not requested
    '''
    ax.plot(list_per_event, label = label, marker = marker)
    ax.set_xlabel(x_label)
    ax.set_ylabel('Delays (time unit)')
    ax.grid(True)
    if log_scale:
        ax.xscale("log")
        ax.yscale("log")
    ax.legend()


def plot_metric_with_ci(ax,
                list_per_event: list,
                label_: str,
                ci_lower: list,
                ci_upper: list,
                x_label = 'Event',
                marker: str = None,
                log_scale: bool = False
                ):
    '''
        This function plot a generic array of delays with standard functions of matplotlib.pyplot
        when a confidence interval is requested
    '''
    ax.plot(list_per_event, label = label_, marker = marker)
    ax.set_xlabel(x_label)
    ax.set_ylabel('Delays (time unit)')
    ax.grid(True)
    # plot confidence interval
    ax.fill_between([x for x in range(len(list_per_event))], ci_lower, ci_upper, alpha = .5, label = f'{label_} confidence interval 95%')
    if log_scale:
        ax.xscale("log")
        ax.yscale("log")
    ax.legend()





np.random.seed(30179)
def main():
    # INPUT PARAMETERS
    # utilization is the average amount of work requested to the server from customers arriving in the time unit
    utilizations = [0.1, 0.2, 0.4, 0.7, 0.8, 0.9, 0.95, 0.99]
    confidence = 0.95
    SIM_TIME = 100000
    print('Starting simulation')
    print('=============INPUT PARAMETERS=============')
    print(f'Simulation time: {SIM_TIME}\nconfidence: {confidence}')

    # statistics structures
    mean_exp = list()
    lower_bounds_exp = list()
    upper_bounds_exp = list()  

    mean_hyperexp = list()
    lower_bounds_hyperexp = list()
    upper_bounds_hyperexp = list()  

    mean_det = list()
    lower_bounds_det = list()
    upper_bounds_det = list()   

    # Main loop
    for distribution in ['exponential', 'hyperexponential', 'deterministic_process']:  
        print('Distribution: ', distribution)
        for u in utilizations:
            # Initializations for each value of u and for each distribution type
            id_client = 0
            users = 0
            # list of delays of the clients
            delays = list()
            # list of clients
            queue_ = list()
            FES = list()
            # initial time 
            time = 0.0
            e0 = Event(time,"arrival")
            c0 = Client("arrival", time, id_client)
            # setup the initial values of the lists
            e0.assignClient(c0)
            FES.append(e0)
            queue_.append(c0)

            

            print('utilization level: ', u)
            users = 0

            while time < SIM_TIME:
                # the FES is sorted such that we have a FIFO service policy, so it is sorted with respect to the event with the 
                # least time the event has occurred
                FES.sort()
                event = FES.pop(0)
                # update the current time
                time = event.time
                if(event.typ == "arrival"):
                    users = arrival(time, FES, queue_, users, u, id_client, distribution)
                elif(event.typ == "departure"):
                    users, delays = departure(time, FES, queue_, users, delays, distribution)

            #cumulative mean of delays per departure event
            cum_mean_per_event = cum_mean(delays)

            # detect and remove transient
            without_transient, idx, thr = remove_transient(cum_mean_per_event, u, distribution)
            print(f'(Transient detection) Threshold for the min-max gap within a window: {thr}')
            # plot average delays per departure event (end of warm-up transient detection)
            fig2, ax2 = plt.subplots(1,1)
            plot_metric(fig2, ax2, cum_mean_per_event , 'Delay', x_label='#departure_event')
            # plot a vertical line when the transient has ended
            ax2.axvline(x = idx, ymin=0, ymax=5, c = 'r',  label = 'end of transient')
            ax2.set_title(f'#departure_event VS cumulative_average_delay, \nUtilization_level: {u}, distribution: {distribution}', fontsize=14)
            fig2.savefig(f'graphs/{distribution}/with u: {u}, (transient detection) #departure_event VS cumulative_average_delay.png')
            plt.close()


            # compute the correct number of batches
            correct_num_batches = find_batches(without_transient, u, 10, confidence)

            #compute the mean for each batch and consequently the confidence interval
            means, ci_lower_bounds, ci_upper_bounds = batch_means(without_transient, correct_num_batches = correct_num_batches)
            # plot the average delays per departure event as result of batch means algorithm 
            fig3, ax3 = plt.subplots(1,1)
            plot_metric_with_ci(ax3, means, 'delays', ci_lower_bounds, ci_upper_bounds, x_label='batch id')
            ax3.set_title(f'batch id VS cumulative_average_delay,\nUtilization_level: {u}, distribution: {distribution}')
            fig3.savefig(f'graphs/{distribution}/with u: {u}, (batch mean) batch id VS cumulative_average_delay.png')
            plt.close()

            if distribution == 'hyperexponential':
                mean_hyperexp.append(np.mean(means))
                ci_hyperexp = t.interval(0.95, len(means)-1, np.mean(means), np.std(means))
                lower_bounds_hyperexp.append(ci_hyperexp[0])
                upper_bounds_hyperexp.append(ci_hyperexp[1]) 
            elif distribution == 'deterministic_process':
                mean_det.append(np.mean(means))
                ci_det = t.interval(0.95, len(means)-1, np.mean(means), np.std(means))
                lower_bounds_det.append(ci_det[0])
                upper_bounds_det.append(ci_det[1])
            elif distribution == 'exponential':
                mean_exp.append(np.mean(means))
                ci_exp = t.interval(0.95, len(means)-1, np.mean(means), np.std(means))
                lower_bounds_exp.append(ci_exp[0])
                upper_bounds_exp.append(ci_exp[1])


    fig4, ax4 = plt.subplots(1,1)
    fig4.suptitle(f'Utilization_level VS delays')
    plot_metric_with_ci(ax4, mean_exp, label_= 'exponential', ci_lower=lower_bounds_exp, ci_upper=upper_bounds_exp, x_label = 'Utilization (work / time_unit)')
    plot_metric_with_ci(ax4, mean_hyperexp, label_= 'hyperexponential', ci_lower=lower_bounds_hyperexp, ci_upper=upper_bounds_hyperexp, x_label = 'Utilization Utilization (work / time_unit)')
    plot_metric_with_ci(ax4, mean_det, label_= 'deterministic', ci_lower=lower_bounds_det, ci_upper=upper_bounds_det, x_label = 'Utilization Utilization (work / time_unit)')
    plt.close()
    
    print('End of the simulation')
    print("The results are plotted in the graphs that are saved in the 'graphs' folder")

if __name__ == '__main__':
    main()











# the utilization is lambda time the average service time. 
# for infinite queue the utilization should be always less than one otherwise
# the system is not stable. 
# utilization is the average amount of work requested to the server from customers arriving in the time unit
# lambda = 3 3 person per unit for time
# if the service time is 10 units of time it means that you need to work 30 units of time on average.
# utilization for single server queue cannot exceed 1


