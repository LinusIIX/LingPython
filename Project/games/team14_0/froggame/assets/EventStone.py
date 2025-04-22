import pygame
import os
from assets import Node, Engine, GameDataLink, AnimatedSprite

#Written by Luca
class EventStone(Node):
    def __init__(self, module, description = "add text", position = (300.0, 300.0), rect_size = (16, 16)):
        #Check if module data is empty if so not playable else can be run change description accordingly 
        super().__init__()
        if module != {}:
            self.runnable = True
            self.pointsInfo = "| not played"
        else:
            self.pointsInfo = "| not playable"
        self.description = description + self.pointsInfo

        self.position = position

        #The EventStone should have on display an animated picture defined here
        sprite_sheet = pygame.image.load(os.path.join(os.getcwd(), "assets", "event_stone.png"))
        frames = Engine.load_sprite_sheet(sprite_sheet, 16, 16, 3)  #16px16p sprites, 2-frame animation
        self.sprite = AnimatedSprite.AnimatedSprite(frames, 100, 100, frame_rate=500) ##Anim import for pygame extended class wired
        self.sprite.animation_region = {"base":[0,1], "noGame" : [2, 2]}
        self.sprite_rect = self.sprite.image.get_rect()
        self.rect_size = rect_size

        #If ES. is running module data is set run in console?, has interface?, display the picture etc.
        if self.runnable:
            self.consoleRun = module["consoleRun"]
            self.modulePath = module["modulePath"]
            self.hasInterface = module["hasInterface"]
            self.moduleData = GameDataLink.init_data()
            self.callProcess = module["displayStone"]
            if module["displayStone"]:
                self.rect_size = self.sprite.image.get_rect().size
            else:
                self.description = description
                
        
    #when runnable add animated sprite part else show grayed out stone
    def process(self, dp):
        if self.runnable:
            self.sprite.update(self.sprite.animation_region["base"])
        else:
            self.sprite.update(self.sprite.animation_region["noGame"])
        dp.blit(self.sprite.image, self.getPos())