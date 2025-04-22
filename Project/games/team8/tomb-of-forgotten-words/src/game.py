import pygame, math
import utils.assets.asset_keys as assets
from utils.input.input_manager import InputManager
from utils.assets.audio_manager import AudioManager
from utils.input.keymap import *
from components.ui.pause_menu import PauseMenu
from components.ui.game_over_menu import GameOverMenu
from components.ui.hud import HUD
from components.stage import Stage


class Game:
    """
    Main game class that handles the game loop, input, rendering, and state management.

    Attributes:
        STAGE_WIDTH (int): The width of the game stage.
        STAGE_HEIGHT (int): The height of the game stage.
        m_input (InputManager): The input manager for handling keyboard and mouse input.
        m_audio (AudioManager): The audio manager for handling sound and music.
        m_font (pygame.font.Font): The font used for UI elements.
        m_hud (HUD): The HUD (Heads-Up Display) for the game.
        m_paused (bool): Indicates whether the game is paused.
        m_pause_menu (PauseMenu): The pause menu UI.
        m_points (int): The player's score.
        m_stage (Stage): The game stage.
        m_camera (pygame.Rect): The camera viewport.
        m_left_click_func (callable): The function to call on left mouse button click.
        m_gun (Gun): The player's gun. (Assuming there's a Gun class)
        m_player (Player): The player object. (Assuming there's a Player class)
        m_bullets (list[Bullet]): The list of bullets fired by the player. (Assuming there's a Bullet class)
    """

    STAGE_WIDTH: int = 2560 * 2
    STAGE_HEIGHT: int = 2560 * 2

    def __init__(self, width: int, height: int, ui_font: pygame.font.Font):
        """
        Initializes the Game object.

        Args:
            width (int): The width of the game window.
            height (int): The height of the game window.
            ui_font (pygame.font.Font): The font used for UI elements.
        """
        self.m_input = InputManager()
        self.m_audio = AudioManager()
        self.m_font = ui_font

        self.m_audio.start_track(assets.TRACK_TOMB)
        self.m_audio.set_music_volume(0.6)

        self.m_hud = HUD()

        self.m_game_over_menu = GameOverMenu(self.restart_game, ui_font)

        self.m_input.assign_function_to_key(KEY_PAUSE, self.toggle_pause)
        self.m_paused = False
        self.m_pause_menu = PauseMenu(self.toggle_pause, self.m_font)

        self.m_points = 0

        self.m_stage = Stage(self.STAGE_WIDTH, self.STAGE_HEIGHT)
        self.m_camera = pygame.Rect(0, 0, width, height)
        self.m_input.set_camera(self.m_camera)

        self.m_left_click_func = (
            self.m_pause_menu.click
        )  # store button function to switch back to when toggling between menu and gameplay


    def restart_game(self) -> None:
        """
        Restarts the game by re-initializing the stage and resetting variables.
        """
        self.m_stage = Stage(self.STAGE_WIDTH, self.STAGE_HEIGHT)
        self.m_points = 0
        self.m_stage.enemy_spawner.reset()

        self.m_input.assign_function_to_key(KEY_PAUSE, self.toggle_pause)   # set the pause menu input as it'll be deactivated during the game-over screen
        self.m_hud.update_grenade_recharge(1)
        self.m_hud.update_inventory_selection(0)


    def toggle_pause(self) -> None:
        """
        Toggles the paused state of the game.
        """
        self.m_paused = not self.m_paused
        if self.m_paused:
            self.m_pause_menu.set_slider_start_values()
            self.m_left_click_func = self.m_input.get_button_function(
                pygame.BUTTON_LEFT
            )  # save what function was called before
            self.m_input.assign_function_to_mouse_button(
                pygame.BUTTON_LEFT, self.m_pause_menu.click
            )
        else:
            self.m_input.assign_function_to_mouse_button(pygame.BUTTON_LEFT, self.m_left_click_func)

    def update(self) -> None:
        """
        Updates the game state.
        """
        self.m_audio.update()
        if self.m_stage.game_over:
            self.m_input.assign_function_to_mouse_button(pygame.BUTTON_LEFT, self.m_game_over_menu.click)
            if self.m_stage.game_won:
                self.m_points = 100
            return
        if self.m_paused or self.m_stage.game_over:     # stop updating if the game is paused or game over has been reached
            return

        self.m_stage.update()

        self.m_camera.center = self.m_stage.player_center
        # TODO: smooth out camera movement (give player a bit of space before the camera snaps onto their movement)
        self.m_camera.x = max(
            0, min(self.m_camera.x, self.m_stage.width - self.m_camera.width)
        )  # prevent camera from moving off screen
        self.m_camera.y = max(0, min(self.m_camera.y, self.m_stage.height - self.m_camera.height))

        self.m_points = int(
            (self.m_stage.enemy_spawner.wave_index - 1) / float(self.m_stage.enemy_spawner.num_waves) * 100.0
        )

    def render(self, window: pygame.Surface) -> None:
        """
        Renders the game state to the window.

        Args:
            window (pygame.Surface): The window surface to render to.
        """
        window.blit(self.m_stage.render(self.m_camera), (-self.m_camera.x, -self.m_camera.y))

        self.m_hud.render(window)

        if self.m_stage.game_over:
            self.m_game_over_menu.render(window, self.m_stage.game_won)
            pass
        elif self.m_paused:
            self.m_pause_menu.render(window)

    def shoot_bullet(self) -> None:
        """
        Handles the shooting of a bullet by the player.
        """
        if self.m_gun.delay_active:  # disable shooting while the gun delay is still active
            return
        diagonals = self.m_player.get_diagonal_speeds()
        self.m_player.recoil(
            diagonals, -self.m_gun.recoil
        )  # negative recoil to invert the direction of the recoil
        self.m_audio.play_sfx(assets.SFX_SHOT)
        self.m_bullets.append(self.m_gun.shoot(diagonals))

        # self.m_points += 1 # TODO: this is for testing - points should get added when an enemy dies
