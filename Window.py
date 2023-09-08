import pygame


class Window:

    def __init__(self, w, h):
        self.screen = pygame.display.set_mode((w,h))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def get_screen(self):
        return self.screen

    

    def update(self, dt):
        self.screen.fill("#713672")
    
    def get_center(self):
        return pygame.Vector2(self.screen.get_size())/2

    def render(self):

        pygame.display.update()