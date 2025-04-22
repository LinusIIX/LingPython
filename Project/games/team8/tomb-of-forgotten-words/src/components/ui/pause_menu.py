import pygame, sys
from utils.assets.audio_manager import AudioManager
from components.ui.menu_button import MenuButton
from components.ui.slider import Slider


class PauseMenu:
    """
    Represents the pause menu in the game, managing the UI components like buttons and sliders.
    """

    def __init__(self, unpause_function: callable, font: pygame.font.Font):
        """
        Initializes a PauseMenu object.

        Args:
            unpause_function (callable): Function to call to unpause the game.
            font (pygame.font.Font): The font used for rendering text.
        """
        self.m_audio = AudioManager()
        self.m_active: bool = False
        self.m_font: pygame.font.Font = font

        self.m_buttons: list[MenuButton] = []
        self.m_buttons.append(
            MenuButton(
                pygame.Rect(640 - 150, 220, 300, 75),
                (0, 143, 129),
                (26, 217, 198),
                (102, 179, 171),
                unpause_function,
                (255, 255, 255),
                font,
                "Resume",
            )
        )
        self.m_buttons.append(
            MenuButton(
                pygame.Rect(640 - 150, 320, 300, 75),
                (0, 143, 129),
                (26, 217, 198),
                (102, 179, 171),
                self.quit,
                (255, 255, 255),
                font,
                "Quit",
            )
        )

        self.m_sliders: list[Slider] = []
        self.m_sliders.append(
            Slider(
                (640 - 150, 450),
                250,
                10,
                20,
                (0, 143, 129),
                (150, 150, 150),
                font,
                self.update_master_volume,
                start_value=self.m_audio.master_volume,
            )
        )
        self.m_sliders.append(
            Slider(
                (640 - 150, 510),
                250,
                10,
                20,
                (0, 143, 129),
                (150, 150, 150),
                font,
                self.update_music_volume,
                start_value=self.m_audio.music_volume,
            )
        )
        self.m_sliders.append(
            Slider(
                (640 - 150, 570),
                250,
                10,
                20,
                (0, 143, 129),
                (150, 150, 150),
                font,
                self.update_sfx_volume,
                start_value=self.m_audio.sfx_volume,
            )
        )

    def set_slider_start_values(self) -> None:
        """
        Sets the initial values for the sliders based on current audio settings.
        """
        self.m_sliders[0].set_value(self.m_audio.master_volume)
        self.m_sliders[1].set_value(self.m_audio.music_volume)
        self.m_sliders[2].set_value(self.m_audio.sfx_volume)

    def update_master_volume(self, vol: float):
        """
        Updates the master volume.

        Args:
            vol (float): The new master volume value.
        """
        if vol < 0.01:
            vol = 0
        self.m_audio.set_master_volume(vol)

    def update_sfx_volume(self, vol: float):
        """
        Updates the sound effects volume.

        Args:
            vol (float): The new sound effects volume value.
        """
        if vol < 0.01:
            vol = 0
        self.m_audio.set_sfx_volume(vol)

    def update_music_volume(self, vol: float):
        """
        Updates the music volume.

        Args:
            vol (float): The new music volume value.
        """
        if vol < 0.01:
            vol = 0
        self.m_audio.set_music_volume(vol)

    def quit(self) -> None:
        """
        Quits the game and exits the application.
        """
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    def click(self) -> None:
        """
        Handles click events for buttons and sliders.
        """
        for btn in self.m_buttons:
            btn.click()

        for slider in self.m_sliders:
            slider.click()

    def render(self, window: pygame.Surface) -> None:
        """
        Renders the pause menu on the given window surface.

        Args:
            window (pygame.Surface): The window surface to render on.
        """
        # darken the background
        bg_overlay = pygame.Surface(
            (window.get_width(), window.get_height()), pygame.SRCALPHA
        )  # create a surface to be able to render transparent rectangles... thanks pygame
        bg_overlay.fill((0, 0, 0, 155))
        window.blit(bg_overlay, (0, 0))

        # actual UI-Background
        background = pygame.Surface((500, 500), pygame.SRCALPHA)
        background.fill((0, 255, 229, 100))
        window.blit(
            background,
            (
                window.get_width() / 2 - background.get_width() / 2,
                window.get_height() / 2 - background.get_height() / 2,
            ),
        )

        # Header Text:
        paused_txt = self.m_font.render("PAUSED", True, (255, 255, 255))
        window.blit(
            paused_txt,
            (
                window.get_width() / 2 - paused_txt.get_width() / 2,
                window.get_height() / 2 - background.get_height() / 2 + 40,
            ),
        )

        for btn in self.m_buttons:
            btn.render(window)

        master_txt = self.m_font.render("Master Volume", True, (255, 255, 255))
        music_txt = self.m_font.render("Music Volume", True, (255, 255, 255))
        sfx_txt = self.m_font.render("Effects Volume", True, (255, 255, 255))

        window.blit(master_txt, (490, 410))
        window.blit(music_txt, (490, 470))
        window.blit(sfx_txt, (490, 530))

        for slider in self.m_sliders:
            slider.render(window)
