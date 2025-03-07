import pygame
import os
from assets import Node, globals


class BackGround(Node):
    def __init__(self, position = (0.0, 0.0)):
        super().__init__()
        BASE_DIR = os.getcwd()
        self.position = position
        self.sprite = pygame.image.load(os.path.join(BASE_DIR, "assets" ,"maybe_map.png"))
        self.sprite_size = self.sprite.get_rect()
        self.sprite = pygame.transform.scale(self.sprite, (globals.game_size * self.sprite_size.width, globals.game_size * self.sprite_size.height))
        self.rect = self.sprite.get_rect()

        self.obstacle_map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        for i in range(len(self.obstacle_map)):  # Loop through rows
            for j in range(len(self.obstacle_map[i])):  # Loop through columns
                if self.obstacle_map[i][j] == 1:
                    obstacle = Node(callProcess=False)
                    obstacle.position = (16*globals.game_size * j,16*globals.game_size * i)
                    obstacle.rect_size = (16*globals.game_size,16*globals.game_size)
                    self.add_node(obstacle)
                value = self.obstacle_map[i][j]
                if globals.debug:
                    print(f"Row {i}, Col {j}: {value}")

    
    def process(self, dp):
        self.rect.center = (self.getX() + self.rect_size[0] * 0.5, self.getY() + self.rect_size[1] * 0.5)
        dp.blit(self.sprite,self.rect)