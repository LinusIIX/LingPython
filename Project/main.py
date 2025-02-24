from assets import Engine, Node, GameDataLink
import pygame
import os
from pygame.locals import *


class Player(Node):

    def __init__(self, handlesEvents):
        super().__init__(handlesEvents)
        self.position = (30.0, 30.0)
        self.moveInput = [False, False, False, False]
        self.SPEED = 0.5
        self.sprite = pygame.image.load(os.path.join(BASE_DIR, "assets", "Frog_pure.png"))
        self.sprite_rect = self.sprite.get_rect()
        print(self.sprite.get_rect())
    
    def process(self, dp):
        hori = self.moveInput[2] - self.moveInput[0]
        vert = self.moveInput[3] - self.moveInput[1]
        self.position = (self.position[0] + vert * self.SPEED, self.position[1] + hori * self.SPEED)
        pygame.draw.rect(dp, (50, 50, 200), (self.position[0], self.position[1], self.rect_size[0], self.rect_size[1]))
        dp.blit(self.sprite, (self.position[0] - self.sprite_rect.centery, self.position[1] - self.sprite_rect.centerx))

    def on_event(self, e, engine):
        if e.type == pygame.KEYDOWN:
            i = 0
            for key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                if e.key == key:
                    self.moveInput[i] = True
                i += 1
        if e.type == pygame.KEYUP:
            i = 0
            for key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                if e.key == key:
                    self.moveInput[i] = False
                i += 1
            if e.key == pygame.K_e:
                engine.interact(self)
        

class EventStone(Node):
    def __init__(self, module, position = (300.0, 300.0)):
        super().__init__()
        self.position = position
        self.rect_size = (32, 32)
        self.moduleName = module["moduleFolderName"]
        self.modulePath = module["modulePath"]
        self.moduleData = GameDataLink.init_data()

        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.displayName = self.font.render(self.moduleName, True, (0, 255, 255), (0, 0, 255))
        self.nameRect = self.displayName.get_rect()
        self.rect_size = (self.nameRect[2], self.nameRect[3])
        self.nameRect.center = (self.position[0], self.position[1])
        self.position = (self.position[0] - self.rect_size[0] * 0.5, self.position[1] - self.rect_size[1] * 0.5)

    def process(self, dp):
        pygame.draw.rect(dp, (50, 50, 50), (self.position[0], self.position[1], self.rect_size[0], self.rect_size[1]))
        dp.blit(self.displayName, self.nameRect)

BASE_DIR = os.path.dirname(__file__)
engine = Engine()
player = Player(handlesEvents=True)
print(player.rect_size)
i = 100
for gameEntry in Engine.get_main_files("games"):
    print(gameEntry)
    engine.add_node(EventStone(gameEntry, (300, i)))
    i += 100
engine.add_node(player)
engine.run()