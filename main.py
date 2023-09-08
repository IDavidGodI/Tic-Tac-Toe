import pygame
import numpy as np

from Player import Player
from Bot import *
from Board import Board
from Window import Window
from Clock import Clock


class Game:

    def __init__(self):
        pygame.init()

        
        pygame.display.set_icon(pygame.image.load("./icono/PalomaSentá.png"))
        pygame.display.set_caption("Triqui (como tres en raya pero...")
        self.turn = round(random.random())
        self.players = np.array((None,None),Player)
        self.board = Board(450)
        self.window = Window(700,700)
        self.clock = Clock(60)
        self.font = pygame.font.Font(None,70)
        self.info_text = str()
        
        

    def render_info_text(self, window:pygame.Surface):
        rendered_text = self.font.render(self.info_text, True, "#FFFFFF")
        size = pygame.Vector2(rendered_text.get_size())/2
        w_center = pygame.Vector2(window.get_size())/2
        window.blit(rendered_text,(w_center.x-size.x,60-size.y))
        

    def setPlayers(self, player1, player2):

        self.players[0] = player1
        self.players[1] = player2

    def changeTurn(self):
        if self.turn==0: self.turn = 1
        else: self.turn=0
        self.update_current_player()
        

    def update_current_player(self):
        self.current_player: Player = self.players[self.turn]
        self.game_symbol = 'X' if self.current_player.symbol==1 else 'O'
        self.info_text = f"Es el turno de {self.game_symbol}"

    def render(self):
        self.render_info_text(self.window.get_screen())
        self.board.render(self.window.get_screen())
        self.window.render()

    def update(self,dt):
        self.board.update(dt)
        self.window.update(dt)

    def reset(self):
        self.board.reset()
        for p in self.players:
            p.reset()

        self.turn = 0


    def loop(self):
        win_line = None
        running = True
        self.update_current_player()
        self.update(0)
        self.render()

        log_file = open("logs/game_log", "w")
        print("Game started")
        while running:
            dt = self.clock.get_dt()
            
            

            self.window.handle_events()
            
                    
            if (win_line and not self.board.line):
                print(win_line)
                self.board.set_win_line(*win_line)
            elif not self.board.hasEnded:
                
                self.current_player.get_event(self.board)
            

            if self.current_player.played_turns>=3 and not win_line: 
                winner = self.board.check_winner(self.current_player.symbol)
                if winner:
                    win_line = self.board.check_winner_line(self.current_player.symbol,*self.current_player.last_play)
                    self.board.hasEnded = True
                    self.info_text = f"Gana el jugador {self.game_symbol}"
                if (not win_line and self.board.check_tie()): 
                    self.board.hasEnded = True
                    self.info_text = f"Es un empate"
                    print(self.info_text)
            self.update(dt)

            if self.current_player.turn_played and not self.board.hasEnded: 
                self.current_player.turn_played = False
                self.board.increase_turns()
                log_file.write(f"Jugada {self.board.played_turns}:\n{self.format_row(self.board.matrix[0])}\n{self.format_row(self.board.matrix[1])}\n{self.format_row(self.board.matrix[2])}\n")
                self.changeTurn()
                

            self.render()      
        log_file.close()
    def format_row(self, row):
        r = []

        for i in row:
            if i==0: r.append('-') 
            elif i==1: r.append('x')
            else: r.append('o')
        return r
g = Game()

g.setPlayers(BetterRandomBot(2), BetterRandomBot(1))
g.loop()