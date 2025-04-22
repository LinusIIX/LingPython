# LingoGuess.py
# Authors: Max Weber, Mojtaba Malek-Nejad, Philipp Gelfuss
# if you want to see more detailed information about the individual contributors of the code files, 
# please have a look at the "contributors.txt" file (in the "project" directory)

import pygame as pg
import random as rand
from game.game_ui import GameUI
from menu.menus import GameMenus
from ui.constants import *
from ui.text_renderer import TextRenderer
from utils.path_utils import PathUtils
from ui.font_manager import FontManager
from wordlists import WordLists

# Debug mode prints a lot of additional messages to the terminal.
DEBUG_MODE = False

# pg constants
WIDTH, HEIGHT = 1000, 600
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("LingoGuess\nA Hero's Quest")
pg.font.init()

# Initialize FontManager for button fonts only
font_manager = FontManager()

# Use default system font for regular text
FONT = pg.font.SysFont("sans_serif", HEIGHT // GAME_FONT_SIZE_FACTOR)
FPS = 60
CLOCK = pg.time.Clock()

# color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize path utils
path_utils = PathUtils()

# Initialize word lists
word_lists = WordLists(DEBUG_MODE)


def draw_text(text, font, color, surface, x, y):
    """Wrapper for text rendering to maintain compatibility"""
    TextRenderer.render_text(text, font, color, surface, x, y)


def draw_text_with_shadow(text, font, color, x, y):
    """Wrapper for shadow text rendering"""
    TextRenderer.render_text_with_shadow(text, font, color, WIN, x, y)


def draw_text_with_outline(text, font, color, x, y, outline_width=2):
    """Wrapper for outline text rendering"""
    TextRenderer.render_text_with_outline(text, font, color, WIN, x, y, outline_width)


class LingoGuess:
    def __init__(self, debug_mode=False):
        self.debug_mode = debug_mode
        self.debug_log("Initializing LingoGuess game")

        # Initialize path utils first
        self.path_utils = PathUtils()

        # Initialize FontManager after path utils
        self.font_manager = FontManager()

        # Initialize menu system with UI components
        self.menus = GameMenus(WIDTH, HEIGHT, WIN)

        # Current game states
        self.game_started = False
        self.show_game_started_text = False
        self.current_menu = "main"
        self.showing_game_over = False
        self.start_time = None

        # Initial gameplay variables
        self.strikes = 0
        self.max_strikes = 2
        self.timer = 61  # Start with 61 seconds (because of loading screen)
        self.times_up = False
        # self.time_added_per_correct_guess = 5  # Add 5 seconds per correct guess
        self.last_time_update = pg.time.get_ticks()
        self.correct_answers = 0
        self.incorrect_answers = 0

        # Initialize the UI
        self.ui = GameUI(WIDTH, HEIGHT, game_instance=self, debug_mode=debug_mode)
        self.debug_log("Game UI initialized")

        # Load game images
        self.background_image = pg.transform.scale(
            pg.image.load(self.path_utils.get_image_path("game_background.png")),
            (WIDTH, HEIGHT),
        )
        self.menu_background = pg.transform.scale(
            pg.image.load(self.path_utils.get_image_path("game_background.png")),
            (WIDTH, HEIGHT),
        )
        self.timer_background_image = pg.image.load(
            self.path_utils.get_image_path("timerbackground.jpg")
        )

        # Load and scale Ouroboros loading screen image to half size
        original_snake = pg.image.load(self.path_utils.get_image_path("snake.png"))
        snake_size = original_snake.get_size()
        self.snake_image = pg.transform.scale(
            original_snake, (snake_size[0] // 2, snake_size[1] // 2)
        )
        self.snake_angle = 0  # Track rotation angle
        self.debug_log("Game images loaded")

        # Initialize feedback system
        self.menus.ui.init_feedback(WIN)

        self.feedback_time = None
        self.show_feedback = False
        self.feedback_message = ""
        self.feedback_is_correct = False
        self.current_word = None
        self.showing_stats = False
        self.restrict_input_after_gameover = False  # New flag to restrict input

        self.score = 0
        self.debug_log("Game initialization completed")

        # Add stone texture colors for buttons
        self.STONE_COLORS = {
            "normal": (64, 64, 64),  # Dark gray
            "hover": (80, 80, 80),  # Lighter gray
            "selected": (90, 90, 90),  # Even lighter gray
            "border": (45, 45, 45),  # Darker gray for border
        }

    def debug_log(self, message):
        if self.debug_mode:
            print(f"[DEBUG][GAME] {message}")

    def check_language(self, input_text: str) -> bool:
        """Check if the input language matches the word's language."""

        self.debug_log(
            f"Checking language: input='{input_text}', word='{self.current_word[0]}'"
        )
        self.debug_log(f"Correct languages: {self.current_word[1]}")

        # Convert user input to lowercase and remove leading and trailing whitespace
        input_lower = input_text.lower().strip()

        # Compare user input with correct languages
        return input_lower in self.current_word[1]

    def create_stone_texture(self, width, height, base_color, noise_intensity=15):
        """Creates a stone-like texture by adding noise to a flat colour base."""

        # Create surface with base color
        texture = pg.Surface((width, height))
        texture.fill(base_color)

        # Add noise to individual color values for stone-like appearance
        for x in range(width):
            for y in range(height):
                noise = rand.randint(-noise_intensity, noise_intensity)
                color = list(base_color)
                for i in range(3):
                    # Clamp noise to valid RGB values
                    color[i] = max(0, min(255, color[i] + noise))
                texture.set_at((x, y), color)
        return texture

    def draw_stone_button(
        self, text, font, x, y, width, height, is_selected=False, is_hovered=False
    ):
        """Draws a stone button of the given size at the given location."""

        # Determine button color based on state
        if is_selected:
            base_color = self.STONE_COLORS["selected"]
        elif is_hovered:
            base_color = self.STONE_COLORS["hover"]
        else:
            base_color = self.STONE_COLORS["normal"]

        # Create stone texture
        button_surface = self.create_stone_texture(width, height, base_color)

        # Add rounded corners (simple version)
        corner_radius = 5
        pg.draw.rect(
            button_surface,
            base_color,
            (0, 0, width, height),
            border_radius=corner_radius,
        )

        # Draw border
        border_rect = pg.Rect(0, 0, width, height)
        pg.draw.rect(
            button_surface,
            self.STONE_COLORS["border"],
            border_rect,
            2,
            border_radius=corner_radius,
        )

        # Draw text with shadow
        text_surface = font.render(text, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(width // 2, height // 2))

        # Add shadow to text
        shadow_surface = font.render(text, True, (30, 30, 30))  # Dark gray shadow
        shadow_rect = text_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        button_surface.blit(shadow_surface, shadow_rect)
        button_surface.blit(text_surface, text_rect)

        # Create the final button rectangle and blit the surface
        button_rect = pg.Rect(x, y, width, height)
        WIN.blit(button_surface, button_rect)

        return button_rect

    def draw_menu_button(self, text, font, x, y, width=None, is_selected=False):
        """Draws a stone button of the given width at the given location."""

        text_surface = font.render(text, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect()
        padding = 20

        # If width is provided, use it; otherwise use text width plus padding
        button_width = width if width is not None else text_rect.width + padding * 2
        button_height = text_rect.height + padding

        # Get mouse position for hover effect
        mouse_pos = pg.mouse.get_pos()
        button_rect = pg.Rect(x, y - button_height // 2, button_width, button_height)
        is_hovered = button_rect.collidepoint(mouse_pos)

        # Draw stone button
        return self.draw_stone_button(
            text,
            font,
            x,
            y - button_height // 2,
            button_width,
            button_height,
            is_selected,
            is_hovered,
        )

    def draw_timer(self):
        """Draws the timer to the gameplay screen in timed mode."""

        if self.menus.get_selected_mode() != "Timed":
            return

        # Define the timer background dimensions
        timer_width = 200
        timer_height = 50
        timer_x = (WIDTH - timer_width) // 2  # Center horizontally
        timer_y = 20  # Position at the top

        # Scale the timer background image to the timer dimensions
        timer_background = pg.transform.scale(
            self.timer_background_image, (timer_width, timer_height)
        )

        # Create a surface for the timer background
        timer_surface = pg.Surface((timer_width, timer_height))
        timer_surface.fill((0, 0, 0))  # Black background

        # Draw the timer text
        timer_text = f"Time: {int(self.timer)}"
        timer_font = self.font_manager.get_button_font(HEIGHT)
        # timer_font = pg.font.SysFont('sans_serif', 36)

        text_surface = timer_font.render(
            timer_text, True, (255, 255, 255)
        )  # White text
        text_rect = text_surface.get_rect(center=(timer_width // 2, timer_height // 2))

        # Blit the text onto the timer background
        WIN.blit(timer_background, (timer_x, timer_y))

        # Blit the timer background onto the main window
        WIN.blit(text_surface, (timer_x + text_rect.x, timer_y + text_rect.y))

    def get_max_button_width(self, texts, font):
        """Return the maximum width of a list of button texts."""

        # Initialize variables
        max_width = 0
        padding = 20

        for text in texts:
            # Render each text to an object to get its width
            text_surface = font.render(text, True, BLACK)
            width = text_surface.get_rect().width + padding * 2

            # Update current max width if needed
            max_width = max(max_width, width)

        return max_width

    def draw_main_menu(self):
        """Draws the main menu to the game window."""

        # Draw background
        WIN.blit(self.menu_background, (0, 0))

        # Title with outline and shadow (using Anirb font)
        title_font = self.font_manager.get_title_font(HEIGHT)
        draw_text_with_outline(
            "LingoGuess - A Hero's Quest",
            title_font,
            (255, 255, 255),
            WIDTH // 2,
            HEIGHT // 6,
            outline_width=3,
        )

        # Menu buttons (using custom font)
        button_font = self.font_manager.get_button_font(HEIGHT)
        button_y_start = HEIGHT // 2 - 100
        button_spacing = 70
        button_x = 40

        # The contents of the main menu buttons
        button_texts = [
            "Start Game (Enter)",
            "Change Mode",
            "Change Difficulty",
            "About Us",
            "Quit Game",
        ]

        # All buttons in the main menu should have the same width
        button_width = self.get_max_button_width(button_texts, button_font)

        # Empty list for the buttons
        buttons = []

        # Create each menu button
        for i, text in enumerate(button_texts):
            rect = self.draw_menu_button(
                text,
                button_font,
                button_x,
                button_y_start + i * button_spacing,
                button_width,
            )

            # Add the new button to the list
            buttons.append((text, rect))

        return buttons

    def draw_mode_menu(self):
        """Draws the mode select menu to the game window."""

        # Draw background
        WIN.blit(self.menu_background, (0, 0))

        # Title with outline (using default font)
        title_font = pg.font.SysFont("sans_serif", HEIGHT // 8)
        draw_text_with_outline(
            "Select Mode",
            title_font,
            (255, 255, 255),
            WIDTH // 2,
            HEIGHT // 6,
            outline_width=3,
        )

        # Menu buttons (using custom font)
        button_font = self.font_manager.get_button_font(HEIGHT)
        button_y_start = HEIGHT // 2 - 100
        button_spacing = 70
        button_x = 40

        # Calculate widths for mode buttons and control buttons separately
        mode_button_width = self.get_max_button_width(self.modes, button_font)
        control_button_width = self.get_max_button_width(
            ["Apply and go back", "Cancel and go back"], button_font
        )

        # Empty list for the buttons
        buttons = []

        # Create each menu button
        for i, mode in enumerate(self.modes):
            rect = self.draw_menu_button(
                mode,
                button_font,
                button_x,
                button_y_start + i * button_spacing,
                mode_button_width,
                mode == self.temp_mode,
            )

            # Add the new button to the list
            buttons.append((mode, rect))

        # Control buttons
        y_offset = button_y_start + len(self.modes) * button_spacing + 20
        apply_rect = self.draw_menu_button(
            "Apply and go back", button_font, button_x, y_offset, control_button_width
        )
        cancel_rect = self.draw_menu_button(
            "Cancel and go back",
            button_font,
            button_x,
            y_offset + button_spacing,
            control_button_width,
        )

        # Add the control buttons to the list
        buttons.extend(
            [("Apply and go back", apply_rect), ("Cancel and go back", cancel_rect)]
        )

        return buttons

    def draw_difficulty_menu(self):
        """Draws the difficulty select menu to the game window."""

        # Draw background
        WIN.blit(self.menu_background, (0, 0))

        # Title (using default font)
        title_font = pg.font.SysFont("sans_serif", HEIGHT // 8)
        draw_text_with_outline(
            "Select Difficulty",
            title_font,
            (255, 255, 255),
            WIDTH // 2,
            HEIGHT // 6,
            outline_width=3,
        )

        # Menu buttons (using custom font)
        button_font = self.font_manager.get_button_font(HEIGHT)
        button_y_start = HEIGHT // 2 - 100
        button_spacing = 70
        button_x = 40

        # Calculate widths for difficulty buttons and control buttons separately
        diff_button_width = self.get_max_button_width(self.difficulties, button_font)
        control_button_width = self.get_max_button_width(
            ["Apply and go back", "Cancel and go back"], button_font
        )

        # Empty list for the buttons
        buttons = []

        # Create each menu button
        for i, diff in enumerate(self.difficulties):
            rect = self.draw_menu_button(
                diff,
                button_font,
                button_x,
                button_y_start + i * button_spacing,
                diff_button_width,
                diff == self.temp_difficulty,
            )

            # Add the new button to the list
            buttons.append((diff, rect))

        # Control buttons
        y_offset = button_y_start + len(self.difficulties) * button_spacing + 20
        apply_rect = self.draw_menu_button(
            "Apply and go back", button_font, button_x, y_offset, control_button_width
        )
        cancel_rect = self.draw_menu_button(
            "Cancel and go back",
            button_font,
            button_x,
            y_offset + button_spacing,
            control_button_width,
        )

        # Add the control buttons to the list
        buttons.extend(
            [("Apply and go back", apply_rect), ("Cancel and go back", cancel_rect)]
        )

        return buttons

    def draw_about_menu(self):
        """Draws the "About Us" menu to the game window."""

        # Draw background
        WIN.blit(self.menu_background, (0, 0))

        # Title with outline and shadow (using default font)
        title_font = pg.font.SysFont("sans_serif", HEIGHT // 8)
        draw_text_with_outline(
            "About Us",
            title_font,
            (255, 255, 255),
            WIDTH // 2,
            HEIGHT // 6,
            outline_width=3,
        )

        # About text with shadow (using default font)
        about_font = pg.font.SysFont("sans_serif", HEIGHT // 25)
        draw_text_with_shadow(
            "About us demo", about_font, (255, 255, 255), WIDTH // 2, HEIGHT // 2
        )

        # Back button (using custom font)
        button_font = self.font_manager.get_button_font(HEIGHT)
        button_x = 40
        button_width = self.get_max_button_width(["Back"], button_font)
        back_rect = self.draw_menu_button(
            "Back", button_font, button_x, HEIGHT * 3 // 4, button_width
        )

        return [("Back", back_rect)]

    def draw_control_button(self, font, x, y, text, color):
        """Draws control buttons (Stop Game, Exit Game) with stone texture style."""

        text_surface = font.render(text, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect()
        padding = 20

        # Create button dimensions
        button_width = text_rect.width + padding * 2
        button_height = text_rect.height + padding

        # Use stone button style for consistency
        return self.draw_stone_button(
            text,
            font,
            x - button_width // 2,
            y - button_height // 2,
            button_width,
            button_height,
        )

    def handle_menu_click(self, pos, buttons):
        """
        Handles button clicks outside of the gameplay screen.
        Returns False if the game should be stopped, True otherwise.
        """

        for text, rect in buttons:
            # Check every button if it was clicked
            if rect.collidepoint(pos):
                if self.current_menu == "main":
                    # Transition to different screens or start the game
                    if text == "Start Game (Enter)":
                        self.game_started = True
                        self.show_game_started_text = True
                        self.start_time = pg.time.get_ticks()
                    elif text == "Change Mode":
                        self.current_menu = "mode"
                        self.temp_mode = self.selected_mode
                    elif text == "Change Difficulty":
                        self.current_menu = "difficulty"
                        self.temp_difficulty = self.selected_difficulty
                    elif text == "About Us":
                        self.current_menu = "about"
                    elif text == "Quit Game":
                        # Signal that the game should close
                        return False

                elif self.current_menu == "mode":
                    # Change game mode and/or go back to the main menu
                    if text in self.modes:
                        self.temp_mode = text
                    elif text == "Apply and go back":
                        self.selected_mode = self.temp_mode
                        self.current_menu = "main"
                    elif text == "Cancel and go back":
                        self.current_menu = "main"

                elif self.current_menu == "difficulty":
                    # Change difficulty and/or go back to the main menu
                    if text in self.difficulties:
                        self.temp_difficulty = text
                    elif text == "Apply and go back":
                        self.selected_difficulty = self.temp_difficulty
                        self.current_menu = "main"
                    elif text == "Cancel and go back":
                        self.current_menu = "main"

                elif self.current_menu == "about":
                    # The About Us menu only has one options
                    if text == "Back":
                        self.current_menu = "main"

                # Return without checking the other buttons
                return True

        # Return if no button was clicked
        return True

    def handle_strikes_mode(self, input_text, events):
        """Handles the logic for the Strikes mode."""

        if self.check_language(input_text):
            # Player guessed the language correctly
            self.feedback_message = "Correct! Well done!"
            self.feedback_is_correct = True
            self.show_feedback = True
            self.feedback_time = pg.time.get_ticks()
            self.correct_answers += 1  # Increment correct answers
            self.debug_log("Correct answer! Waiting to show next word")
            self.current_word = word_lists.get_word()
            self.debug_log(f"New word displayed: {self.current_word[0]}")

        elif self.strikes >= self.max_strikes:
            # Player reached the strike limit and lost the game
            self.debug_log("Maximum strikes reached, game over")
            self.incorrect_answers += 1  # Increment incorrect answers

            # Show stats screen and wait for a button click to save as the response
            result = self.ui.show_stats_popup(
                self.correct_answers, self.incorrect_answers, self.start_time
            )

            # Start a new game or load the main menu
            if result == "play_again":
                self.start_new_game()
            elif result == "main_menu":
                self.game_started = False
                self.menus.state.switch_to_main()

        else:
            # Player guessed a wrong language
            self.feedback_message = "Try again!"
            self.feedback_is_correct = False
            self.show_feedback = True
            self.incorrect_answers += 1  # Increment incorrect answers
            self.feedback_time = pg.time.get_ticks()
            self.strikes += 1  # Increment strike counter

    def handle_timed_mode(self, input_text, events):
        """Handles the logic for the Timed mode."""

        if self.check_language(input_text):
            # Player guessed the language correctly
            self.feedback_message = "Correct! Well done!"
            self.feedback_is_correct = True
            self.show_feedback = True
            self.correct_answers += 1  # Increment correct answers
            self.feedback_time = pg.time.get_ticks()
            self.timer += 5  # Add time for correct guess
            self.current_word = word_lists.get_word()
            self.debug_log(f"New word displayed: {self.current_word[0]}")

        else:
            # Player guessed a wrong language
            self.feedback_message = "Try again!"
            self.feedback_is_correct = False
            self.show_feedback = True
            self.feedback_time = pg.time.get_ticks()
            self.incorrect_answers += 1  # Increment incorrect answers

    def update_timer(self, events):
        """Updates the timer displayed ingame."""

        current_time = pg.time.get_ticks()
        elapsed_time = (
            current_time - self.last_time_update
        ) / 1000  # Convert to seconds
        self.timer = max(
            0, self.timer - elapsed_time
        )  # Make sure the timer isn't negative
        self.last_time_update = current_time

        if self.timer <= 0 and not self.showing_stats:
            # Trigger a game over when the time ran out
            self.timer = 0
            self.ui.draw_feedback("Time's Up!", False)
            self.times_up = True
            pg.display.update()
            pg.time.wait(2000)
            self.showing_stats = (
                True  # Set the Flag before `show_stats_popup` gets called
            )

            # Show stats screen and wait for a button click to save as the response
            result = self.ui.show_stats_popup(
                self.correct_answers, self.incorrect_answers, self.timer
            )

            # Start a new game or load the main menu
            if result == "play_again":
                self.start_new_game()
            elif result == "main_menu":
                self.game_started = False
                self.menus.state.switch_to_main()

    def draw_game_buttons(self):
        """Draws the game control buttons in the gameplay screen."""

        button_font = self.font_manager.get_game_button_font(HEIGHT)
        mouse_pos = pg.mouse.get_pos()

        # Stop Game Button
        stop_button_rect = pg.Rect(
            WIDTH - 170, 20, GAME_BUTTON_WIDTH, GAME_BUTTON_HEIGHT
        )
        is_stop_hovered = stop_button_rect.collidepoint(mouse_pos)
        stop_button_rect = self.menus.ui.draw_stone_button(
            WIN,
            "Stop Game",
            button_font,
            WIDTH - 170,
            20,
            GAME_BUTTON_WIDTH,
            GAME_BUTTON_HEIGHT,
            False,  # is_selected
            is_stop_hovered,  # is_hovered
        )

        # Exit Game Button
        exit_button_rect = pg.Rect(
            WIDTH - 170, 75, GAME_BUTTON_WIDTH, GAME_BUTTON_HEIGHT
        )
        is_exit_hovered = exit_button_rect.collidepoint(mouse_pos)
        exit_button_rect = self.menus.ui.draw_stone_button(
            WIN,
            "Exit Game",
            button_font,
            WIDTH - 170,
            75,
            GAME_BUTTON_WIDTH,
            GAME_BUTTON_HEIGHT,
            False,  # is_selected
            is_exit_hovered,  # is_hovered
        )

        return stop_button_rect, exit_button_rect

    def start_new_game(self):
        """Resets internal variables to start a clean new game."""

        self.strikes = 0
        self.timer = 61
        self.times_up = False
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.current_word = word_lists.get_word()
        self.start_time = pg.time.get_ticks()
        self.last_time_update = self.start_time
        self.showing_stats = False  # Falls nötig
        self.show_game_started_text = False  # Falls nötig
        self.debug_log("New game started")

    def run_game(self):
        """Starts the game and its main loop."""

        self.debug_log("Game initialization started")
        pg.init()
        self.debug_log("Pygame initialized")

        run = True
        input_text = ""
        stop_button_rect = None
        exit_button_rect = None

        # Get initial word
        self.current_word = word_lists.get_word()
        self.debug_log("Initial game state set")

        while run:
            events = pg.event.get()
            # Handle pygame events
            for event in events:
                if event.type == pg.QUIT:
                    # Exit the game loop
                    self.debug_log("Game quit requested")
                    run = False

                if self.showing_stats:
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        self.showing_stats = False  # Reset flag
                        pg.display.update()
                        result = self.menus.handle_menu_click(event.pos, buttons)

                elif not self.game_started:
                    if (
                        event.type == pg.MOUSEBUTTONDOWN and event.button == 1
                    ):  # Left click
                        buttons = self.menus.draw_current_menu()
                        result = self.menus.handle_menu_click(event.pos, buttons)

                        if result == "start_game":
                            self.start_new_game()
                            self.game_started = True
                            self.show_game_started_text = True
                            self.start_time = pg.time.get_ticks()
                            self.last_time_update = (
                                pg.time.get_ticks()
                            )  # Reset the last time update

                        elif result == "quit_game":
                            # Exit the game loop
                            run = False

                    elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                        # Enter key was pressed to start the game
                        if self.menus.state.current_menu == "main":
                            self.game_started = True
                            self.show_game_started_text = True
                            self.start_time = pg.time.get_ticks()

                elif not self.show_game_started_text:  # Game is running normally
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        if stop_button_rect and stop_button_rect.collidepoint(
                            event.pos
                        ):
                            # Return to main menu
                            self.game_started = False
                            self.menus.state.switch_to_main()

                        elif exit_button_rect and exit_button_rect.collidepoint(
                            event.pos
                        ):
                            # Exit the game loop
                            run = False

                    elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            # Escape key pressed, exit game loop
                            self.debug_log("Game terminated by escape key")
                            run = False

                        elif event.key == pg.K_BACKSPACE:
                            # Backspace pressed, remove one letter from the input
                            input_text = input_text[:-1]

                        elif event.key == pg.K_RETURN and input_text.strip():
                            # Evaluate the player input if it isn't empty
                            if self.menus.get_selected_mode() == "Strikes":
                                # Strike game mode
                                self.handle_strikes_mode(input_text, events)

                            elif self.menus.get_selected_mode() == "Timed":
                                # Timed game mode
                                self.handle_timed_mode(input_text, events)

                            else:
                                # Endless game mode
                                if self.check_language(input_text):
                                    # Player guessed correctly
                                    self.feedback_message = "Correct! Well done!"
                                    self.feedback_is_correct = True
                                    self.show_feedback = True
                                    self.feedback_time = pg.time.get_ticks()
                                    self.current_word = word_lists.get_word()

                                else:
                                    # Player guessed a wrong language
                                    self.feedback_message = "Try again!"
                                    self.feedback_is_correct = False
                                    self.show_feedback = True
                                    self.feedback_time = pg.time.get_ticks()

                            # Reset the input text after evaluation
                            input_text = ""

                        else:
                            # Add the pressed key to the input if it's below the maximum length
                            if len(input_text) < 15:
                                input_text += event.unicode

            # Draw the current menu if the game isn't running
            if not self.game_started:
                if self.current_menu == "main":
                    self.draw_main_menu()

                elif self.current_menu == "mode":
                    self.draw_mode_menu()

                elif self.current_menu == "difficulty":
                    self.draw_difficulty_menu()

                elif self.current_menu == "about":
                    self.draw_about_menu()

                buttons = self.menus.draw_current_menu()

            # Show the loading screen and start the game
            elif self.show_game_started_text:
                WIN.fill(BLACK)

                # Get the center of the screen, move snake up by 50 pixels
                center_x = WIDTH // 2
                center_y = HEIGHT // 2 - 50  # Move snake up

                # Rotate the Ouroboros loading screen image
                self.snake_angle = (
                    self.snake_angle - 2
                ) % 360  # Rotate counterclockwise
                rotated_snake = pg.transform.rotate(self.snake_image, self.snake_angle)

                # Get the rect of the rotated image and center it
                snake_rect = rotated_snake.get_rect(center=(center_x, center_y))

                # Draw the rotated snake
                WIN.blit(rotated_snake, snake_rect)

                # Draw "Loading Game" text below snake using Fondamento font
                loading_font = self.font_manager.get_loading_font(HEIGHT)
                draw_text(
                    "Loading Game",
                    loading_font,
                    WHITE,
                    WIN,
                    WIDTH // 2,
                    HEIGHT // 2 + 200,
                )

                # For the duration of the loading screen
                if pg.time.get_ticks() - self.start_time > GAME_START_DURATION:
                    self.show_game_started_text = False
                    self.timer = 61  # Reset timer
                    self.last_time_update = pg.time.get_ticks()

            elif self.game_started:
                # Draw game screen
                WIN.blit(self.background_image, (0, 0))

                # Use configured game word font
                word_font_config = self.font_manager.get_game_word_font(HEIGHT)
                TextRenderer.render_game_word(
                    self.current_word[0], word_font_config, WIN, WIDTH // 2, HEIGHT // 2
                )

                # Draw feedback if needed
                if self.show_feedback:
                    self.menus.ui.feedback.show(
                        self.feedback_message, self.feedback_is_correct
                    )
                    self.menus.ui.feedback.draw()

                    if (
                        not self.menus.ui.feedback.update()
                        or pg.time.get_ticks() - self.feedback_time > 2000
                    ):
                        self.show_feedback = False

                # Draw input box with default font
                input_rect = pg.Rect(WIDTH // 2 - 200, HEIGHT // 2 + 75, 400, 50)
                pg.draw.rect(WIN, WHITE, input_rect)
                pg.draw.rect(WIN, BLACK, input_rect, 2)
                draw_text(input_text, FONT, BLACK, WIN, WIDTH // 2, HEIGHT // 2 + 100)

                stop_button_rect, exit_button_rect = self.draw_game_buttons()

                if self.menus.get_selected_mode() == "Timed" and (not self.times_up):
                    self.update_timer(events)
                    self.draw_timer()

                elif self.times_up:
                    result = self.ui.show_stats_popup(
                        self.correct_answers, self.incorrect_answers, self.start_time
                    )

                    if result == "play_again":
                        self.start_new_game()
                        self.times_up = False

                    elif result == "main_menu":
                        self.game_started = False
                        self.times_up = False
                        self.menus.state.switch_to_main()
                    # Quit Game is handled directly in the `show_stats_popup` method

            # Trigger game over for Strike mode
            elif self.game_started and self.strikes > self.max_strikes:
                self.showing_game_over = True
                # self.ui.draw_feedback("Game Over!", False)
                pg.display.update()
                pg.time.wait(500)
                self.showing_stats = True  # Set flag to show stats
                self.ui.show_stats_popup(events)  # Call stats pop-up

            # Update the game window
            pg.display.update()
            CLOCK.tick(FPS)

        self.debug_log("Game terminated")
        pg.quit()


# Start the game if this file is being interpreted directly (not through an import)
if __name__ == "__main__":
    game = LingoGuess(DEBUG_MODE)
    game.run_game()
