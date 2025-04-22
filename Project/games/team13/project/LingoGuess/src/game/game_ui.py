# game_ui.py
# Author: Mojtaba Malek-Nejad, Max Weber, Philipp Gelfuss
# if you want to see more detailed information about the individual contributors of the code files, 
# please have a look at the "contributors.txt" file (in the "project" directory)

from typing import List
import pygame as pg
from ui.constants import *
from ui.text_renderer import TextRenderer
from ui.font_manager import FontManager
from utils.path_utils import PathUtils


class GameUI:
    def __init__(self, width, height, game_instance=None, debug_mode=False):
        self.game_instance = game_instance  # Store the game instance reference
        self.width = width
        self.height = height
        self.debug_mode = debug_mode
        self.window = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("LingoGuess\nA Hero's Quest")
        self.font = pg.font.SysFont('sans_serif', 36)
        self.feedback_font = pg.font.SysFont('sans_serif', 48)  # Larger font for feedback
        self.clock = pg.time.Clock()
        self.fps = 60
        # Colors for feedback
        self.CORRECT_COLOR = (0, 200, 0)  # Green
        self.INCORRECT_COLOR = (200, 0, 0)  # Red
        self.debug_log("GameUI initialized with resolution: {}x{}".format(width, height))

    def debug_log(self, message):
        if self.debug_mode:
            print(f"[DEBUG][UI] {message}")

    def draw_text(self, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.window.blit(text_surface, text_rect)
        self.debug_log(f"Text drawn: '{text}' at position ({x}, {y})")

    def draw_button(self, color, rect, text, text_color):
        pg.draw.rect(self.window, color, rect)
        text_surface = self.font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(rect.x + rect.width // 2, rect.y + rect.height // 2))
        self.window.blit(text_surface, text_rect)
        self.debug_log(f"Button drawn: '{text}'")

    def update_display(self):
        pg.display.update()
        self.clock.tick(self.fps)
        self.debug_log("Display updated")

    def clear_window(self, color):
        self.window.fill(color)
        self.debug_log("Window cleared")

    def show_game_over(self):
        self.clear_window((255, 255, 255))
        self.draw_text("Game Over", (255, 0, 0), self.width // 2, self.height // 2)
        self.update_display()
        self.debug_log("Game Over screen displayed")
        pg.time.wait(2000)

    def show_victory(self):
        self.clear_window((255, 255, 255))
        self.draw_text("You Decoded the Inscription!", (0, 255, 0), self.width // 2, self.height // 2)
        self.update_display()
        self.debug_log("Victory screen displayed")
        pg.time.wait(2000)


    # f"Correct Answers: {self.correct_answers}",
    # f"Incorrect Answers: {self.incorrect_answers}",
    # f"Accuracy: {accuracy:.2f}%",
    # f"Words Per Minute (WPM): {wpm:.2f}"
    def show_stats_popup(self, correct_answers, incorrect_answers, start_time):
        """Show a full page stats view with game results and navigation buttons."""
        # Load background image (using same reference as game)
        path_utils = PathUtils()
        background = pg.transform.scale(
            pg.image.load(path_utils.get_image_path('stats_background_wood.png')), 
            (self.width, self.height)
        )
        
        # Draw background
        self.window.blit(background, (0, 0))

        # Initialize FontManager for consistent styling
        font_manager = FontManager()
        
        # Get game word configuration for consistent styling
        word_config = font_manager.get_game_word_font(self.height)
        stats_color = word_config['color']  # Use the same color as the game word
        
        # Draw Game Over text using stats header font
        game_over_font = font_manager.get_font('main_font', 'stats_header', self.height)
        TextRenderer.render_text_with_outline(
            "Game Over",
            game_over_font,
            (255, 0, 0),  # Red color for Game Over
            self.window,
            self.width // 2,
            180,  # Position above stats
            word_config['outline_width']
        )
        
        # Stats text
        stats_font = font_manager.get_button_font(self.height)
        if correct_answers + incorrect_answers > 0:
            accuracy = f"Accuracy: {correct_answers / (correct_answers + incorrect_answers) * 100:.2f}%"
        else:
            accuracy = "Accuracy: N/A"
            
        # Calculate elapsed time in minutes
        elapsed_time_minutes = (pg.time.get_ticks() - start_time) / 60000  # Convert milliseconds to minutes
        if elapsed_time_minutes > 0:
            wpm = correct_answers / elapsed_time_minutes
        else:
            wpm = 0
        
        stats_texts = [
            f"Correct Answers: {correct_answers}",
            f"Incorrect Answers: {incorrect_answers}",
            accuracy,
            f"WPM: {int(wpm)}"
        ]

        # Draw stats text (moved down)
        for i, text in enumerate(stats_texts):
            # Create text with outline and shadow like the game word
            if word_config['has_outline']:
                TextRenderer.render_text_with_outline(
                    text,
                    stats_font,
                    stats_color,
                    self.window,
                    self.width // 2,
                    250 + i * 50,
                    word_config['outline_width']
                )
            else:
                stat_surface = stats_font.render(text, True, stats_color)
                stat_rect = stat_surface.get_rect(center=(self.width // 2, 250 + i * 50))
                self.window.blit(stat_surface, stat_rect)

        # Create navigation buttons with same style as other buttons
        button_font = font_manager.get_button_font(self.height)
        
        # Use constants from ui.constants for consistent button dimensions and spacing
        button_height = button_font.get_height() + BUTTON_PADDING  # Match the height calculation from Button class
        button_spacing = BUTTON_SPACING  # Use constant from ui.constants

        # Button texts
        button_texts = ["Play Again", "Return to Menu", "Quit Game"]
        
        # Calculate button width to match main menu buttons
        main_menu_texts = ["Start Game (Enter)", "Change Mode", "Change Difficulty", "About Us", "Quit Game"]
        button_width = 0
        padding = BUTTON_PADDING  # Use constant from ui.constants
        for text in main_menu_texts:  # Use main menu texts to calculate width
            text_surface = button_font.render(text, True, (255, 255, 255))
            width = text_surface.get_rect().width + padding * 2
            button_width = max(button_width, width)

        # Position buttons at the same positions as the last three buttons in main menu
        button_x = DEFAULT_BUTTON_X  # Use constant from ui.constants
        bottom_button_y = 480  # Position of bottom button
        second_button_y = bottom_button_y - button_spacing  # Second from bottom
        top_button_y = second_button_y - button_spacing  # Third from bottom
        button_positions = [top_button_y, second_button_y, bottom_button_y]
        
        # Draw buttons using the same stone button style
        from menu.menu_ui import MenuUI
        menu_ui = MenuUI(self.width, self.height)
        
        buttons = []
        mouse_pos = pg.mouse.get_pos()
        
        for i, text in enumerate(button_texts):
            y_pos = button_positions[i]  # Use pre-calculated positions
            button_rect = pg.Rect(button_x, y_pos, button_width, button_height)
            is_hovered = button_rect.collidepoint(mouse_pos)
            
            rect = menu_ui.draw_stone_button(
                self.window,
                text,
                button_font,
                button_x,
                y_pos,
                button_width,
                button_height,
                False,  # is_selected
                is_hovered
            )
            buttons.append((text, rect))

        pg.display.update()

        # Wait for button click
        while True:
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pg.mouse.get_pos()
                    for text, rect in buttons:
                        if rect.collidepoint(mouse_pos):
                            if text == "Play Again":
                                return "play_again"
                            elif text == "Return to Menu":
                                return "main_menu"
                            elif text == "Quit Game":
                                pg.quit()
                                exit(0)
                elif event.type == pg.QUIT:
                    pg.quit()
                    exit(0)
                elif event.type == pg.MOUSEMOTION:
                    # Redraw buttons to update hover effects
                    self.window.blit(background, (0, 0))
                    
                    # Redraw Game Over text
                    TextRenderer.render_text_with_outline(
                        "Game Over",
                        game_over_font,
                        (255, 0, 0),  # Red color for Game Over
                        self.window,
                        self.width // 2,
                        180,
                        word_config['outline_width']
                    )
                    
                    # Redraw stats with outline and shadow
                    for i, text in enumerate(stats_texts):
                        if word_config['has_outline']:
                            TextRenderer.render_text_with_outline(
                                text,
                                stats_font,
                                stats_color,
                                self.window,
                                self.width // 2,
                                250 + i * 50,
                                word_config['outline_width']
                            )
                        else:
                            stat_surface = stats_font.render(text, True, stats_color)
                            stat_rect = stat_surface.get_rect(center=(self.width // 2, 250 + i * 50))
                            self.window.blit(stat_surface, stat_rect)
                    
                    # Redraw buttons with updated hover states
                    mouse_pos = event.pos
                    for i, (text, _) in enumerate(buttons):
                        y_pos = button_positions[i]  # Use pre-calculated positions
                        button_rect = pg.Rect(button_x, y_pos, button_width, button_height)
                        is_hovered = button_rect.collidepoint(mouse_pos)
                        
                        rect = menu_ui.draw_stone_button(
                            self.window,
                            text,
                            button_font,
                            button_x,
                            y_pos,
                            button_width,
                            button_height,
                            False,
                            is_hovered
                        )
                        buttons[i] = (text, rect)
                    
                    pg.display.update()

    def draw_feedback(self, message, is_correct):
        # Create semi-transparent background
        feedback_surface = pg.Surface((self.width, 100))
        feedback_surface.set_alpha(180)  # Semi-transparent
        
        if is_correct:
            feedback_surface.fill(self.CORRECT_COLOR)
            self.debug_log("Drawing correct feedback message")
        else:
            feedback_surface.fill(self.INCORRECT_COLOR)
            self.debug_log("Drawing incorrect feedback message")

        # Draw the background
        self.window.blit(feedback_surface, (0, self.height // 4))

        # Draw the message with a white color for better contrast
        feedback_text = self.feedback_font.render(message, True, (255, 255, 255))
        text_rect = feedback_text.get_rect(center=(self.width // 2, self.height // 4 + 50))
        self.window.blit(feedback_text, text_rect)

        self.update_display()