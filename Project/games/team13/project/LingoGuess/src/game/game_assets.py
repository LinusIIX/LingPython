# game_assets.py
# Author: Max Weber, Mojtaba Malek-Nejad
# if you want to see more detailed information about the individual contributors of the code files, 
# please have a look at the "contributors.txt" file (in the "project" directory)

import pygame as pg
import os

# Game asset management
class GameAssets:
    def __init__(self, debug_mode=False):
        self.assets = {}
        self.debug_mode = debug_mode
        self.debug_log("GameAssets manager initialized")
        self.load_assets()

    def debug_log(self, message):
        if self.debug_mode:
            print(f"[DEBUG][ASSETS] {message}")

    def load_assets(self):
        self.debug_log("Starting to load game assets")
        try:
            self.assets['background'] = self.load_image('photographics/background.png')
            self.debug_log("Background image loaded")
            self.assets['hero'] = self.load_image('assets/hero.png')
            self.debug_log("Hero image loaded")
            self.debug_log(f"Successfully loaded {len(self.assets)} assets")
        except Exception as e:
            self.debug_log(f"Error loading assets: {str(e)}")

    def load_image(self, path):
        full_path = os.path.join(os.path.dirname(__file__), '..', path)
        self.debug_log(f"Loading image from: {full_path}")
        try:
            image = pg.image.load(full_path).convert_alpha()
            self.debug_log(f"Successfully loaded image: {path}")
            return image
        except Exception as e:
            self.debug_log(f"Failed to load image {path}: {str(e)}")
            raise

    def get_asset(self, name):
        if name in self.assets:
            self.debug_log(f"Retrieved asset: {name}")
            return self.assets.get(name)
        self.debug_log(f"Asset not found: {name}")
        return None

    def unload_assets(self):
        self.assets.clear()
        self.debug_log("All assets unloaded")