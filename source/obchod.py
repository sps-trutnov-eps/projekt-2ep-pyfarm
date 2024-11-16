import pygame
import sys

class Obchod:
    def __init__(self, hrac):
        pygame.init()
        self.screen_size = 1000, 600
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        self.running = True
        self.hrac = hrac
    
    def run(self):
        while self.running:
            self.screen.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.update()
            self.clock.tick(60)
        
        self.hrac.rect.topleft = (self.hrac.rect.x + 120, self.hrac.rect.y)
        pygame.display.set_mode((1000,600))


