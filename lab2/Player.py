
import random
import numpy as np
from board import Board
BOARD_SIZE = 8
random.seed(302179)
class Player:
    def __init__(self, 
    initial_coordinates: tuple,
    speed: float, 
    id_: int):
        self.id_ = id_
        self.coordinates = initial_coordinates
        self.kill_counter=0
        self.speed = speed

    def get_id(self):
        return int(self.id_)

    
    def check_distance(self, other, thr):
        dist = (abs(self.coordinates[0] - other.coordinates[0]), abs(self.coordinates[1] - other.coordinates[1])) 
        if (dist[0]<=thr and dist[1]<=thr):
            return True
        else:
            return False
    
    def update_coordinates(self, movement):
        self.coordinates = (self.speed * movement[0], self.speed* movement[1])



    def increase_kill(self):
        self.kill_counter +=1

    def __str__(self) -> str:
        return str(self.id_)




