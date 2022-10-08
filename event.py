from client import *
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