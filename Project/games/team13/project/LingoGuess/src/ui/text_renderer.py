# text_renderer.py
# Author: Max Weber
# if you want to see more detailed information about the individual contributors of the code files, 
# please have a look at the "contributors.txt" file (in the "project" directory)

import pygame as pg
from .constants import *

class TextRenderer:
    @staticmethod
    def create_font(height, size_factor):
        return pg.font.SysFont('sans_serif', height // size_factor)

    @staticmethod
    def render_text(text, font, color, surface, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        surface.blit(text_surface, text_rect)

    @staticmethod
    def render_text_with_shadow(text, font, color, surface, x, y, shadow_offset=2):
        # Draw shadow
        shadow_surface = font.render(text, True, TEXT_SHADOW_COLOR)
        shadow_rect = shadow_surface.get_rect(center=(x + shadow_offset, y + shadow_offset))
        surface.blit(shadow_surface, shadow_rect)
        
        # Draw main text
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        surface.blit(text_surface, text_rect)

    @staticmethod
    def render_text_with_outline(text, font, color, surface, x, y, outline_width=2):
        # Create surfaces for the outline
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        
        # Draw outline by offsetting text in all directions
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:  # Skip the center position
                    outline_rect = text_rect.copy()
                    outline_rect.x += dx
                    outline_rect.y += dy
                    outline_surface = font.render(text, True, TEXT_OUTLINE_COLOR)
                    surface.blit(outline_surface, outline_rect)
        
        # Draw main text
        surface.blit(text_surface, text_rect)

    @staticmethod
    def render_game_word(text, font_config, surface, x, y):
        """Render game word with configured style (outline, shadow, etc.)"""
        font = font_config['font']
        color = font_config['color']
        
        # Create main text surface
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        
        # Draw outline if configured
        if font_config['has_outline']:
            outline_width = font_config['outline_width']
            outline_color = font_config['outline_color']
            
            for dx in range(-outline_width, outline_width + 1):
                for dy in range(-outline_width, outline_width + 1):
                    if dx != 0 or dy != 0:
                        outline_rect = text_rect.copy()
                        outline_rect.x += dx
                        outline_rect.y += dy
                        outline_surface = font.render(text, True, outline_color)
                        surface.blit(outline_surface, outline_rect)
        
        # Draw shadow if configured
        if font_config['has_shadow']:
            shadow_color = font_config['shadow_color']
            shadow_offset = font_config['shadow_offset']
            
            shadow_surface = font.render(text, True, shadow_color)
            shadow_rect = text_rect.copy()
            shadow_rect.x += shadow_offset[0]
            shadow_rect.y += shadow_offset[1]
            surface.blit(shadow_surface, shadow_rect)
        
        # Draw main text
        surface.blit(text_surface, text_rect)

    @staticmethod
    def get_text_dimensions(text, font):
        text_surface = font.render(text, True, BLACK)
        return text_surface.get_rect().width, text_surface.get_rect().height