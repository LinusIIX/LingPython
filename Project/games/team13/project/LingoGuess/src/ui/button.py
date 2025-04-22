# button.py
# Author: Max Weber
# if you want to see more detailed information about the individual contributors of the code files, 
# please have a look at the "contributors.txt" file (in the "project" directory)

import pygame as pg
from .constants import *
from .text_renderer import TextRenderer

class Button:
    def __init__(self, surface, text, font, x, y, width=None, height=None):
        self.surface = surface
        self.text = text
        self.font = font
        self.x = x
        self.y = y
        
        # Calculate dimensions if not provided
        if width is None or height is None:
            text_width, text_height = TextRenderer.get_text_dimensions(text, font)
            self.width = width or text_width + BUTTON_PADDING * 2
            self.height = height or text_height + BUTTON_PADDING
        else:
            self.width = width
            self.height = height
        
        self.rect = pg.Rect(x, y, self.width, self.height)
        self.is_hovered = False
        self.is_selected = False
        
        # Get MenuUI instance (Singleton)
        from menu.menu_ui import MenuUI
        self.menu_ui = MenuUI()
        
        # Pre-render all surfaces
        self._initialize_cached_surfaces()
        
    def _initialize_cached_surfaces(self):
        # Cache für Button-Zustände
        self._cached_surfaces = self._create_cached_surfaces()
        
        # Cache für Text
        self._cached_text = self._create_cached_text()
        
        # Cache für Schatten
        self._cached_shadows = self._create_cached_shadows()
    
    def _create_cached_text(self):
        # Erstelle Text-Surface mit Schatten
        text_surface = self.font.render(self.text, True, TEXT_COLOR)
        text_shadow = self.font.render(self.text, True, TEXT_SHADOW_COLOR)
        
        # Berechne die Position für die Zentrierung
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        shadow_rect = text_shadow.get_rect(center=(self.width // 2 + TEXT_SHADOW_OFFSET, 
                                                 self.height // 2 + TEXT_SHADOW_OFFSET))
        
        # Erstelle eine kombinierte Surface
        combined = pg.Surface((self.width, self.height), pg.SRCALPHA)
        combined.blit(text_shadow, shadow_rect)
        combined.blit(text_surface, text_rect)
        
        return combined
    
    def _create_cached_shadows(self):
        shadows = {
            'normal': None,
            'hover': []
        }
        
        # Normaler Schatten
        normal_shadow = pg.Surface((self.width + 4, self.height + 4), pg.SRCALPHA)
        normal_shadow.fill((0, 0, 0, 40))
        shadows['normal'] = normal_shadow
        
        # Hover-Schatten (8 Ebenen)
        shadow_offset = 8
        for i in range(shadow_offset):
            shadow = pg.Surface((self.width + i*2, self.height + i*2), pg.SRCALPHA)
            alpha = int(35 * (1 - i/shadow_offset))
            shadow.fill((0, 0, 0, alpha))
            shadows['hover'].append(shadow)
        
        return shadows

    def _create_cached_surfaces(self):
        cached = {}
        states = ['normal', 'hover', 'selected']
        
        for state in states:
            # Create button surface with alpha channel
            button_surface = pg.Surface((self.width, self.height), pg.SRCALPHA)
            button_surface.fill((0, 0, 0, 0))  # Transparent
            
            # Draw rounded rectangle mask
            pg.draw.rect(button_surface, (255, 255, 255, 255), button_surface.get_rect(), border_radius=BUTTON_CORNER_RADIUS)
            
            # Get texture region
            region = self.menu_ui.get_cached_region(self.text, self.width, self.height)
            
            # Apply texture within rounded corners
            base_color = self.menu_ui.STONE_COLORS[state]
            for x in range(self.width):
                for y in range(self.height):
                    if button_surface.get_at((x, y))[3] > 0:
                        color = region.get_at((x, y))
                        if state == 'hover':
                            # Slightly lighter on hover (10% brighter)
                            r = min(255, int(color[0] * 1.15))
                            g = min(255, int(color[1] * 1.15))
                            b = min(255, int(color[2] * 1.15))
                            button_surface.set_at((x, y), (r, g, b, 255))
                        elif state == 'selected':
                            # Slightly darker when selected (20% darker)
                            r = int(color[0] * 0.65)
                            g = int(color[1] * 0.65)
                            b = int(color[2] * 0.65)
                            button_surface.set_at((x, y), (r, g, b, 255))
                        else:
                            # Normal state - use original texture color
                            button_surface.set_at((x, y), (color[0], color[1], color[2], 255))
            
            cached[state] = button_surface
        
        return cached

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered

    def get_state(self):
        if self.is_selected:
            return 'selected'
        elif self.is_hovered:
            return 'hover'
        return 'normal'

    def draw(self):
        # Get current state
        state = self.get_state()
        hover_offset = 0
        
        # Draw shadows based on state
        if self.is_hovered:
            hover_offset = 1  # Offset für Hover-Effekt
            for i, shadow in enumerate(self._cached_shadows['hover']):
                shadow_x = self.x - i
                shadow_y = self.y + i + 2 - hover_offset
                self.surface.blit(shadow, (shadow_x, shadow_y))
        else:
            self.surface.blit(self._cached_shadows['normal'], 
                            (self.x - 2, self.y + 3))
        
        # Draw the cached button surface
        self.surface.blit(self._cached_surfaces[state], 
                         (self.x, self.y - hover_offset))
        
        # Draw the cached text
        self.surface.blit(self._cached_text, 
                         (self.x, self.y - hover_offset))

    def handle_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos) 