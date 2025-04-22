# game_logic.py
# Author: Mojtaba Malek-Nejad
# if you want to see more detailed information about the individual contributors of the code files, 
# please have a look at the "contributors.txt" file (in the "project" directory)

import random

class GameLogic:
    def __init__(self):
        self.inscription = "Decode the secrets of the hidden doorway"
        self.clues = []
        self.hero_position = (0, 0)

    def add_clue(self, clue):
        self.clues.append(clue)

    def check_inscription(self, user_input):
        return user_input.lower() == self.inscription.lower()

    def move_hero(self, direction):
        x, y = self.hero_position
        if direction == "up":
            self.hero_position = (x, y - 1)
        elif direction == "down":
            self.hero_position = (x, y + 1)
        elif direction == "left":
            self.hero_position = (x - 1, y)
        elif direction == "right":
            self.hero_position = (x + 1, y)

    def get_clue_count(self):
        return len(self.clues)

    def reset_game(self):
        self.clues.clear()
        self.hero_position = (0, 0)