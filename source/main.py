import pygame
import sys

pygame.init()
pygame.display.set_caption("PyFarm")
screen_size = 1000, 600
screen = pygame.display.set_mode(screen_size)

class Hrac(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = postava1 = pygame.image.load("images/postava1.png").convert_alpha()
        self.rect = postava1.get_rect(center = (500,300)) 
        self.speed = 6

    def input(self):
        keys = pygame.key.get_pressed()
    
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed  
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed 
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed 
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed 
    def update(self):
        self.input()

hrac = Hrac()

mapa1 = pygame.image.load("images/mapa1.png")


running = True

while running:
    
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    hrac.update()
    screen.blit(hrac.image, hrac.rect)
    
    pygame.display.update()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()