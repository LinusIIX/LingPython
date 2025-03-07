import pygame
import os
from assets import Node, globals


class BackGround(Node):
    def __init__(self, position = (0.0, 0.0)):
        super().__init__()
        BASE_DIR = os.getcwd()
        #self.position =(650, 600) #Startposition
        self.offsetPos = (0,0)
        self.sprite = pygame.image.load(os.path.join(BASE_DIR, "assets", "maybe_map.png"))
        self.sprite_size = self.sprite.get_rect()
        self.sprite = pygame.transform.scale(self.sprite, (globals.game_size * self.sprite_size.width, globals.game_size * self.sprite_size.height))
        self.rect = self.sprite.get_rect()
        self.rect = self.rect.move((self.rect.height)/2,(self.rect.width)/2) #Nicht anfassen, funktioniert ((dimension of image)/2)

        self.obstacle_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
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

    
    def process(self, dp):
        self.rect.center = (self.getX() + self.rect_size[0] * 0.5, self.getY() + self.rect_size[1] * 0.5)
        dp.blit(self.sprite,self.rect)