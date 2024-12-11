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
        self.sheep_message_time = None 
        self.max_cow_surf = self.font.render("You already have a cow!", False, (0, 0, 0))
        self.cow_message_time = None
        self.running = True
        self.items = [  # Nabídka obchodu: (název, cena, atribut hráče, obrázek nebo text)
            {"name": "Carrot Seeds", "price": 10, "attribute": "carrot_seeds"},
            {"name": "Wheat Seeds", "price": 20, "attribute": "wheat_seeds"},
            {"name": "Potato Seeds", "price": 40, "attribute": "potato_seeds"},
            {"name": "Sheep", "price": 60, "attribute": "sheep"},
            {"name": "Cow", "price": 80, "attribute": "cow"},
            {"name": "Pig", "price": 100, "attribute": "pig"},
            {"name": "Money", "price": 50, "attribute": "money"}
        ]
    
    def sell_items(self):
        if self.hrac.carrots > 0:
            self.hrac.money += self.hrac.carrots * 15
            self.hrac.carrots = 0
        if self.hrac.wheat > 0:
            self.hrac.money += self.hrac.wheat * 25
            self.hrac.wheat = 0
        if self.hrac.potatoes > 0:
            self.hrac.money += self.hrac.potatoes * 45
            self.hrac.potatoes = 0
        if self.hrac.wool > 0:
            self.hrac.money += self.hrac.wool * 10
            self.hrac.wool = 0
        if self.hrac.milk > 0:
            self.hrac.money += self.hrac.milk * 20
            self.hrac.milk = 0
        if self.hrac.meat > 0:
            self.hrac.money += self.hrac.meat * 120
            self.hrac.meat = 0
    
    def display_items(self):
        for idx, item in enumerate(self.items):
            x = 100
            y = 10 + idx * 100
            width = 400
            height = 80
        
            pygame.draw.rect(self.screen, (174, 198, 255), (x, y, width, height))
            pygame.draw.rect(self.screen, (106, 139, 204), (x, y, width, height), 2)
            
            text = f"{item['name']} - {item['price']} money"
            text_surf = self.font.render(text, True, (0, 0, 0))
            self.screen.blit(text_surf, (x + 10, y + 25))
            
    def check_click(self, pos):
        for idx, item in enumerate(self.items):
            x = 100
            y = 10 + idx * 100
            width = 400
            height = 80

            if x <= pos[0] <= x + width and y <= pos[1] <= y + height:
                if self.hrac.money >= item["price"]:
                    if item["attribute"] == "carrot_seeds":
                        self.hrac.seeds['carrot'] += 1 
                        self.hrac.money -= item["price"]
                    elif item["attribute"] == "wheat_seeds":
                        self.hrac.seeds['wheat'] += 1
                        self.hrac.money -= item["price"]
                    elif item["attribute"] == "potato_seeds":
                        self.hrac.seeds['potato'] += 1
                        self.hrac.money -= item["price"]
                    elif item["attribute"] == "sheep":
                        if self.hrac.sheep_placed > 0 or self.hrac.sheep > 0:
                            #print("You already have a sheep!")
                            self.sheep_message_time = pygame.time.get_ticks()
                        else:
                            self.hrac.sheep += 1 
                            self.hrac.money -= item["price"]
                    elif item["attribute"] == "cow":
                        if self.hrac.cow_placed > 0 or self.hrac.cow > 0:
                            #print("You already have a cow!")
                            self.cow_message_time = pygame.time.get_ticks()
                        else:
                            self.hrac.cow += 1 
                            self.hrac.money -= item["price"]
                    elif item["attribute"] == "pig":
                        self.hrac.pig += 1
                        self.hrac.money -= item["price"]
                elif self.hrac.special_money >= item["price"]:
                    if item["attribute"] == "money":
                        self.hrac.money += 10
                        self.hrac.special_money -= item["price"]
    
    def run(self):
        while self.running:
            self.screen.fill((235, 235, 255))
            self.display_items() 
            self.sell_items()

            if self.sheep_message_time and pygame.time.get_ticks() - self.sheep_message_time < 5000:
                self.screen.blit(self.max_sheep_surf, (600, 50))
            elif self.sheep_message_time and pygame.time.get_ticks() - self.sheep_message_time >= 5000:
                self.sheep_message_time = None
            
            if self.cow_message_time and pygame.time.get_ticks() - self.cow_message_time < 5000:
                self.screen.blit(self.max_cow_surf, (604, 110))
            elif self.cow_message_time and pygame.time.get_ticks() - self.cow_message_time >= 5000:
                self.cow_message_time = None
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                    self.check_click(event.pos)

            money_surf = self.font.render(f"Money: {self.hrac.money}", False, (0,0,0))
            money_rect = money_surf.get_rect(center = (1100, 45))
            self.screen.blit(money_surf, money_rect)

            special_money_surf = self.font.render(f"Special money: {self.hrac.special_money}", False, (0,0,0))
            special_money_rect = special_money_surf.get_rect(center = (1045, 80))
            self.screen.blit(special_money_surf, special_money_rect)

            special_surf = self.font.render("50 special money for 10 normal money", False, (0,0,0))
            special_rect = special_surf.get_rect(center = (800, 650))
            self.screen.blit(special_surf, special_rect)


            pygame.display.update()
            self.clock.tick(60)
        
        self.hrac.rect.topleft = (self.hrac.rect.x + 150, self.hrac.rect.y)
        pygame.display.set_mode((1200,700))
        return self.hrac.money, self.hrac.special_money

