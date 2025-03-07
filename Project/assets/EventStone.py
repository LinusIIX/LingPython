import pygame
import os
from assets import Node, Engine, GameDataLink, AnimatedSprite

class EventStone(Node):
    def __init__(self, module, description = "add text", position = (300.0, 300.0)):
        super().__init__()
        self.moduleName = module["moduleFolderName"]
        self.consoleRun = module["consoleRun"]
        self.modulePath = module["modulePath"]
        self.moduleData = GameDataLink.init_data()
        self.description = description
        self.position = position

        sprite_sheet = pygame.image.load(os.path.join(os.getcwd(), "assets", "event_stone.png"))
        frames = Engine.load_sprite_sheet(sprite_sheet, 16, 16, 2)  #16px16p sprites, 16-frame animation
        self.sprite = AnimatedSprite.AnimatedSprite(frames, 100, 100, frame_rate=500) ##Anim import for pygame extended class wired
        self.sprite.animation_region = {"base":[0,1]}
        self.sprite_rect = self.sprite.image.get_rect()
        self.rect_size = self.sprite.image.get_rect().size

    def process(self, dp):
        self.sprite.update(self.sprite.animation_region["base"])
        dp.blit(self.sprite.image, self.getPos())
        #pygame.draw.rect(dp, (50, 50, 50), (self.getX(), self.getY(), self.rect_size[0], self.rect_size[1]))
        #self.nameRect.center = (self.getX() + self.rect_size[0] * 0.5, self.getY() + self.rect_size[1] * 0.5)
        #dp.blit(self.displayName, self.nameRect)