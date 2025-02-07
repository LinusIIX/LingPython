from assets import Engine, Node
import pygame
from pygame.locals import *


class Player(Node):

    def __init__(self):
        self.position = (30.0, 30.0)
        self.moveInput = [False, False, False, False]
        self.SPEED = 0.5
    
    def process(self, dp):
        hori = self.moveInput[2] - self.moveInput[0]
        vert = self.moveInput[3] - self.moveInput[1]
        self.position = (self.position[0] + vert * self.SPEED, self.position[1] + hori * self.SPEED)
        pygame.draw.rect(dp, (50, 50, 200), (self.position[0], self.position[1], 64, 64))
    
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
                engine.run_game()
        

class EventStone(Node):
    def __init__(self):
        self.position = (300.0, 300.0)

    def process(self, dp):
        pygame.draw.rect(dp, (50, 50, 50), (self.position[0], self.position[1], 32, 32))


engine = Engine()
player = Player()
eventStone = EventStone()
engine.add_node(eventStone)
engine.add_node(player)
engine.run()