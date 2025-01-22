import pygame
from pygame.locals import *
from engine import EventHandler

class Engine:
  def __init__(self, xRes = 400, yRes = 400):
    print(xRes, yRes)
    pygame.display.set_mode((xRes, yRes), pygame.HWSURFACE | pygame.DOUBLEBUF)
    self.eventHandler = EventHandler()
    self.eventHandler.add_input(pygame.QUIT, lambda event : pygame.event.Event: 
                                )
  
  def start(self):
    print("start game")

    while (True):
      for e in pygame.event.get():
        if e.type == pygame.QUIT:
          return


  def add_root(self, node):
    self.root = node
