import pygame
import os
from assets import Node, Engine, globals


#Textdisplay so that text for the stones gets displayed
#Writen by Luca
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
            texts = self.curNode.description.split("\n")
            for idx, text in enumerate(texts):
                self.description = self.font.render(text, True, (240, 240, 255), (50, 50, 0))
                textRect = pygame.Rect(400 - len(text) * globals.game_size * 1.4, 750 - len(texts) * 50 + idx * 50, 800, len(text) * globals.game_size * 1.4)
                dp.blit(self.description, textRect)
                if not Engine.check_collision(self.curNode.getPos(), self.curNode.rect_size, self.nodeRefs["player"]):
                    self.curNode = None
                    break
