# menu_ui.py
# Author: Max Weber
# if you want to see more detailed information about the individual contributors of the code files, 
# please have a look at the "contributors.txt" file (in the "project" directory)

import pygame as pg
import random as rand
import os
import math  # Add math import
from ui.constants import *
from ui.text_renderer import TextRenderer
from ui.button import Button
from ui.feedback import Feedback
from utils.path_utils import PathUtils
from ui.font_manager import FontManager  # Add this import

class MenuUI:
    _instance = None
    
    def __new__(cls, width=None, height=None):
        if cls._instance is None:
            cls._instance = super(MenuUI, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, width=None, height=None):
        if self._initialized:
            return
            
        self.width = width
        self.height = height
        self.STONE_COLORS = {
            'normal': (64, 64, 64),      # Dunkelgrau für normale Ansicht
            'hover': (80, 80, 80),       # Helleres Grau für Hover
            'selected': (45, 45, 45),    # Dunkleres Grau für Selected
            'border': (45, 45, 45),      # Dunkleres Grau für Kanten
            'shadow': (0, 0, 0)          # Schwarz für Schatten
        }
        
        # Initialize FontManager
        self.font_manager = FontManager()
        
        # Load slate texture
        path_utils = PathUtils()
        slate_path = path_utils.get_image_path('schieferV5.jpg')
        self.slate_texture = pg.image.load(slate_path)
        # Reduziere die Textur auf eine vernünftigere Größe für bessere Performance
        self.slate_texture = pg.transform.scale(self.slate_texture, (1024, 1024))
        
        # Initialize text renderer
        self.text_renderer = TextRenderer()
        
        # Cache initialisieren
        self.texture_cache = {}
        self.text_cache = {}
        self.button_cache = {}
        self.edge_masks = {}
        self.texture_region_cache = {}  # Cache für konstante Texturregionen
        self.shadow_cache = {}  # Cache für Schatten
        self.button_surface_cache = {}  # Cache für Button-Surfaces
        
        # Initialize feedback system
        self.feedback = None  # Will be initialized when surface is provided
        
        self._initialized = True

    def debug_log(self, message):
        """Simple debug logging"""
        print(f"[MenuUI] {message}")

    def get_button_font(self, size=None):
        """Get the button font with optional custom size"""
        if size is None:
            return self.font_manager.get_button_font(self.height)
        return self.font_manager.get_button_font(size * 20)  # Adjust size multiplier as needed

    def get_game_button_font(self, size=None):
        """Get the game button font with optional custom size"""
        if size is None:
            return self.font_manager.get_game_button_font(self.height)
        return self.font_manager.get_game_button_font(size * 20)

    def _create_cache_key(self, width, height, state):
        return f"{width}_{height}_{state}"

    def _create_text_cache_key(self, text, font_size, color):
        return f"{text}_{font_size}_{color}"

    def _create_region_cache_key(self, text, width, height):
        """Erstellt einen einzigartigen Key für jeden Button basierend auf Text und Größe"""
        return f"region_{text}_{width}_{height}"

    def _create_shadow_cache_key(self, width, height, is_hover):
        """Erstellt einen Cache-Key für Schatten"""
        return f"shadow_{width}_{height}_{is_hover}"

    def _create_button_surface_cache_key(self, text, width, height, state, is_about_button):
        """Erstellt einen Cache-Key für Button-Surfaces"""
        return f"button_{text}_{width}_{height}_{state}_{is_about_button}"

    def get_cached_texture(self, width, height, state, text):
        """Get or create a cached texture"""
        cache_key = f"{width}_{height}_{state}_{text}"
        if cache_key not in self.texture_cache:
            base_color = self.STONE_COLORS[state]
            region = self.get_cached_region(text, width, height)  # Hole die konstante Region
            self.texture_cache[cache_key] = self.apply_color_effect(region, base_color)  # Wende nur den Farbeffekt an
        return self.texture_cache[cache_key]

    def get_cached_text(self, text, font, color):
        cache_key = self._create_text_cache_key(text, font.get_height(), color)
        if cache_key not in self.text_cache:
            self.text_cache[cache_key] = font.render(text, True, color)
        return self.text_cache[cache_key]

    def get_cached_region(self, text, width, height):
        """Holt eine gecachte Texturregion oder erstellt eine neue"""
        cache_key = self._create_region_cache_key(text, width, height)
        
        if cache_key not in self.texture_region_cache:
            # Berechne die Größe des Texturausschnitts
            tex_width, tex_height = self.slate_texture.get_rect().size
            min_size_factor = 0.05
            scale_factor = max(0.05, min_size_factor * max(tex_width/width, tex_height/height))
            
            # Stelle sicher, dass die skalierte Größe nicht größer als die Textur ist
            scaled_width = min(tex_width, int(width * scale_factor))
            scaled_height = min(tex_height, int(height * scale_factor))
            
            # Berechne mögliche Offset-Bereiche
            max_x_offset = max(0, tex_width - scaled_width)
            max_y_offset = max(0, tex_height - scaled_height)
            
            # Wähle einen zufälligen Ausschnitt
            x_offset = rand.randint(0, max_x_offset) if max_x_offset > 0 else 0
            y_offset = rand.randint(0, max_y_offset) if max_y_offset > 0 else 0
            
            # Kopiere den Ausschnitt
            region = pg.Surface((scaled_width, scaled_height))
            region.blit(self.slate_texture, (0, 0), (x_offset, y_offset, scaled_width, scaled_height))
            
            # Skaliere mit Padding
            padding = 4
            padded_width = width + padding * 2
            padded_height = height + padding * 2
            region = pg.transform.scale(region, (padded_width, padded_height))
            
            # Schneide den mittleren Teil aus
            final_region = pg.Surface((width, height))
            final_region.blit(region, (-padding, -padding))
            
            # Speichere im Cache
            self.texture_region_cache[cache_key] = final_region
            
        return self.texture_region_cache[cache_key]

    def get_cached_region_about(self, text, width, height):
        """Spezielle hochqualitative Texturregion für About-Us-Buttons"""
        cache_key = f"about_{self._create_region_cache_key(text, width, height)}"
        
        if cache_key not in self.texture_region_cache:
            # Berechne die Größe des Texturausschnitts
            tex_width, tex_height = self.slate_texture.get_rect().size
            
            # Verwende einen größeren Skalierungsfaktor für About-Buttons
            min_size_factor = 0.8
            
            # Berechne den Skalierungsfaktor basierend auf der Buttongröße
            scale_factor = max(min_size_factor, min_size_factor * max(width/tex_width, height/tex_height))
            
            # Stelle sicher, dass die skalierte Größe nicht größer als die Textur ist
            scaled_width = min(tex_width, int(width * scale_factor))
            scaled_height = min(tex_height, int(height * scale_factor))
            
            # Berechne mögliche Offset-Bereiche
            max_x_offset = max(0, tex_width - scaled_width)
            max_y_offset = max(0, tex_height - scaled_height)
            
            # Wähle einen zufälligen Ausschnitt
            x_offset = rand.randint(0, max_x_offset) if max_x_offset > 0 else 0
            y_offset = rand.randint(0, max_y_offset) if max_y_offset > 0 else 0
            
            # Kopiere den Ausschnitt
            region = pg.Surface((scaled_width, scaled_height))
            region.blit(self.slate_texture, (0, 0), (x_offset, y_offset, scaled_width, scaled_height))
            
            # Skaliere mit Padding für bessere Qualität
            padding = 8
            padded_width = width + padding * 2
            padded_height = height + padding * 2
            
            # Verwende SMOOTHSCALE für bessere Qualität bei der Skalierung
            region = pg.transform.smoothscale(region, (padded_width, padded_height))
            
            # Schneide den mittleren Teil aus
            final_region = pg.Surface((width, height))
            final_region.blit(region, (-padding, -padding))
            
            # Speichere im Cache
            self.texture_region_cache[cache_key] = final_region
            
        return self.texture_region_cache[cache_key]

    def draw_text_with_shadow(self, surface, text, font, color, x, y):
        """Draw text with shadow effect"""
        TextRenderer.render_text_with_shadow(text, font, color, surface, x, y)

    def draw_text_with_outline(self, surface, text, font, color, x, y, outline_width=2):
        """Draw text with outline effect"""
        TextRenderer.render_text_with_outline(text, font, color, surface, x, y, outline_width)

    def create_irregular_mask(self, width, height):
        """Erstellt eine realistischere, leicht unregelmäßige Maske für Schieferplatten"""
        cache_key = f"{width}_{height}"
        if cache_key not in self.edge_masks:
            mask = pg.Surface((width, height), pg.SRCALPHA)
            mask.fill((0, 0, 0, 0))  # Start transparent
            
            # Verwende den definierten BUTTON_CORNER_RADIUS
            corner_radius = BUTTON_CORNER_RADIUS
            
            # Zeichne das Hauptrechteck mit Rundungen
            rect = pg.Rect(0, 0, width, height)
            pg.draw.rect(mask, (255, 255, 255, 255), rect, border_radius=corner_radius)
            
            # Zeichne einen inneren Bereich mit leicht kleinerem Radius für weichere Kanten
            inner_rect = pg.Rect(1, 1, width-2, height-2)
            pg.draw.rect(mask, (255, 255, 255, 255), inner_rect, border_radius=corner_radius-1)
            
            # Füge subtile Unregelmäßigkeiten nur im inneren Bereich hinzu
            padding = corner_radius + 4  # Größerer Abstand vom Rand
            for i in range(3):  # Noch weniger Unregelmäßigkeiten
                x1 = rand.randint(padding, width - padding)
                y1 = rand.randint(padding, height - padding)
                x2 = x1 + rand.randint(-3, 3)  # Noch kleinere Variationen
                y2 = y1 + rand.randint(-3, 3)
                
                # Zeichne sehr dünne Linien für minimale Variationen
                pg.draw.line(mask, (255, 255, 255, 255), (x1, y1), (x2, y2), 1)
            
            self.edge_masks[cache_key] = mask
        return self.edge_masks[cache_key]

    def create_stone_texture(self, width, height, base_color, text):
        # 1. Erstelle die Basis-Surface mit Alpha-Kanal
        texture = pg.Surface((width, height), pg.SRCALPHA)
        texture.fill((0, 0, 0, 0))  # Komplett transparent
        
        # 2. Zeichne das gerundete Rechteck als Maske
        pg.draw.rect(texture, (255, 255, 255, 255), texture.get_rect(), border_radius=BUTTON_CORNER_RADIUS)
        
        # 3. Hole die Textur-Region
        region = self.get_cached_region(text, width, height)
        
        # 4. Wende die Textur innerhalb der Rundungen an
        for x in range(width):
            for y in range(height):
                if texture.get_at((x, y))[3] > 0:  # Wenn der Pixel sichtbar ist
                    color = region.get_at((x, y))
                    # Mische mit der Basis-Farbe
                    r = min(255, int((color[0] + base_color[0]) / 2))
                    g = min(255, int((color[1] + base_color[1]) / 2))
                    b = min(255, int((color[2] + base_color[2]) / 2))
                    texture.set_at((x, y), (r, g, b, 255))
        
        return texture

    def init_feedback(self, surface):
        if self.feedback is None:
            self.feedback = Feedback(surface, self.width, self.height)

    def create_button(self, surface, text, font, x, y, width=None, height=None, is_selected=False):
        """Factory method for creating buttons with consistent styling"""
        button = Button(surface, text, font, x, y, width, height)
        button.is_selected = is_selected
        return button

    def get_cached_button(self, surface, text, font, x, y, width=None, height=None, is_selected=False):
        """Get or create a cached button instance"""
        cache_key = f"{text}_{x}_{y}_{width}_{height}_{is_selected}"
        
        if cache_key not in self.button_cache:
            self.button_cache[cache_key] = self.create_button(
                surface, text, font, x, y, width, height, is_selected
            )
        
        button = self.button_cache[cache_key]
        button.update(pg.mouse.get_pos())
        return button

    def _get_cached_shadow(self, width, height, is_hover):
        """Holt oder erstellt gecachte Schatten"""
        cache_key = self._create_shadow_cache_key(width, height, is_hover)
        
        if cache_key not in self.shadow_cache:
            if is_hover:
                # Create layered hover shadows
                shadows = []
                shadow_offset = 8
                for i in range(shadow_offset):
                    shadow = pg.Surface((width + i*2, height + i*2), pg.SRCALPHA)
                    alpha = int(35 * (1 - i/shadow_offset))
                    shadow.fill((0, 0, 0, alpha))
                    shadows.append(shadow)
                self.shadow_cache[cache_key] = shadows
            else:
                # Create normal shadow
                normal_shadow = pg.Surface((width + 4, height + 4), pg.SRCALPHA)
                normal_shadow.fill((0, 0, 0, 40))
                self.shadow_cache[cache_key] = normal_shadow
            
        return self.shadow_cache[cache_key]

    def _get_cached_button_surface(self, text, width, height, state, is_about_button):
        """Holt oder erstellt gecachte Button-Surface"""
        cache_key = self._create_button_surface_cache_key(text, width, height, state, is_about_button)
        
        if cache_key not in self.button_surface_cache:
            # Create the button surface
            button_surface = pg.Surface((width, height), pg.SRCALPHA)
            button_surface.fill((0, 0, 0, 0))  # Transparent
            
            # Draw rounded rectangle mask
            pg.draw.rect(button_surface, (255, 255, 255, 255), button_surface.get_rect(), border_radius=BUTTON_CORNER_RADIUS)
            
            # Get the appropriate region
            if is_about_button:
                region = self.get_cached_region_about(text, width, height)
            else:
                region = self.get_cached_region(text, width, height)
            
            # Apply texture and effects
            for x_pos in range(width):
                for y_pos in range(height):
                    if button_surface.get_at((x_pos, y_pos))[3] > 0:
                        color = region.get_at((x_pos, y_pos))
                        if state == 'hover':
                            # 10% brighter
                            r = min(255, int(color[0] * 1.15))
                            g = min(255, int(color[1] * 1.15))
                            b = min(255, int(color[2] * 1.15))
                            button_surface.set_at((x_pos, y_pos), (r, g, b, 255))
                        elif state == 'selected':
                            # 20% darker
                            r = int(color[0] * 0.65)
                            g = int(color[1] * 0.65)
                            b = int(color[2] * 0.65)
                            button_surface.set_at((x_pos, y_pos), (r, g, b, 255))
                        else:
                            # Normal state
                            button_surface.set_at((x_pos, y_pos), (color[0], color[1], color[2], 255))
            
            self.button_surface_cache[cache_key] = button_surface
        
        return self.button_surface_cache[cache_key]

    def draw_stone_button(self, surface, text, font, x, y, width, height, is_selected=False, is_hovered=False, is_about_button=False):
        """Draw a stone-textured button with optional hover and selected states"""
        hover_offset = 0
        
        # Get cached shadows
        shadows = self._get_cached_shadow(width, height, is_hovered)
        
        # Draw shadows based on state
        if is_hovered:
            hover_offset = 1  # Button moves up when hovered
            # Draw layered hover shadows
            for i, shadow in enumerate(shadows):
                shadow_x = x - i
                shadow_y = y + i + 2 - hover_offset
                surface.blit(shadow, (shadow_x, shadow_y))
        else:
            # Draw normal shadow
            surface.blit(shadows, (x - 2, y + 3))
        
        # Get button state
        state = 'selected' if is_selected else 'hover' if is_hovered else 'normal'
        
        # Get cached button surface with the actual text
        button_surface = self._get_cached_button_surface(text, width, height, state, is_about_button)
        
        # Draw the button with hover offset
        surface.blit(button_surface, (x, y - hover_offset))
        
        # Draw text if provided
        if text:
            # Render text with shadow for better visibility
            shadow_color = (30, 30, 30)  # Dark gray for shadow
            text_color = (255, 255, 255)  # White for main text
            
            # Cache shadow text
            shadow_cache_key = f"text_shadow_{text}_{font.get_height()}"
            if shadow_cache_key not in self.text_cache:
                self.text_cache[shadow_cache_key] = font.render(text, True, shadow_color)
            shadow_surface = self.text_cache[shadow_cache_key]
            
            # Cache main text
            text_cache_key = f"text_{text}_{font.get_height()}"
            if text_cache_key not in self.text_cache:
                self.text_cache[text_cache_key] = font.render(text, True, text_color)
            text_surface = self.text_cache[text_cache_key]
            
            # Calculate text position
            text_rect = text_surface.get_rect(center=(x + width//2, y + height//2 - hover_offset))
            shadow_rect = text_rect.copy()
            shadow_rect.x += 2  # Offset shadow slightly
            shadow_rect.y += 2
            
            # Draw shadow first, then main text
            surface.blit(shadow_surface, shadow_rect)
            surface.blit(text_surface, text_rect)
        
        return pg.Rect(x, y - hover_offset, width, height)

    def get_max_button_width(self, texts, font):
        """Calculate maximum width needed for a group of buttons"""
        max_width = 0
        for text in texts:
            text_width, _ = TextRenderer.get_text_dimensions(text, font)
            width = text_width + BUTTON_PADDING * 2
            max_width = max(max_width, width)
        return max_width

    def apply_color_effect(self, texture, base_color):
        """Wendet nur den Farbeffekt auf eine existierende Textur an"""
        result = pg.Surface(texture.get_size(), pg.SRCALPHA)
        
        # Berechne den Dunkelheitsfaktor für den ausgewählten Zustand
        darkening = 0.65 if base_color == self.STONE_COLORS['selected'] else 1.15  # Heller für normale Buttons
        
        for x in range(texture.get_width()):
            for y in range(texture.get_height()):
                color = texture.get_at((x, y))
                if color.a > 0:  # Nur sichtbare Pixel bearbeiten
                    # Berechne die finale Farbe basierend auf der Textur und dem Basis-Farbton
                    r = min(255, int(color[0] * darkening))
                    g = min(255, int(color[1] * darkening))
                    b = min(255, int(color[2] * darkening))
                    result.set_at((x, y), (r, g, b, color.a))
                else:
                    result.set_at((x, y), color)
        
        return result 