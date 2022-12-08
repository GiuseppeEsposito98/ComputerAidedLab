
import numpy as np
import random
from useful_classes import *
from sympy import symbols, Eq, solve


def arrival(lambda_hp, lambda_lp, distribution, case, queue, N, FES, server, time, id_client, users):
    # Random generate the priority of the next generated client.
        priority_type = random.choice(["low", "high"])
        # Random generate the inter-arrival time
        if priority_type == 'high':
            t_ia = random.expovariate(lambda_hp)
        elif priority_type == 'low':
            t_ia = random.expovariate(lambda_lp)
        # and the service_time
        service_time = generate_service_time(case, priority_type, lambda_hp, lambda_lp, distribution)

        # Schedule the arrival of the next client if there is any room in the queue
        if len(queue) <= N:
            e10 = Event(time + t_ia, 'arrival')
            users = users + 1
            client = Client('arrival', time, id_client, priority_type, remaining_time=service_time)
            e10.assignClient(client)
            FES.append(e10)
            queue.append(client)
        # Schedule the departure of the actual client when one of the sever has finishes his last job
        if users == 1:
            server.set_client(client)
            client.set_server(server)
            server.status = 'busy'
            e = Event(time+service_time, "departure")
            e.assignClient(client)
            FES.append(e)
        return users, id_client

def high_arrival(server_dict, users, time, FES, queue, distribution, case, lambda_hp, lambda_lp, N, id_client):
        """
            In the arrival function when a client just generated has a priority that is high there can be some conflict
            if there are some servers that are processing a client that has low priority. Then we suppose that client_arr
            has already been checked to be high_priority and here we check all the other things.
        """
        # Select at random the server to idle in order to serve the HP client
        srv_hp = random.choice(list(server_dict.values()))
        priority_type = random.choice(["low", "high"])
        if priority_type == 'high':
                t_ia = random.expovariate(lambda_hp)
        elif priority_type == 'low':
                t_ia = random.expovariate(lambda_lp)
        service_time = generate_service_time(case, priority_type, lambda_hp, lambda_lp, distribution)
        if len(queue) <= N:
            e = Event(time + t_ia, 'arrival')
            FES.append(e)
            users = users + 1
            client = Client('arrival', time, id_client, priority_type, remaining_time=service_time)
            e.assignClient(client)
            queue.append(client)

        # The client which has been stopped is put another time in the queue if there is an avilable room
        client_via = srv_hp.client
        client_via.server = None
        client_via.time = time
        if users == 1:
            srv_hp.client = client_via
            client_via.server = srv_hp
            srv_hp.status = 'busy'
            e3 = Event(time+ service_time, 'departure')
            e3.assignClient(client_via)
            FES.append(e3)
        if len(queue)<= N:
            e4 = Event(time + client.arrival_time, 'arrival')
            FES.insert(0,e4)
        return users, id_client

# Departure function
def departure(users,time, FES, queue, distribution, case, lambda_hp, lambda_lp, delays_low, delays_high, delays):
        """
            When a client has finished to be served an instance of the event departure is created and the server 
            that was working on that is made idle. 
        """
        # If the selected distribution for the service time is exponential
        # Remove the served client from the queue
        client = queue.pop(0)
        service_time = generate_service_time(case, client.priority, lambda_hp, lambda_lp, distribution )
        server = client.server
        if server != None:
            server.status = 'idle'
        users = users - 1
        if users > 0:
            e24 = Event(time+service_time, "departure")
            e24.assignClient(client)
            FES.append(e24)
            if client.priority == 'high':
                delays_high.append(time-client.arrival_time)
            if client.priority == 'low':
                delays_low.append(time-client.arrival_time)
            delays.append(time-client.arrival_time)
        # Return the number of users that are now in the queue and the time the client just served has enetered the queue
        return users



def generate_hyperexponential(case, priority):
        """
           Generate numbers from an hyperexponential distribution with respect to the priority of the client
           and also to different setup of the hyperexponential distribution in terms of mean and of standard
           deviation of the possible exponential distributions
        """
        p = 0.5

        if case == "a": 
            lam1 = 1/6 
            lam2 = 1/8 
            u = random.uniform(0,1)
            if u <= p:
                service_time = random.expovariate(1/lam1)
            else:
                service_time = random.expovariate(1/lam2)
            
        # by definition of mean and standard deviation a systems of 2 equation is defined that can be solved
        # with sympy library.
        if case == "b":
            if priority == "high":
                mean = 1/2
                stdv = 5
                lam1, lam2 = symbols('lambda1 lambda2')
                eq1 = Eq(p/lam1 + (1-p)/lam2, mean)
                eq2 = Eq(2*p/(lam1**2) + 2*(1-p)/(lam2**2)-mean, stdv**2)
                sols = solve((eq1,eq2), (lam1, lam2), dict = True)
                l1 = sols[0]['lambda1']
                l2 = sols[0]['lambda2']
                u = random.uniform(0,1)
                if u <= p:
                    service_time = random.expovariate(1/l1)
                else:
                    service_time = random.expovariate(1/l2)

            if priority == "low":
                mean = 3/2
                stdv = 15
                # by definition of mean and standard deviation a systems of 2 equation is defined that can be solved
                # with sympy library.
                lam1, lam2 = symbols('lambda1 lambda2')
                eq1 = Eq(p/lam1 + (1-p)/lam2, mean)
                eq2 = Eq(2*p/(lam1**2) + 2*(1-p)/(lam2**2)-mean, stdv**2)
                sols = solve((eq1,eq2), (lam1, lam2), dict = True)
                l1 = sols[0]['lambda1']
                l2 = sols[0]['lambda2']
                u = random.uniform(0,1)
                if u <= p:
                    service_time = random.expovariate(1/l1)
                else:
                    service_time = random.expovariate(1/l2)

        return service_time

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




def generate_service_time(case, priority, lambda_hp, lambda_lp, distribution = 'exponential'):
        """
            In all different cases given by the priority-type of the client and of the distribution from which 
            it has to be generated, a service time is generated
        """
        if distribution == "exponential":
            if case == "a": 
                scale = 1
            if case == "b":
                if priority == "high":
                    scale = 1/2
                if priority == "low":
                    scale = 3/2
            service_time = random.expovariate(scale)
        elif distribution == "deterministic_process":
            if case == "a":
                service_time = 1
            if case == "b":
                if priority == "high":
                    service_time = lambda_hp
                if priority == "low":
                    service_time = lambda_lp
        if distribution == "hyperexponential":
            service_time = generate_hyperexponential(case, priority)
        
        return service_time