import random

class Client:
    def __init__(self,
    typ: str,
    arrival_time: int,
    id_client: int) :
        self.typ = typ
        self.arrival_time= arrival_time
        self.id_client = id_client

    def __lt__(self, other):
        return self.arrival_time < other.arrival_time

    def __str__(self) -> str:
        return f"id: {self.id_client}"

    def set_(self, status: str):
        self.typ = status