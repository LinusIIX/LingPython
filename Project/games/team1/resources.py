# contributors:
# Nikolas (most of the file, asset loading, crteated as a result of refactoring)
# Max (highscore functions)

import json
import os
import sys
from typing import LiteralString
import tkinter
import tkinter.filedialog

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame as pg
import requests

import settings

# convention: objects and groupings in CAPS, assets in snake_case
ASSETS = {
    "SOUNDS": {
        "KEYBOARD": {}
    },
    "IMAGES": {},
    "FONTS": {},
    "WORDLISTS": {},
    "HIGHSCORES": {}
}


def load_assets():
    # load fonts
    load_sysfont(name="monospace", size=(settings.SCREEN_HEIGHT // 30), bold=True)
    load_sysfont(name="monospace", size=(settings.SCREEN_HEIGHT // 30), bold=True, underline=True)

    # load wordlists
    load_wordlist("MIT-10000")

    # load images
    load_image(name="background",
               filename=(os.path.join("img", "background.png")),
               scale=settings.SCREEN_HEIGHT)
    load_image(name="ballista",
               filename=(os.path.join("img", "ballista.png")),
               scale=settings.PLAYER_SIZE * 2)
    load_image(name="heart",
               filename=(os.path.join("img", "heart.png")),
               scale=settings.PLAYER_SIZE)
    load_image(name="empty_heart",
               filename=(os.path.join("img", "empty_heart.png")),
               scale=settings.PLAYER_SIZE)
    load_image(name="healing_heart",
               filename=(os.path.join("img", "healing_heart.png")),
               scale=settings.PLAYER_SIZE)
    load_image(name="bolt",
               filename=(os.path.join("img", "bolt.png")),
               scale=0.1*settings.PLAYER_SIZE)

    # load sounds
    load_sound(name="kill", filename=(os.path.join("sounds", "enter.mp3")))
    load_sound(name="kill", filename=(os.path.join("sounds", "caps.mp3")))

    with (open(resource_path(os.path.join("resources", "sounds", "keyboard", "config.json")), "r") as sound_config_file_handle):
        sound_config = json.load(sound_config_file_handle)
        for sound_key in sound_config:
            load_sound(name=sound_key,
                       filename=os.path.join("sounds", "keyboard", f"{str(sound_config[sound_key][0])}.ogg"),
                       keyboard=True)
            
    load_highscores()


def load_sysfont(name: str, size: int, bold=False, italic=False, underline=False):
    font = pg.font.SysFont(name, size, bold=bold, italic=italic)
    font.set_underline(underline)
    ASSETS["FONTS"][f"{name}{'UL' if underline else ''}"] = font
    return ASSETS["FONTS"][name]

def load_image(name: str, filename: str | LiteralString, scale: float = None):
    image = pg.image.load(resource_path(os.path.join("resources", filename)))
    if scale:
        orig_width = image.width
        orig_height = image.height
        scale_factor = scale / min(orig_width, orig_height)
        new_width = int(orig_width * scale_factor)
        new_height = int(orig_height * scale_factor)
        image = pg.transform.smoothscale(image, (new_width, new_height))
    ASSETS["IMAGES"][name] = image
    return ASSETS["IMAGES"][name]


def load_sound(name: str, filename: str | LiteralString, keyboard=False):
    sound = pg.mixer.Sound(resource_path((os.path.join("resources", filename))))

    if keyboard:
        ASSETS["SOUNDS"]["KEYBOARD"][name] = sound
        sound.set_volume(0.5)
    else:
        ASSETS["SOUNDS"][name] = sound

    return sound

def load_wordlist(name: str = ""):
    if name:
        url = "https://www.mit.edu/~ecprice/wordlist.10000"
        content = requests.get(url).content.decode("utf-8").lower().splitlines()
    else:
        top = tkinter.Tk()
        top.withdraw()
        file_path = tkinter.filedialog.askopenfilename(parent=top, filetypes=[("Text files", "*.txt")], title="Select text file with word list")
        top.destroy()
        with open(file_path, "r") as file:
            content = list(filter(lambda x: all(char in "abcdefghijklmnopqrstuvwxyz " for char in x.lower()), file.read().splitlines()))
        name = file_path.rsplit("/",1)[-1]
    ASSETS["WORDLISTS"][name] = content
    return name

def resource_path(relative_path):
    """ This gets the path to the resources, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):  # pyinstaller apparently sets this var
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__) # oh blessed be this function for it granteth me the true path, no matter whence the script is summoned
    return os.path.join(base_path, relative_path)

def load_highscores():
    with open(resource_path("highscores.json")) as file:
        ASSETS["HIGHSCORES"] = json.load(file)

def save_highscore(leaderboard, score):
    if "You" in ASSETS["HIGHSCORES"][leaderboard]:
        if ASSETS["HIGHSCORES"][leaderboard]["You"] >= score:
            return
    ASSETS["HIGHSCORES"][leaderboard]["You"] = score
    with open(resource_path("highscores.json"), "w") as file:
        json.dump(ASSETS["HIGHSCORES"], file, indent=4)