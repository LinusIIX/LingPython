# constants.py
# Author: Max Weber
# if you want to see more detailed information about the individual contributors of the code files, 
# please have a look at the "contributors.txt" file (in the "project" directory)

import pygame as pg

# Color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Button constants
BUTTON_PADDING = 20
BUTTON_CORNER_RADIUS = 10
BUTTON_SPACING = 70
DEFAULT_BUTTON_X = 40

# Font sizes (relative to screen height)
TITLE_FONT_SIZE_FACTOR = 8  # HEIGHT // 8
BUTTON_FONT_SIZE_FACTOR = 20  # HEIGHT // 20 - Zurück zum ursprünglichen Wert
GAME_FONT_SIZE_FACTOR = 10  # HEIGHT // 10 - Zurück zum ursprünglichen Wert

# Button states colors
STONE_COLORS = {
    'normal': (1, 1, 1),        # Multiplier für normale Ansicht
    'hover': (1.15, 1.15, 1.15),  # Leicht heller
    'selected': (0.85, 0.85, 0.85), # Leicht dunkler
    'border': (25, 25, 25),      # Dunkle Kanten
    'shadow': (0, 0, 0)          # Schwarz für Schatten
}

# Text constants
TEXT_COLOR = (255, 255, 255)  # Weiß
TEXT_SHADOW_COLOR = (30, 30, 30)  # Dunkelgrau
TEXT_OUTLINE_COLOR = BLACK
TEXT_SHADOW_OFFSET = 2

# Feedback colors
FEEDBACK_CORRECT_COLOR = (0, 200, 0)  # Green
FEEDBACK_INCORRECT_COLOR = (200, 0, 0)  # Red

# Animation timings (in milliseconds)
FEEDBACK_DURATION = 2000
GAME_START_DURATION = 2000  # 2 Sekunden

# Game button dimensions
GAME_BUTTON_WIDTH = 140
GAME_BUTTON_HEIGHT = 40 