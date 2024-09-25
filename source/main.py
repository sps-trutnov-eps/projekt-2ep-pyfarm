import pygame
import sys

pygame.init()
pygame.display.set_caption("PyFarm")
screen_size = 1000, 600
screen = pygame.display.set_mode(screen_size)

running = True

postava1 = pygame.image.load("images/postava1.png")
postava_rect = postava1.get_rect(center = (500,300)) 
speed = 6

while running:
    screen.fill((255,255,255))
    screen.blit(postava1,postava_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        postava_rect.x -= speed  
    if keys[pygame.K_RIGHT]:
        postava_rect.x += speed  
    if keys[pygame.K_UP]:
        postava_rect.y -= speed 
    if keys[pygame.K_DOWN]:
        postava_rect.y += speed  

    
    pygame.display.update()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()