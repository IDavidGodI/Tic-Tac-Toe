from Board import Board
import numpy as np

from Player import Player
from math import floor

import time
import random

class Bot(Player):

    def __init__(self, symbol):

        Player.__init__(self, symbol)
        self.o_symbol = symbol = 1 if self.symbol==2 else 2
        
    def get_event(self, board: Board):
        predict = board.get_matrix_copy()
        computed_play = self.compute_play(board, predict)
        time.sleep(2)
        print(f"Bot selected {computed_play[1]} with a {computed_play[0]} score")
        x,y = computed_play[1]
        self.play(board,x,y)
        
    def compute_play(self, board:Board, matrix, max=True):

        if self.terminal(board, matrix):
            return [self.toValue(board, matrix), None]

        if max: # MAX    
            value = [float('-inf'), None]
        else: # MIN    
            value = [float('inf'), None]
            
        for x in range(0,3):
            for y in range(0,3):
                if (matrix[y,x]!=0): continue

                c_matrix = self.case_result(matrix, self.symbol if max else self.o_symbol, x,y)
                n_value = self.compute_play(board,c_matrix, not max)
                n_value[1] = (x,y)

                if (max):
                    if (n_value[0]>value[0]):
                        value = n_value
                else:
                    if (n_value[0]<value[0]):
                        value = n_value
            
        return value
            

    
    def case_result(self, matrix, symbol, x,y):
        copy = np.copy(matrix)
        copy[y][x] = symbol
        return copy

    def terminal(self, board: Board, matrix):
        return (
            board.check_winner(self.symbol, matrix) or
            board.check_winner(self.o_symbol, matrix) or            
            board.check_tie(matrix)
        )
    
    def toValue(self, board:Board, matrix):

        if board.check_winner(self.symbol, matrix): return 1
        if board.check_winner(self.o_symbol, matrix): return -1            
        return 0

    def copy_matrix(self, matrix):
        return np.copy(matrix)
    

class RandomBot1(Bot):

    def __init__(self, symbol):

        Bot.__init__(self, symbol)


    def get_event(self, board: Board):

        if self.played_turns<=2:
            p = random.randint(0,8)
            x,y = p%3, floor(p/3)
            time.sleep(random.random()+0.2)
            self.play(board,x,y)
        else: super().get_event(board)

class BetterBot(Bot):

    def __init__(self, symbol):
        super().__init__(symbol)
    
    def toValue(self, board: Board, matrix):
        spaces = board.count_spaces(matrix)
        return super().toValue(board, matrix)*(spaces+1)
    
class BetterRandomBot(RandomBot1,BetterBot):

    def __init__(self, symbol):
        super().__init__(symbol)

    def get_event(self, board: Board):
        return RandomBot1.get_event(self,board)


