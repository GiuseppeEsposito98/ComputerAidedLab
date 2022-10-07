class Event():
    def __init__(self, duration, typ) -> None:
        self.duration = duration
        self.typ = typ 

    def __str__(self):
        return f"duration = {self.duration}, type = {self.typ}"

    def __lt__(self, other):
        return self.duration < other.duration