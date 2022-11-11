from client import *
class Server:
    def __init__(self) -> None:
        self.busy = False
        self.processing_client = None

    def is_busy(self, busy):
        self.busy = busy
    
    def set_client(self, client):
        self.processing_client = client
