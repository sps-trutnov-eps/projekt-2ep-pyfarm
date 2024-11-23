import pygame
import sys

class Obchod:
    def __init__(self, hrac):
        pygame.init()
        self.hrac = hrac
        self.screen_size = 1200, 700
        self.screen = pygame.display.set_mode(self.screen_size)
        self.font = pygame.font.Font(None, 40)
        self.clock = pygame.time.Clock()
        self.max_sheep_surf = self.font.render("You already have a sheep!", False, (0, 0, 0))
        #self.sheep_max_timer = pygame.time.get_ticks()
        self.running = True
        self.items = [  # Nabídka obchodu: (název, cena, atribut hráče, obrázek nebo text)
            {"name": "Carrot Seeds", "price": 10, "attribute": "carrot_seeds"},
            {"name": "Wheat Seeds", "price": 20, "attribute": "wheat_seeds"},
            {"name": "Sheep", "price": 60, "attribute": "sheep"},
            {"name": "Cow", "price": 80, "attribute": "cow"},
            {"name": "Pig", "price": 100, "attribute": "pig"}
        ]
    
    def sell_items(self):
        if self.hrac.carrots > 0:
            self.hrac.money += self.hrac.carrots * 15
            self.hrac.carrots = 0
        if self.hrac.wheat > 0:
            self.hrac.money += self.hrac.wheat * 25
            self.hrac.wheat = 0
        if self.hrac.wool > 0:
            self.hrac.money += self.hrac.wool * 10
            self.hrac.wool = 0
        if self.hrac.milk > 0:
            self.hrac.money += self.hrac.milk * 20
            self.hrac.milk = 0
        if self.hrac.meat > 0:
            self.hrac.money += self.hrac.meat * 40
            self.hrac.meat = 0
    
    def display_items(self):
        for idx, item in enumerate(self.items):
            x = 100
            y = 50 + idx * 100
            width = 350
            height = 80
        
            pygame.draw.rect(self.screen, (174, 198, 255), (x, y, width, height))
            pygame.draw.rect(self.screen, (106, 139, 204), (x, y, width, height), 2)
            
            text = f"{item['name']} - {item['price']} money"
            text_surf = self.font.render(text, True, (0, 0, 0))
            self.screen.blit(text_surf, (x + 10, y + 25))
            
    def check_click(self, pos):
        for idx, item in enumerate(self.items):
            x = 100
            y = 50 + idx * 100
            width = 350
            height = 80

            if x <= pos[0] <= x + width and y <= pos[1] <= y + height:
                if self.hrac.money >= item["price"]:
                    if item["attribute"] == "carrot_seeds":
                        self.hrac.seeds['carrot'] += 1 
                        self.hrac.money -= item["price"]
                    elif item["attribute"] == "wheat_seeds":
                        self.hrac.seeds['wheat'] += 1
                        self.hrac.money -= item["price"]
                    elif item["attribute"] == "sheep":
                        if self.hrac.sheep_placed > 0 or self.hrac.sheep > 0:
                            print("You already have a sheep!")
                            self.screen.blit(self.max_sheep_surf, (670, 10))
                        else:
                            self.hrac.sheep += 1 
                            self.hrac.money -= item["price"]
                    elif item["attribute"] == "cow":
                        if self.hrac.cow_placed > 0 or self.hrac.cow > 0:
                            print("You already have a cow!")
                        else:
                            self.hrac.cow += 1 
                            self.hrac.money -= item["price"]
                    elif item["attribute"] == "pig":
                        self.hrac.pig += 1
                        self.hrac.money -= item["price"]
    
    def run(self):
        while self.running:
            self.screen.fill((235, 235, 255))
            self.display_items() 
            self.sell_items()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                    self.check_click(event.pos)

            money_surf = self.font.render(f"Money: {self.hrac.money}", False, (0,0,0))
            money_rect = money_surf.get_rect(center = (1100, 45))
            self.screen.blit(money_surf, money_rect)


            pygame.display.update()
            self.clock.tick(60)
        
        self.hrac.rect.topleft = (self.hrac.rect.x + 150, self.hrac.rect.y)
        pygame.display.set_mode((1200,700))
        return self.hrac.money

