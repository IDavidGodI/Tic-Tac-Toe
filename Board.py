import numpy as np
import pygame
from pygame.math import Vector2
from math import floor

class Board:


    WIN_LINE_DRAW_SPEED = 2.5

    def __init__(self, size:int):
        self.size = size
        self.matrix = np.zeros((3,3))

        self.cell_size = round(self.size/3)
        self.frame = pygame.Surface((self.size,self.size))
        self.hasEnded = False
        self.line = False
        self.drawing_line = False
        self.played_turns = 0

    def reset(self):
        self.matrix = np.zeros((3,3))
        self.line = False
        self.drawing_line = False
        self.hasEnded = False

    def increase_turns(self):
        self.played_turns+=1
    def __str__(self):
        return self.matrix.__str__()
    
    def render(self, window:pygame.Surface):
        
        self.frame.fill("#713672")
        wx,wy = window.get_size()

        for i in range(self.cell_size,self.size,self.cell_size):
            pygame.draw.line(self.frame, "#c194b2",(i,0),(i,self.size),6)
            pygame.draw.line(self.frame, "#c194b2",(0,i),(self.size,i),6)
        
        for x in range(0,3):
            for y in range(0,3):
                if self.matrix[y,x] == 1:
                    self.render_x((x,y))
                if self.matrix[y,x] == 2:
                    self.render_o((x,y))

       
        if self.hasEnded and self.line: 
            pygame.draw.line(self.frame, "#FFDD33",self.win_line_start*self.cell_size,self.win_line_cp*self.cell_size,10)

        window.blit(self.frame,((wx/2)-self.size/2,(wy/2)-self.size/2))
        # window.blit(self.frame,(0,0))

    def trace_win_line(self,dt):

        cl =  self.win_line_start.distance_to(self.win_line_cp)
        tl = self.win_line_start.distance_to(self.win_line_end)
        self.drawing_line = cl < tl
        if (self.drawing_line):
            direction = (self.win_line_end-self.win_line_start).normalize()
            

            self.win_line_cp+=direction*Board.WIN_LINE_DRAW_SPEED*dt
            cl = self.win_line_start.distance_to(self.win_line_cp)
            if  cl > tl:
                self.win_line_cp = self.win_line_end
            

            
            
    def count_spaces(self, matrix = None):
        if matrix is None: matrix = self.matrix
        return np.count_nonzero(matrix==0)
        
        
    def set_win_line(self, start:tuple[int,int], end:tuple[int,int]):
        self.hasEnded = True
        self.line = True
        self.drawing_line = True

        self.win_line_start = Vector2(start)
        self.win_line_end = Vector2(end)
        self.win_line_start+=Vector2(0.5,0.5)
        self.win_line_end+=Vector2(0.5,0.5)

        d = self.get_direction(self.win_line_start, self.win_line_end)
        
        

        self.win_line_cp = Vector2(self.win_line_start)

    def get_direction(self, v1: Vector2,v2: Vector2):
        d = (v2-v1).normalize()
        
        if (d.x>0): d.x=1
        if (d.y>0): d.y=1

        return d

    def get_matrix_copy(self):
        return np.copy(self.matrix)
    def update(self,dt):
        if (self.hasEnded and self.line and self.drawing_line):
            self.trace_win_line(dt)

    def set_cell(self, symbol, x, y):
        self.matrix[y,x] = symbol
        return x,y

    def transform_coords(self,c):
        return floor(c/self.cell_size)

    def pixels_to_cells(self, x, y):
        offset = (700/2)-(self.size/2)
        x-= offset
        y-= offset

        if (x<0 or y<0 or x>self.size or y>self.size): return None

        return self.transform_coords(x), self.transform_coords(y)

    def isEmpty(self, x,y):
        
        return self.matrix[y,x] == 0

    def render_x(self, pos:tuple[int,int], offset = 0.3):

        x,y = pos
        cs = self.cell_size
        x*=cs
        y*=cs

        x+=cs*offset
        y+=cs*offset
        
        
        lines = [
            ((x,y),(x+cs*(1-offset*2),y+cs*(1-offset*2))),
            ((x+cs*(1-offset*2),y),(x,y+cs*(1-offset*2)))
        ]
        
        for line in lines:
            pygame.draw.line(self.frame, "#c7dcac",line[0],line[1],9)

    


    def render_o(self, pos:tuple[int,int], offset = 0.4):

        x,y = pos
        cs = self.cell_size
        x*=cs
        y*=cs

        center = (x+(cs/2), y+(cs/2))

        radius = (cs/2)*(1-offset)
               
        pygame.draw.circle(self.frame,"#BACEF4",center, radius,7)

    def check_v(self, matriz, symbol, x):
            
        for y in range(0,3):
            if (matriz[y,x]!=symbol): return None

        return (x,0),(x,2)
    
    def check_h(self, matriz, symbol, y):
            
        for x in range(0,3):
            if (matriz[y,x]!=symbol): return None
        
        return (0,y),(2,y)
            
    def check_d(self, matrix, symbol, x, y):

        # return (matrix[0,0]==matrix[1,1]==matrix[2,2]==symbol or
        #     matrix[2,0]==matrix[1,1]==matrix[0,2]==symbol )

        if not (x==y or (x==0 and y==2) or (x==2 and y==0)): return None
        
        nx, ny = x,y
        

        while True:
            if (x!=1):
                if (x==0): dx=1
                else: dx=-1

                if (y==0): dy=1
                else: dy=-1
                if (matrix[ny,nx]!=symbol): return None
                if (not (nx+dx in range(0,3)) or not (ny+dy in range(0,3))): 
                    
                    return (x,y),(nx,ny)
                nx+=dx
                ny+=dy
                continue
            
            nx, ny = 0, 0
            state = self.check_d(matrix, symbol, nx, ny)
            if (state): return state

            
            nx, ny = 0, 2

            return self.check_d(matrix, symbol,nx,ny)
        
    def check_tie(self, matrix=None):
        if matrix is None: matrix = self.matrix
        return not (0 in matrix)
    
    def check_winner(self,symbol, matrix=None):
        if matrix is None: matrix=self.matrix
        return (
            matrix[0,0]==matrix[0,1]==matrix[0,2]==symbol or
            matrix[1,0]==matrix[1,1]==matrix[1,2]==symbol or
            matrix[2,0]==matrix[2,1]==matrix[2,2]==symbol or

            matrix[0,0]==matrix[1,0]==matrix[2,0]==symbol or
            matrix[0,1]==matrix[1,1]==matrix[2,1]==symbol or
            matrix[0,2]==matrix[1,2]==matrix[2,2]==symbol or

            matrix[0,0]==matrix[1,1]==matrix[2,2]==symbol or
            matrix[2,0]==matrix[1,1]==matrix[0,2]==symbol 
            
        )


    def check_winner_line(self, symbol, x, y, matrix=None):
        if matrix is None: matrix = self.matrix
        return self.check_v(matrix, symbol,x) or self.check_h(matrix, symbol,y) or self.check_d(matrix, symbol, x, y)
