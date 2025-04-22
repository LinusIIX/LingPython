# contributors:
# Nikolas (created as a result of refactoring)

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60

PLAYER_SIZE = SCREEN_WIDTH//30

SHOT_FLIGHT_RATE = 0.5
BASE_SUMMONING_CHANCE = 200 # 1 per BASE_SUMMONING_CHANCE per tick

COLORS_CHOICES = {
    # Hier kann man eigene colours hinzügen
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "DARK_GRAY": (50,50,50),
    "LIGHT_GRAY": (100,100,100),
}

ENEMY_COLOR_CHOICES = {
    "DARK_RED": (130, 0, 0),
    "DARK_MAGENTA": (130, 0, 130),
    "DARK_BLUE": (0, 0, 130),
    "LIGHT_RED": (255, 50, 50),
    "LIGHT_MAGENTA": (230, 0, 230),
    "LIGHT_BLUE": (100, 100, 255)
}

ENEMY_COLORS = list(ENEMY_COLOR_CHOICES.values())

CHANGABLE_VARIABLES = {
  "SOUND": 50,
  "DIFFICULTY": 0,
  "stats": True,
  "word_length_min": 4,
  "word_length_max": 6,
  "active_wordlist": "MIT-10000",
}