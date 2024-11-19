import pygame
import sys

class Obchod:
    def __init__(self, hrac):
        pygame.init()
        self.hrac = hrac
        self.screen_size = 1000, 600
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        self.running = True
    
    def sell_items(self):
        if self.hrac.carrots > 0:
            self.hrac.money += self.hrac.carrots * 10
            self.hrac.carrots = 0
        if self.hrac.wheat > 0:
            self.hrac.money += self.hrac.wheat * 10
            self.hrac.wheat = 0
        if self.hrac.wool > 0:
            self.hrac.money += self.hrac.wool * 10
            self.hrac.wool = 0
        if self.hrac.milk > 0:
            self.hrac.money += self.hrac.milk * 10
            self.hrac.milk = 0
        if self.hrac.meat > 0:
            self.hrac.money += self.hrac.meat * 10
            self.hrac.meat = 0
    
    def run(self):
        while self.running:
            self.screen.fill((255, 255, 255))
            self.sell_items()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.update()
            self.clock.tick(60)
        
        self.hrac.rect.topleft = (self.hrac.rect.x + 120, self.hrac.rect.y)
        pygame.display.set_mode((1000,600))
        return self.hrac.money

