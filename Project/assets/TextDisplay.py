import pygame
import os
from assets import Node, Engine, globals

class TextDisplay(Node):
    def __init__(self, handlesEvents=False, nodeRefs=..., callProcess=True):
        super().__init__(handlesEvents, nodeRefs, callProcess)
        self.curNode = None

        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.description = self.font.render("text", True, (0, 255, 255), (0, 0, 255))
        #self.nameRect = self.description.get_rect()

    def process(self, dp):
        if self.curNode is None:
            for collider in (self.nodeRefs["eventStoneContainer"].children):
                if Engine.check_collision(collider.getPos(), collider.rect_size, self.nodeRefs["player"]):
                    self.curNode = collider
        else:
            self.description = self.font.render(self.curNode.description, True, (240, 240, 255), (50, 50, 0))
            #textRect = pygame.Rect(400 - len(self.curNode.description) * globals.game_size * 1.45, 750, 800, len(self.curNode.description) * globals.game_size * 1.45)
            pygame.draw.rect(dp, (50, 50, 50), textRect)
            dp.blit(self.description, textRect)
            if not Engine.check_collision(self.curNode.getPos(), self.curNode.rect_size, self.nodeRefs["player"]):
                self.curNode = None
