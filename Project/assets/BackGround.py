import pygame
import os
from assets import Node, globals
from assets.interactable import Interactable



class BackGround(Node):
    def __init__(self, position = (0.0, 0.0),nodeRefs = {}):
        super().__init__()
        BASE_DIR = os.getcwd()
        self.nodeRefs = nodeRefs
        self.position =(650, 600) #Startposition
        self.offsetPos = (0,0)
        self.sprite = pygame.image.load(os.path.join(BASE_DIR, "assets", "maybe_map.png"))
        self.sprite_size = self.sprite.get_rect()
        self.sprite = pygame.transform.scale(self.sprite, (globals.game_size * self.sprite_size.width, globals.game_size * self.sprite_size.height))
        self.rect = self.sprite.get_rect()
        self.rect = self.rect.move((self.rect.height)/2,(self.rect.width)/2) #Nicht anfassen, funktioniert ((dimension of image)/2)

        self.obstacle_map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        for i in range(len(self.obstacle_map)):  # Loop through rows
            for j in range(len(self.obstacle_map[i])):  # Loop through columns
                if self.obstacle_map[i][j] == 1:
                    obstacle = Node(callProcess=False)
                    obstacle.offsetPos = (0,0)
                    obstacle.position = ( -self.rect.top + (self.rect.width/17) * j,-self.rect.left + (self.rect.height/12) * i)
                    obstacle.rect_size = (self.rect.width/17,self.rect.height/12)
                    print(obstacle.rect_size)
                    self.add_node(obstacle)
                value = self.obstacle_map[i][j]
                if globals.debug:
                    print(f"Row {i}, Col {j}: {value}")
        #place interactables in extra node so that they dont get checked with player collision (alternative, another variable in node)
        interactable_container = Node(callProcess=False)
        interactable_container.position = (1000,1000)
        self.add_node(interactable_container)

        altar_1 = Interactable(description="altar_1", nodeRefs=self.nodeRefs, pickup=False)
        altar_1.position = ( -self.rect.top + (self.rect.width/17) * 5,-self.rect.left + (self.rect.height/12) * 3)
        altar_1.rect_size = ((self.rect.width/17) * 1.5,(self.rect.width/17) * 1.5)
        self.add_node(altar_1)
        print(altar_1.position)

        altar_2 = Interactable(description = "altar_2", nodeRefs=self.nodeRefs, pickup=False)
        frog = Interactable(description = "frog", nodeRefs=self.nodeRefs, pickup=True)
        fish = Interactable(description = "fish", nodeRefs=self.nodeRefs, pickup=True)
        net = Interactable(description = "net", nodeRefs=self.nodeRefs, pickup=True)
        fireplace = Interactable(description = "fireplace", nodeRefs=self.nodeRefs, pickup=True)
        #interactable_container.add_node(altar_1)
        #interactable_container.add_node(altar_2)
        #interactable_container.add_node(frog)
        #interactable_container.add_node(fish)
        #interactable_container.add_node(net)
        #interactable_container.add_node(fireplace)
        


    def process(self, dp):
        self.rect.center = (self.getX() + self.rect_size[0] * 0.5, self.getY() + self.rect_size[1] * 0.5)
        dp.blit(self.sprite,self.rect)