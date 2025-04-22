import pygame
from game import Game
from utils.input.input_manager import InputManager
from utils.assets.asset_manager import AssetManager
from utils.assets.audio_manager import AudioManager
from utils.assets import asset_keys

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from assets import GameDataLink

TARGET_FPS: int = 60
WINDOW_WIDTH: int = 1280
WINDOW_HEIGHT: int = 720
WINDOW_HEADER: str = "Tomb of the Forgotten Words"
WINDOW_CLEAR_COLOR: tuple[int, int, int] = (255, 255, 255)


def create_window(header: str, width: int, height: int) -> pygame.Surface:
    """
    Creates a pygame window with the specified header, width, and height.

    Args:
        header (str): The title of the window.
        width (int): The width of the window.
        height (int): The height of the window.

    Returns:
        pygame.Surface: The created window surface.
    """
    pygame.display.set_caption(header)
    return pygame.display.set_mode((width, height))


def handle_events(input_manager: InputManager) -> int:
    """
    Handles pygame events and updates the input manager.

    Args:
        input_manager (InputManager): The input manager to update.

    Returns:
        int: 1 if the window was closed, 0 otherwise.
    """
    for event in pygame.event.get():
        match (event.type):
            case pygame.QUIT:
                return 1
            case pygame.KEYDOWN:
                input_manager.press_key(event.key)
            case pygame.KEYUP:
                input_manager.release_key(event.key)
            case pygame.MOUSEBUTTONDOWN:
                input_manager.press_mb(event.button)
            case pygame.MOUSEBUTTONUP:
                input_manager.release_mb(event.button)
            case pygame.MOUSEWHEEL:
                input_manager.scroll(event.y)
    return 0


def game_loop(
    game: Game, clock: pygame.time.Clock, window: pygame.Surface, input_manager: InputManager
) -> None:
    """
    Main game loop that handles updating and rendering the game.

    Args:
        game (Game): The game instance to update and render.
        clock (pygame.time.Clock): The clock to control the frame rate.
        window (pygame.Surface): The window surface to render to.
        input_manager (InputManager): The input manager for handling input.
    """
    running: bool = True

    while running:
        running = (
            handle_events(input_manager) != 1
        )  # check if user closed window and also handle other events

        # physics and movement
        game.update()  # update Game

        # If we called pygame.quit() inside game.update(), break out here
        if not pygame.get_init():
            break

        # rendering
        window.fill(WINDOW_CLEAR_COLOR)  # clear screen
        game.render(window)  # render Game

        pygame.display.flip()  # display rendered image on window

        clock.tick(TARGET_FPS)


def draw_loading_screen(window: pygame.Surface, font: pygame.font.Font, progress: float) -> None:
    """
    Draws the loading screen with a progress bar.

    Args:
        window (pygame.Surface): The window surface to render to.
        font (pygame.font.Font): The font to use for the loading text.
        progress (float): The loading progress (0.0 to 1.0).
    """
    window.fill((0, 0, 0))

    bar_width = WINDOW_WIDTH // 2  # outer bar dimensions
    bar_x = WINDOW_WIDTH // 2 - (bar_width // 2)
    bar_height = WINDOW_HEIGHT // 20
    bar_y = WINDOW_HEIGHT // 2

    loading_text = font.render(
        f"Loading... {int(progress*100)}%", True, (255, 255, 255)
    )  # centering the text
    text_size = loading_text.get_size()
    text_x = (WINDOW_WIDTH // 2) - (text_size[0] // 2)
    text_y = (WINDOW_HEIGHT // 2) - text_size[1]

    inner_x = bar_x + 5  # inner bar dimensions
    inner_y = bar_y + 5
    inner_height = bar_height - 10
    filled_width = int((bar_width - 10) * progress)

    window.blit(loading_text, (text_x, text_y))  # render
    pygame.draw.rect(window, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 3)
    pygame.draw.rect(window, (255, 255, 255), (inner_x, inner_y, filled_width, inner_height))

    pygame.display.flip()  # draw to screen


def show_splash_screen(window: pygame.Surface, assets: AssetManager) -> None:
    """
    Displays the splash screen before the loading screen using AssetManager.

    Args:
        window (pygame.Surface): The game window surface.
        assets (AssetManager): The asset manager to load the splash image.
    """
    splash_image = assets.get_image(asset_keys.SPRITE_SPLASH_SCREEN)  # Load splash image via AssetManager
    splash_image = pygame.transform.scale(splash_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    while True:
        window.fill((0, 0, 0))
        window.blit(splash_image, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    return


def start() -> None:
    """
    Initializes and starts the game.
    """
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("Calibri", 30)
    window = create_window(WINDOW_HEADER, WINDOW_WIDTH, WINDOW_HEIGHT)  # create window

    assets = AssetManager()  # load assets and update loading screen
    assets.load_music(lambda progress: draw_loading_screen(window, font, progress / 3))
    assets.load_sfx(lambda progress: draw_loading_screen(window, font, 1 / 3 + progress / 3))
    assets.load_images(lambda progress: draw_loading_screen(window, font, 2 / 3 + progress / 3))

    show_splash_screen(window, assets)  # Show splash screen

    audio_manager = AudioManager()  # initialize audio manager
    input_manager = InputManager()  # initialize Input manager
    game = Game(WINDOW_WIDTH, WINDOW_HEIGHT, font)  # initialize Main Game
    clock = pygame.time.Clock()

    game_loop(game, clock, window, input_manager)  # start the game loop

    data = GameDataLink.get_data()
    data["text"] = "TEST"
    data["neededPoints"] = 100
    data["earnedPoints"] = game.m_points
    data["rewardText"] = "jolinat - to cook; azhat - to give"
    GameDataLink.send_data(data)
    pygame.quit()


if __name__ == "__main__":
    start()
