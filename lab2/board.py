import numpy as np
import random
from Action import Action
random.seed(302179)
class Board():
    def __init__(self, 
    board_size: tuple) -> None:
        self.board_size = board_size
        self.matrix = np.zeros(board_size)
        self.list_of_players = list()
        self.killed = []

    
    def update_matrix(self):
        '''update the values in the matrix with a random movement and also the coordinated of the player'''
        for player in self.list_of_players:
            movement = Action.move(player.coordinates, self.board_size[0])
            self.matrix[player.coordinates[0], player.coordinates[1]] = 0
            self.matrix[movement[0], movement[1]] = player.id_
            player.update_coordinates(movement)
        
    def save_players(self, player):
        self.list_of_players.append(player)
        self.matrix[player.coordinates[0], player.coordinates[1]] = player.id_

    def sort_list(self):
        self.list_of_players.sort(key=lambda x: x.id_)

    def remove_player(self, player):
        '''when a player is killed, append it to the list of killed players and then remove from the general list of players'''
        self.killed.append(player)
        self.list_of_players.remove(player)

    def __str__(self) -> str:
        return str(self.matrix)
