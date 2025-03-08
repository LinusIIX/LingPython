import pygame
import os
from assets import Node

class Interactable(Node):
    def __init__(self, description="add text", position=(300.0, 300.0), pickup=True,nodeRefs = {},requires = "nothing",callProcess=False,handlesEvents=True):
        super().__init__()  
        self.description = description
        self.position = position
        self.pickup = pickup  
        self.nodeRefs = nodeRefs
        self.callProcess = False
        self.handlesEvents = True
        self.interactable = True
        self.requires = requires
        self.contains = []
         

    def interact(self,player):
        if self.pickup and player.holding == self.requires:
            # You could maybe start the minigame here
            player.holding = self.description
        else:
            if self.description.startswith("altar") and (player.holding != "nothing"):
                self.contains.append(player.holding)
                player.holding = "nothing"
            elif self.description.startswith("fire"):
                if player.holding == "fish":
                    player.holding = "cooked fish"
                elif player.holding == "frog":
                    player.holding = "cooked frog"

    def process(self, dp):
        print(self.position)
