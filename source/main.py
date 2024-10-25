import pygame
import sys
import random
from obchod import Obchod

pygame.init()

pygame.display.set_caption("PyFarm")
screen_size = 1000, 600
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 42)

class Camera_group(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        
        self.posun = pygame.math.Vector2()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        
        self.map_surf = pygame.image.load("images/mapa_v1.png").convert_alpha()
        self.map_rect = self.map_surf.get_rect(topleft = (0,0))
        
    def stred_camera(self, target):
        self.posun.x = target.rect.centerx - self.half_width
        self.posun.y = target.rect.centery - self.half_height

    def custom_draw(self, hrac):
        self.stred_camera(hrac)
        posun_mapy = self.map_rect.topleft - self.posun
        self.display_surface.blit(self.map_surf, posun_mapy)
        for sprite in self.sprites():
            posun_pos = sprite.rect.topleft - self.posun
            self.display_surface.blit(sprite.image, posun_pos)


class Hrac(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.transform.scale(pygame.image.load("images\character_blue.png"), (35,80)).convert_alpha()
        self.rect = self.image.get_rect(center = pos) 
        self.direction = pygame.math.Vector2()
        self.speed = 5
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction = pygame.math.Vector2()
        if keys[pygame.K_LEFT]:
            self.direction.x -= self.speed  
        if keys[pygame.K_RIGHT]:
            self.direction.x += self.speed 
        if keys[pygame.K_UP]:
            self.direction.y -= self.speed 
        if keys[pygame.K_DOWN]:
            self.direction.y += self.speed 
    def update(self):
        self.input()
        self.rect.center += self.direction
        
        self.rect.left = max(camera_group.map_rect.left, self.rect.left)
        self.rect.right = min(camera_group.map_rect.right, self.rect.right)
        self.rect.top = max(camera_group.map_rect.top, self.rect.top)
        self.rect.bottom = min(camera_group.map_rect.bottom, self.rect.bottom)
        

class Cow(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.transform.scale(pygame.image.load("images\cow.png"), (125, 80)).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2(random.choice([-1, 1]), random.choice([-1, 1])) 
        self.speed = 2  

    def move(self):
        self.rect.center += self.direction * self.speed

        if random.randint(0, 100) < 1:  
            self.direction.x = random.choice([-1, 1])
            self.direction.y = random.choice([-1, 1])

        if self.rect.left < camera_group.map_rect.left or self.rect.right > camera_group.map_rect.right:
            self.direction.x *= -1
        if self.rect.top < camera_group.map_rect.top or self.rect.bottom > camera_group.map_rect.bottom:
            self.direction.y *= -1

    def update(self):
        self.move()
        
class Sheep(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.transform.scale(pygame.image.load("images\sheep.png"), (125, 80)).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2(random.choice([-1, 1]), random.choice([-1, 1])) 
        self.speed =  2.5
       
    def move(self):
        self.rect.center += self.direction * self.speed

        if random.randint(0, 100) < 2:  
            self.direction.x = random.choice([-1, 1])
            self.direction.y = random.choice([-1, 1])

        if self.rect.left < camera_group.map_rect.left or self.rect.right > camera_group.map_rect.right:
            self.direction.x *= -1
        if self.rect.top < camera_group.map_rect.top or self.rect.bottom > camera_group.map_rect.bottom:
            self.direction.y *= -1

    def update(self):
        self.move()



class Ctverec_obchodu(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y, group):
        super().__init__(group)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x,y))


class Flower(pygame.sprite.Sprite):
    def __init__(self, pos, group, flower_image):
        super().__init__(group)
        self.image = flower_image.convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        
def flower_spawn():
    flower_images = [
        pygame.image.load("images/Flowers/blue_flower.png"),
        pygame.image.load("images/Flowers/orange_flower.png"),
        pygame.image.load("images/Flowers/purple_flower.png"),
        pygame.image.load("images/Flowers/red_flower.png")
    ]
    chosen_image = random.choice(flower_images)
    random_position = (
        random.randint(camera_group.map_rect.left, camera_group.map_rect.right),
        random.randint(camera_group.map_rect.top, camera_group.map_rect.bottom)
    )
    Flower(random_position, camera_group, chosen_image)
    print("flower just spawned")




money = 0
money_surf = font.render(f"Money: {money}", False, (0,0,0))
money_rect = money_surf.get_rect(center = (900, 45))

camera_group = Camera_group()
hrac = Hrac((1500,1500), camera_group)
cow = Cow((1600, 1600), camera_group)
sheep = Sheep((1300, 1300), camera_group)
ctverec_obchodu = Ctverec_obchodu((255,0,0), 80, 50, 1500, 1200, camera_group)

FLOWER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(FLOWER_EVENT, random.randint(5000, 20000))

running = True

while running:
    
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == FLOWER_EVENT:
            flower_spawn()
            pygame.time.set_timer(FLOWER_EVENT, random.randint(5000, 20000))
    
    hrac.update()

    camera_group.update()
    camera_group.custom_draw(hrac)
    screen.blit(money_surf, money_rect)

    for sprite in camera_group.sprites():
        if isinstance(sprite, Flower) and hrac.rect.colliderect(sprite.rect):
            sprite.kill()
            money += 10
            money_surf = font.render(f"Money: {money}", False, (0,0,0))
    
    if hrac.rect.colliderect(ctverec_obchodu.rect):
        shop = Obchod(hrac) 
        shop.run()
        print("1")
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()

if __name__ == "__main__":
    main()