import pygame
from pygame.locals import *

class Engine:
    def __init__(self):
        self.nodes = []
        self.running = True
        pygame.init()
        self.dp = pygame.display.set_mode((800, 800), pygame.HWSURFACE | pygame.DOUBLEBUF)
    
    def add_node(self, node):
        self.nodes.append(node)

    def run(self):
        while self.running:
            self.dp.fill((255, 255, 255))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                self.nodes[1].on_event(e, self)
            for node in self.nodes:
                node.process(self.dp)
            pygame.display.flip()
    
    def run_game():
        print("run")