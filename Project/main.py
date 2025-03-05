from assets import Engine, Node, GameDataLink, globals
from assets.Player import Player  # Corrected import
import pygame
import os
from pygame.locals import *


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

    def process(self, dp):
        pygame.draw.rect(dp, (50, 50, 50), (self.getX(), self.getY(), self.rect_size[0], self.rect_size[1]))
        self.nameRect.center = (self.getX() + self.rect_size[0] * 0.5, self.getY() + self.rect_size[1] * 0.5)
        dp.blit(self.displayName, self.nameRect)

engine = Engine()
root = Node(handlesEvents=False, nodeRefs={}, callProcess=False)
player = Player(handlesEvents=True, nodeRefs={
    "root" : root
})
player.rect_size = (globals.game_size*player.sprite_rect.width,globals.game_size*player.sprite_rect.height)
print(player.rect_size)
i = 100
for gameEntry in Engine.get_main_files("games"):
    if globals.debug:
        print(gameEntry)
    root.add_node(EventStone(gameEntry, (300, i)))
    i += 100
engine.add_node(root)
engine.add_node(player)
engine.run()