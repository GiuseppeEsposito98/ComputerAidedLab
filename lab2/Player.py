import math
import random
import numpy as np
class Player:
    def __init__(self, 
    initial_coordinates: tuple,
    speed: float, 
    id_: int):
        self.id_ = id_
        self.coordinates= initial_coordinates
        self.kill_counter=0
        self.speed = speed

    def get_id(self):
        return int(self.id_)

    def compute_local_winner(self, players, thr):
        for other in players:
            dist = self.compute_distance(other, thr)
            if(self.check_distance()):
                winner = random.choice([0,1])
                if winner == 1:
                    self.increase_kill()
                    return self.id_
                elif winner == 0:
                    other.increase_kill()
                    return other.id_
    
    def check_distance(self, other, thr):
            dist = self.compute_distance(other)
            if (dist[0]<=thr and dist[1]<=thr):
                return True
            else:
                return False


    def compute_distance(self, other):

        dist = ( abs(self.coordinates[0] - other.coordinates[0]), abs(self.coordinates[1] - other.coordinates[1])) 
        return dist
    
    def update_coordinates(self, 
    board_size: int):
        move = random.choice([(1,0), (1,1), (0,1), (-1,0), (-1, -1), (0,-1), (-1,1)])
        if move[0] < 0 or move[1] < 0 or move [0] > board_size or move[1] > board_size:
            move = random.choice([(1,0), (1,1), (0,1), (-1,0), (-1, -1), (0,-1), (-1,1)])
        else:
            self.coordinates = self.coordinates + move


    def increase_kill(self):
        self.kill_counter +=1

    def __str__(self) -> str:
        return str(self.id_)



