# font_manager.py
# Author: Max Weber, Philipp Gelfuss
# if you want to see more detailed information about the individual contributors of the code files, 
# please have a look at the "contributors.txt" file (in the "project" directory)

import pygame as pg
import json
from utils.path_utils import PathUtils
import os
import traceback


class FontManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FontManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, debug_mode=False):
        self._debug_mode = debug_mode

        if self._initialized:
            return

        self.path_utils = PathUtils()
        self.config = self._load_font_config()
        self.font_cache = {}
        self._initialized = True

    def _load_font_config(self):
        """Load font configuration from JSON file"""
        try:
            config_path = self.path_utils.get_resource_path("fonts", "font_config.json")
            with open(config_path, "r") as f:
                return json.load(f)
        except Exception as e:
            self._dprint("ERROR", f"Error loading font config: {e}")
            return None

    def get_font(self, font_type, size_type, height):
        """Get a font with the specified type and size"""
        if not self.config:
            self._dprint("WARNING", "No font config loaded!")
            return pg.font.Font(None, height // 20)

        cache_key = f"{font_type}_{size_type}_{height}"
        if cache_key in self.font_cache:
            return self.font_cache[cache_key]

        try:
            if font_type not in self.config["fonts"]:
                self._dprint("WARNING", f"Font type '{font_type}' not found in config!")
                return pg.font.Font(None, height // 20)

            font_config = self.config["fonts"][font_type]
            font_name = font_config["name"]

            if size_type not in font_config["sizes"]:
                self._dprint(
                    "WARNING",
                    f"Size type '{size_type}' not found for font '{font_type}'!",
                )
                return pg.font.Font(None, height // 20)

            size_value = font_config["sizes"][size_type]["value"]

            font_path = self.path_utils.get_resource_path("fonts", font_name)
            self._dprint("INFO", f"Loading font from: {font_path}")  # Debug output

            if not os.path.exists(font_path):
                self._dprint("WARNING", f"Font file not found: {font_path}")
                return pg.font.Font(None, height // 20)

            font = pg.font.Font(font_path, height // size_value)
            self.font_cache[cache_key] = font
            return font

        except Exception as e:
            self._dprint(
                "ERROR",
                f"Error loading font: {e}, font_type: {font_type}, size_type: {size_type}",
            )
            print(f"Stack trace: {traceback.format_exc()}")
            return pg.font.Font(None, height // 20)

    def get_game_word_font(self, height):
        """Get the font configuration for the game word"""
        try:
            if not self.config or "game_word" not in self.config:
                self._dprint("WARNING", "No game word font config found!")
                return {
                    "font": pg.font.Font(None, height // 20),
                    "has_outline": False,
                    "outline_color": (0, 0, 0),
                    "outline_width": 2,
                    "has_shadow": False,
                    "shadow_color": (0, 0, 0),
                    "shadow_offset": (2, 2),
                }

            word_config = self.config["game_word"]
            font_name = word_config.get("font_name")
            size_factor = word_config.get("size_factor", 20)

            # Load the font
            font_path = (
                self.path_utils.get_resource_path("fonts", font_name)
                if font_name
                else None
            )
            if font_path and os.path.exists(font_path):
                font = pg.font.Font(font_path, height // size_factor)
            else:
                font = pg.font.Font(None, height // size_factor)

            # Return complete configuration
            return {
                "font": font,
                "has_outline": word_config.get("has_outline", False),
                "outline_color": tuple(word_config.get("outline_color", (0, 0, 0))),
                "outline_width": word_config.get("outline_width", 2),
                "has_shadow": word_config.get("has_shadow", False),
                "shadow_color": tuple(word_config.get("shadow_color", (0, 0, 0))),
                "shadow_offset": tuple(word_config.get("shadow_offset", (2, 2))),
                "color": tuple(word_config.get("color", (255, 255, 255))),
            }

        except Exception as e:
            self._dprint("ERROR", f"Failed loading game word font: {e}")
            print(f"Stack trace: {traceback.format_exc()}")
            return {
                "font": pg.font.Font(None, height // 20),
                "has_outline": False,
                "outline_color": (0, 0, 0),
                "outline_width": 2,
                "has_shadow": False,
                "shadow_color": (0, 0, 0),
                "shadow_offset": (2, 2),
                "color": (255, 255, 255),
            }

    def get_title_font(self, height):
        """Get the title font (Anirb)"""
        try:
            return self.get_font("title_font", "title", height)
        except Exception as e:
            print("WARNING", f"Failed loading Anirb title font: {e}")
            return pg.font.SysFont("sans_serif", height // 8)

    def get_button_font(self, height):
        """Get the button font"""
        return self.get_font("main_font", "button", height)

    def get_game_button_font(self, height):
        """Get the game button font"""
        return self.get_font("main_font", "game_button", height)

    def get_text_font(self, height):
        """Get the normal text font"""
        return self.get_font("main_font", "text", height)

    def get_about_font(self, height):
        """Get the about text font"""
        return self.get_font("main_font", "about", height)

    def get_loading_font(self, height):
        """Get the loading screen font (Fondamento)"""
        try:
            return self.get_font("main_font", "loading", height)
        except Exception as e:
            self._dprint("WARNING", f"Failed loading loading font: {e}")
            return pg.font.SysFont("sans_serif", height // 12)

    def get_submenu_font(self, height):
        """Get the submenu font (Fondamento) at the specified size"""
        try:
            return self.get_font("submenu_font", "title", height)
        except Exception as e:
            self._dprint("WARNING", f"Failed loading submenu font: {e}")
            return pg.font.SysFont("sans_serif", height // 8)

    def _dprint(self, level, message):
        if self._debug_mode:
            print(f"[{level}] {message}")
