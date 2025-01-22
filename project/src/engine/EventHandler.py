from typing import Callable, Dict
import pygame
from pygame.locals import *

class EventHandler:
    def __init__(self):
        self.inputMap : Dict[int, Callable[[e], None]] = {}
    
    def add_input(input : int, on_input : Callable[[e], None]):
      self.inputMap[input] = on_input