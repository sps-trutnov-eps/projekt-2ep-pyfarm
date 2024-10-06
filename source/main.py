import pygame
import sys

pygame.init()

pygame.display.set_caption("PyFarm")
screen_size = 1000, 600
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()


class Camera_group(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        
        self.posun = pygame.math.Vector2()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        
        self.map_surf = pygame.image.load("images/mapa1.png").convert_alpha()
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
        self.image = pygame.image.load("images/postava1.png").convert_alpha()
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


class Ctverec_obchodu(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y, group):
        super().__init__(group)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x,y))


camera_group = Camera_group()
hrac = Hrac((1500,1500), camera_group)
ctverec_obchodu = Ctverec_obchodu((255,0,0), 100, 50, 1500, 1200, camera_group)

running = True

while running:
    
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    hrac.update()

    camera_group.update()
    camera_group.custom_draw(hrac)
    
    if hrac.rect.colliderect(ctverec_obchodu.rect):
        print("obchod otevřen")
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()