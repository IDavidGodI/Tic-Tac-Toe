import pygame
from pygame import Vector2
from Board import Board

class Player:
    
    def __init__(self, symbol):
        self.symbol = symbol
        self.played_turns = 0
        self.last_play = (-1,-1)
        self.turn_played = False

    def reset(self):
        self.turn_played = False
        self.last_play = (-1,-1)
        self.played_turns = 0

    def play_turn(self, board:Board, x,y):
        board.set_cell(self.symbol,x,y)

        self.last_play = (x,y)
        self.played_turns+=1
        self.turn_played = True

    def get_event(self, board:Board):
        mouse_click = pygame.mouse.get_pressed()[0]

        if (mouse_click):
            pos =Vector2(pygame.mouse.get_pos())
            # print(pos)
            c = board.pixels_to_cells(pos.x, pos.y)
            if c : 
                self.play(board,*c)

    def play(self, board:Board, x, y):
        
        if board.isEmpty(x,y) and not board.hasEnded:
            self.play_turn(board, x,y)