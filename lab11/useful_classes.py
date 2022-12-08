
class Client:
    '''
    This class manages the customers entering in the system.
    '''
    def __init__(self,
    status: str,
    arrival_time: int,
    id_client: int,
    priority: str = '',
    remaining_time: float = 0.0,
    server= None) :
        self.status = status
        self.arrival_time= arrival_time
        self.id_client = id_client
        self.priority = priority
        self.remaining_time = remaining_time
        self.server = server

    def __str__(self) -> str:
        return f"id: {self.id_client}"

    def set_status(self, status: str):
        # either 'arrival' or 'departure'
        self.status = status

    def set_type(self, typ):
        # either 'high' or 'low' priority'
        self.typ = typ
    
    def save_remaining_time(self, remaining_time):
        '''
        If the client is low priority and it is in a server and a client of high priority has just arrived
        we need to interrupt the job of the current client and put it at the head of the queue saving his remaining 
        service time a server need to have his job completed.
        
        '''
        self.remaining_time = remaining_time
    
    def set_server(self, server):
        '''
        keep track of the server where the client is.
        '''
        self.server = server


class Event:
    '''
    This class defines the events that can be either 'arrival' or 'departure' keeping track of the client they are releted
    '''
    def __init__(self, time, typ) -> None:
        self.time = time
        # departure or arrival
        self.typ = typ
        # this is the first client
        self.client = Client("arrival", 0, 0, 'high')

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

class Server:
    '''
    This class represent the k servers involved in the simulation, this will be needed to let 2 people working in parallel.
    '''
    def __init__(self) -> None:
        self.status = 'idle'
        self.client = None

    def set_status(self, status:tuple):
        '''
        the server can be either busy or idle.
        '''
        self.status = status
    
    def set_client(self, client):
        '''
        This method will take track of which client the server is serving.
        '''
        self.client = client
    
    def remove_client(self):
        new_client = self.client
        self.client = None
        return new_client
        
        
    

class Queue:
    '''
    This class has been created to manage the clients with low and high priority
    '''
    def __init__(self, 
                max_length = 0,
                typ: str = '') -> None:
        self.typ = typ
        self.max_length = max_length
        self.client_list = list()

    def add_client(self, client:Client):
        '''
        when all server are busy, add the client to the queue if there is still a place
        '''
        if len(self.client_list) < self.max_length:
            self.client_list.append(client)
    
    def add_client_as_first(self, client:Client):
        '''
        when a client is dropped because of a conflict, just insert it as it is the next to be served
        '''
        if len(self.client_list) < self.max_length:
            self.client_list.insert(0, client)

    def remove_first_client(self):
        '''
        according to the FIFO policy that we are asked to use this method remove the first client added
        '''
        client_served = self.client_list.pop(0)
        return client_served
    
    def __len__(self):
        '''
        This function return the length of the queue
        '''
        return len(self.client_list)
    
    def is_empty(self):
        '''
        This method checks whether the queue is empty or not
        '''
        if len(self.client_list) == 0:
            return True
        else:
            return False
    
    def set_max_length(self,N):
        self.max_length = N
    

