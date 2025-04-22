# feedback.py
# Author: Max Weber
# if you want to see more detailed information about the individual contributors of the code files, 
# please have a look at the "contributors.txt" file (in the "project" directory)

import pygame as pg
from .constants import *
from .text_renderer import TextRenderer

class Feedback:
    def __init__(self, surface, width, height):
        self.surface = surface
        self.width = width
        self.height = height
        self.font = TextRenderer.create_font(height, BUTTON_FONT_SIZE_FACTOR)
        self.show_feedback = False
        self.message = ""
        self.is_correct = False
        self.feedback_time = None

    def show(self, message, is_correct):
        self.message = message
        self.is_correct = is_correct
        self.show_feedback = True
        self.feedback_time = pg.time.get_ticks()

    def update(self):
        if self.show_feedback:
            if pg.time.get_ticks() - self.feedback_time > FEEDBACK_DURATION:
                self.show_feedback = False
                return False
            return True
        return False

    def draw(self):
        if not self.show_feedback:
            return

        # Create semi-transparent background
        feedback_surface = pg.Surface((self.width, 100))
        feedback_surface.set_alpha(180)
        
        # Set color based on feedback type
        if not self.is_correct and self.message == "Game Over!":
            feedback_surface.fill(FEEDBACK_INCORRECT_COLOR)
        elif self.is_correct:
            feedback_surface.fill(FEEDBACK_CORRECT_COLOR)
        else:
            feedback_surface.fill(FEEDBACK_INCORRECT_COLOR)

        # Draw the background
        self.surface.blit(feedback_surface, (0, self.height // 4))

        # Draw the message
        TextRenderer.render_text(
            self.message,
            self.font,
            TEXT_COLOR,
            self.surface,
            self.width // 2,
            self.height // 4 + 50
        ) 