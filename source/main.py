import pygame
import sys
import random
import os
from obchod import Obchod

pygame.init()

pygame.display.set_caption("PyFarm")
screen_size = 1200, 700
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
        self.image = pygame.transform.scale(pygame.image.load("images\clothes\character_pink.png"), (35,80)).convert_alpha()
        self.rect = self.image.get_rect(center = pos) 
        self.direction = pygame.math.Vector2()
        self.money = 100
        self.speed = 5
        self.seeds = {
            'carrot': 3,  
            'wheat': 2   
        }
        self.carrots = 0
        self.wheat = 0
        self.selected_seed = "carrot"
        self.sheep = 1
        self.wool = 0
        self.sheep_placed = False
        self.cow = 0
        self. milk = 0
        self.cow_placed = False
        self.pig = 2
        self.meat = 0 
        self.pig_placed = False 
        
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
        
        if keys[pygame.K_SPACE] and self.seeds[self.selected_seed] > 0: 
            for plot in farm_plots:
                if self.rect.colliderect(plot.rect) and not plot.is_planted:
                    plot.plant_seed(self.selected_seed)  
                    self.seeds[self.selected_seed] -= 1  
                    break
                
        if keys[pygame.K_SPACE]:
            for plot in farm_plots:
                if self.rect.colliderect(plot.rect) and plot.is_planted and plot.growth_stage == 3:
                    harvested_crop = plot.harvest()
                    if harvested_crop == "carrot":
                        self.carrots += 1
                    elif harvested_crop == "wheat":
                        self.wheat += 1
                    break
        
        if keys[pygame.K_SPACE] and self.sheep > 0 and not self.sheep_placed:
            if self.rect.colliderect(sheep_fence.rect):
                sheep.place_in_fence(sheep_fence)  # Use the correct method here
                self.sheep -= 1
                self.sheep_placed = True
        
        if keys[pygame.K_h]: 
            if self.rect.colliderect(sheep.rect) and sheep.harvest_wool():
                self.wool += 1
                
        if keys[pygame.K_c]:  # Press 'C' to select carrot seeds
            self.selected_seed = "carrot"
        if keys[pygame.K_w]:  # Press 'W' to select wheat seeds
            self.selected_seed = "wheat"

        if keys[pygame.K_SPACE] and self.cow > 0 and not self.cow_placed:
            if self.rect.colliderect(cow_fence.rect):
                cow.place_in_fence(cow_fence)
                self.cow -= 1
                self.cow_placed = True
        if keys[pygame.K_h]:
            if self.rect.colliderect(cow.rect) and cow.harvest_milk():
                self.milk += 1
                
        if keys[pygame.K_SPACE] and self.pig > 0 and not self.pig_placed:
            if self.rect.colliderect(pig_fence.rect):
                pig.place_in_fence(pig_fence)  
                self.pig -= 1
                self.pig_placed = True

        if keys[pygame.K_h]:  
            if self.rect.colliderect(pig.rect) and pig.harvest_meat():
                self.meat += 1
                self.pig_placed = False
                    
    def update(self):
        self.input()
        self.rect.center += self.direction
        
        self.rect.left = max(camera_group.map_rect.left, self.rect.left)
        self.rect.right = min(camera_group.map_rect.right, self.rect.right)
        self.rect.top = max(camera_group.map_rect.top, self.rect.top)
        self.rect.bottom = min(camera_group.map_rect.bottom, self.rect.bottom)
                

class Closet:
    def __init__(self, hrac):
        self.hrac = hrac
        self.clothing_images = self.load_clothing_images()
        self.selected_skin = None

    def load_clothing_images(self):
        images = []
        folder_path = "images/Clothes"
        for filename in os.listdir(folder_path):
            if filename.endswith(".png"):
                img = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
                img = pygame.transform.scale(img, (80, 80))
                images.append(img)
        return images

    def display_closet(self, screen):
        screen.fill((220, 220, 220))
        font = pygame.font.Font(None, 42)
        title_surf = font.render("Choose Your Skin", True, (0, 0, 0))
        screen.blit(title_surf, (400, 50))
        
        for idx, img in enumerate(self.clothing_images):
            x = 100 + (idx % 5) * 120
            y = 150 + (idx // 5) * 120
            screen.blit(img, (x, y))
            if img.get_rect(topleft=(x, y)).collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (0, 255, 0), img.get_rect(topleft=(x, y)), 3)

    def run(self, screen):
        closet_open = True
        while closet_open:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for idx, img in enumerate(self.clothing_images):
                        x = 100 + (idx % 5) * 120
                        y = 150 + (idx // 5) * 120
                        if img.get_rect(topleft=(x, y)).collidepoint(event.pos):
                            self.hrac.image = pygame.transform.scale(img, (35, 80))
                            closet_open = False
                            break

            self.display_closet(screen)
            pygame.display.update()
            
class FarmPlot:
    def __init__(self, x, y):
        self.soil_image = pygame.Surface((100, 100))
        self.soil_image.fill((139, 69, 19))
        self.rect = self.soil_image.get_rect(topleft=(x, y))
        self.is_planted = False
        self.growth_stage = -1
        self.growth_timer = 0
        self.crop_type = None

    def plant_seed(self, crop_type):
        if not self.is_planted:
            self.is_planted = True
            self.growth_stage = 0
            self.growth_timer = pygame.time.get_ticks()
            self.crop_type = crop_type
            
    def harvest(self):
        if self.is_planted and self.growth_stage == 3:
            self.is_planted = False
            self.growth_stage = -1
            harvested_crop = self.crop_type  
            self.crop_type = None 
            return harvested_crop  
        return None

    def update(self):
        if self.is_planted:
            current_time = pygame.time.get_ticks()
            if current_time - self.growth_timer > 5000:
                if self.growth_stage < 3:
                    self.growth_stage += 1
                    self.growth_timer = current_time


    def draw(self, surface, camera_pos):
        surface.blit(self.soil_image, self.rect.topleft - camera_pos)
        growth_image = None
        if self.crop_type == "carrot":
            if self.growth_stage == 0:
                growth_image = pygame.image.load("images/seeds/seeds.png").convert_alpha()
            elif self.growth_stage == 1:
                growth_image = pygame.image.load("images/seeds/carrot1.png").convert_alpha()
            elif self.growth_stage == 2:
                growth_image = pygame.image.load("images/seeds/carrot2.png").convert_alpha()
            elif self.growth_stage == 3:
                growth_image = pygame.image.load("images/seeds/carrot3.png").convert_alpha()
        elif self.crop_type == "wheat":
            if self.growth_stage == 0:
                growth_image = pygame.image.load("images/seeds/seeds.png").convert_alpha()
            elif self.growth_stage == 1:
                growth_image = pygame.image.load("images/seeds/wheat1.png").convert_alpha()
            elif self.growth_stage == 2:
                growth_image = pygame.image.load("images/seeds/wheat2.png").convert_alpha()
            elif self.growth_stage == 3:
                growth_image = pygame.image.load("images/seeds/wheat3.png").convert_alpha()

        if growth_image:
            growth_image = pygame.transform.scale(growth_image, (100, 100))
            surface.blit(growth_image, self.rect.topleft - camera_pos)


class CowFence(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y, group):
        super().__init__(group)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

class Cow(pygame.sprite.Sprite):
    def __init__(self, fence, group):
        super().__init__(group)
        self.image_milk = pygame.image.load("images/milk.png")
        self.image_without_milk = pygame.transform.scale(pygame.image.load("images/cow.png"), (125, 80)).convert_alpha()
        self.image = self.image_without_milk
        self.rect = self.image.get_rect(center=(-1000, -100))
        self.has_milk = False
        self.growth_timer = pygame.time.get_ticks()
        
    def place_in_fence(self, fence):
        self.rect.center = fence.rect.center
        self.has_milk = False
        self.image = self.image_without_milk
        self.growth_timer = pygame.time.get_ticks()
    def harvest_milk(self):
        if self.has_milk:
            self.has_milk = False
            self.image = self.image_without_milk
            self.growth_timer = pygame.time.get_ticks()
            return True
        return False

    def update(self):
        if not self.has_milk:
            current_time = pygame.time.get_ticks()
            if current_time - self.growth_timer > 10000:
                self.has_milk = True
                self.image = self.image_milk

class SheepFence(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y, group):
        super().__init__(group)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))           
        
class Sheep(pygame.sprite.Sprite):
    def __init__(self, fence, group):
        super().__init__(group)
        self.image_with_wool = pygame.transform.scale(pygame.image.load("images/sheep.png"), (125, 80)).convert_alpha()
        self.image_without_wool = pygame.transform.scale(pygame.image.load("images/bald-sheep-opraveno.png"), (125, 80)).convert_alpha()
        self.image = self.image_with_wool
        self.rect = self.image.get_rect(center=(-1000, -100))
        self.has_wool = True
        self.growth_timer = pygame.time.get_ticks()
    
    def place_in_fence(self, fence):
        self.rect.center = fence.rect.center
        self.has_wool = True
        self.image = self.image_with_wool

    def harvest_wool(self):
        if self.has_wool:
            self.has_wool = False
            self.image = self.image_without_wool
            self.growth_timer = pygame.time.get_ticks()
            return True
        return False
    
    def update(self):
        if not self.has_wool:
            current_time = pygame.time.get_ticks()
            if current_time - self.growth_timer > 10000:
                self.has_wool = True
                self.image = self.image_with_wool

class PigFence(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y, group):
        super().__init__(group)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

class Pig(pygame.sprite.Sprite):
    def __init__(self, fence, group):
        super().__init__(group)
        self.image_pig = pygame.transform.scale(pygame.image.load("images/pig.png"), (125, 80)).convert_alpha()
        self.image_meat = pygame.image.load("images/meat.png").convert_alpha()
        self.image = self.image_pig 
        self.rect = self.image.get_rect(center=(-1000, -100))
        self.is_ready = False
        self.growth_timer = pygame.time.get_ticks()
        self.harvested = False
    
    def place_in_fence(self, fence):
        self.rect.center = fence.rect.center
        self.is_ready = False
        self.harvested = False 
        self.image = self.image_pig
        self.growth_timer = pygame.time.get_ticks()
        
    def harvest_meat(self):
        if self.is_ready and not self.harvested:
            self.harvested = True 
            self.rect.center=(-1000, -100)
            return True
        return False
    
    def update(self):
        if not self.is_ready and not self.harvested:
            current_time = pygame.time.get_ticks()
            if current_time - self.growth_timer > 10000: 
                self.is_ready = True
                self.image = self.image_meat
        
        
class Ctverec_obchodu(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(pygame.image.load("images/shop.png"), (100,80))
        self.rect = self.image.get_rect(topleft=(1550, 1500))


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


camera_group = Camera_group()
hrac = Hrac((1400,1200), camera_group)

farm_plot_positions = [
    (200, 300),  # First plot position
    (350, 300),  # Second plot position
    (500, 300),  # Third plot position
    (650, 300),  # Fourth plot position
    (800, 300),   # Fifth plot position
    (950, 300)   # Sixth plot position
]

farm_plots = [FarmPlot(x, y) for x, y in farm_plot_positions]

sheep_fence = SheepFence((150, 100, 30), 150, 150, 900, 1200, camera_group)
sheep = Sheep(sheep_fence, camera_group)

ctverec_obchodu = Ctverec_obchodu(camera_group)
cow_fence = CowFence((200, 100, 50), 150, 150, 900, 1400, camera_group) 
cow = Cow(cow_fence, camera_group)
pig_fence = PigFence((180, 50, 50), 150, 150, 900, 1600, camera_group)
pig = Pig(pig_fence, camera_group)
closet_button = pygame.Rect(850, 10, 100, 40)
carrot_seed_image = pygame.image.load('images/seeds/carrot_seeds.png')
carrot_seed_image = pygame.transform.scale(carrot_seed_image, (40, 40))

milk_image = pygame.transform.scale(pygame.image.load("images/milk.png"), (30,40))
meat_image = pygame.transform.scale(pygame.image.load("images/meat.png"), (40,40))
sheep_image = pygame.transform.scale(pygame.image.load("images/sheep.png"), (40,30))
cow_image = pygame.transform.scale(pygame.image.load("images/cow.png"), (40,30))
pig_image = pygame.transform.scale(pygame.image.load("images/pig.png"), (40,30))

wheat_seed_image = pygame.image.load('images/seeds/wheat_seeds.png')
wheat_seed_image = pygame.transform.scale(wheat_seed_image, (30, 30))

FLOWER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(FLOWER_EVENT, random.randint(5000, 20000))


running = True


while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if closet_button.collidepoint(event.pos):
                closet = Closet(hrac)
                closet.run(screen)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if hrac.seeds[hrac.selected_seed] > 0:
                    for plot in farm_plots:
                        if hrac.rect.colliderect(plot.rect) and not plot.is_planted:
                            plot.plant_seed(hrac.selected_seed)
                            hrac.seeds[hrac.selected_seed] -= 1
                            break
        elif event.type == FLOWER_EVENT:
            flower_spawn()
            pygame.time.set_timer(FLOWER_EVENT, random.randint(5000, 20000))
    
    
    hrac.update()

    camera_group.update()
    camera_group.custom_draw(hrac)

    for plot in farm_plots:
        plot.update()
        plot.draw(camera_group.display_surface, camera_group.posun)

    seeds_surf = font.render(f"Carrot Seeds: {hrac.seeds['carrot']}", False, (0, 0, 0))
    screen.blit(seeds_surf, (50, 320))
    screen.blit(carrot_seed_image, (10,315))

    wheat_seeds_surf = font.render(f"Wheat Seeds: {hrac.seeds['wheat']}", False, (0, 0, 0))
    screen.blit(wheat_seeds_surf, (50, 30))
    screen.blit(wheat_seed_image, (10,25))

    selected_seed_surf = font.render(f"Selected Seed: {hrac.selected_seed.capitalize()}", False, (0, 0, 0))
    screen.blit(selected_seed_surf, (10, 650))

    money_surf = font.render(f"Money: {hrac.money}", False, (0,0,0))
    money_rect = money_surf.get_rect(center = (1100, 45))
    screen.blit(money_surf, money_rect)

    carrots_surf = font.render(f"Carrots: {hrac.carrots}", False, (0, 0, 0))
    carrots_rect = carrots_surf.get_rect(topleft=(10, 240))
    screen.blit(carrots_surf, carrots_rect)
    
    wheat_surf = font.render(f"Wheat: {hrac.wheat}", False, (0, 0, 0))
    wheat_rect = wheat_surf.get_rect(topleft=(10, 280))
    screen.blit(wheat_surf, wheat_rect)
    
    camera_group.display_surface.blit(hrac.image, hrac.rect.topleft - camera_group.posun)
    
    sheep.update()
    cow.update()
    cow.update()
    wool_surf = font.render(f"Wool: {hrac.wool}", False, (0, 0, 0))
    screen.blit(wool_surf, (10, 70))
    
    sheep_surf = font.render(f"Sheep: {hrac.sheep}", False, (0, 0, 0))
    screen.blit(sheep_surf, (50, 110))
    screen.blit(sheep_image, (8,105))

    milk_surf = font.render(f"Milk: {hrac.milk}", False, (0, 0, 0))
    screen.blit(milk_surf, (50, 150))
    screen.blit(milk_image, (10,140))

    cow_surf = font.render(f"Cow: {hrac.cow}", False, (0, 0, 0))
    screen.blit(cow_surf, (50, 190))
    screen.blit(cow_image, (8,189))

    pig_surf = font.render(f"Pig: {hrac.pig}", False, (0, 0, 0))
    screen.blit(pig_surf, (50, 410))
    screen.blit(pig_image, (8,406))
    
    meat_surf = font.render(f"Meat: {hrac.meat}", False, (0, 0, 0))
    screen.blit(meat_surf, (55, 370))
    screen.blit(meat_image, (10,360))
    
    closet_button = pygame.Rect(1050, 200, 150, 50)
    pygame.draw.rect(screen, (250, 200, 200), closet_button)
    closet_button_text = font.render("Closet", True, (255, 255, 255))
    screen.blit(closet_button_text, closet_button.topleft)
    
    for sprite in camera_group.sprites():
        if isinstance(sprite, Flower) and hrac.rect.colliderect(sprite.rect):
            sprite.kill()
            hrac.money += 10
            money_surf = font.render(f"Money: {hrac.money}", False, (0, 0, 0))
    
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