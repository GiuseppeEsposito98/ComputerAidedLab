import numpy as np
from Player import Player
class Board():
    def __init__(self, 
    board_size: tuple) -> None:
        self.board_size = board_size
        self.matrix = np.zeros(self.board_size, dtype=object)
        self.list_of_players = list()
    
    def update_matrix(self, 
        player: Player,
        previous_coor: tuple):
        self.matrix[previous_coor[0], previous_coor[1]] = 0
        self.matrix[player.coordinates[0], player.coordinates[1]] = player
        
    def save_players(self, player):
        self.list_of_players.append(player)
        self.matrix[player.coordinates[0], player.coordinates[1]] = player

    def __str__(self) -> str:
        return str(self.matrix)