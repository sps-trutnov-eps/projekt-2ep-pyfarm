import pygame
import sys

pygame.init()
pygame.display.set_caption("PyFarm")
screen_size = 1000, 600
screen = pygame.display.set_mode(screen_size)

running = True

postava1 = pygame.image.load("images/postava1.png")

while running:
    screen.fill((255,255,255))
    screen.blit(postava1,(500,300))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.update()

pygame.quit()
sys.exit()