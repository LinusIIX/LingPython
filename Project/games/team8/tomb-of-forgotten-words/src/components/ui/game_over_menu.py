import pygame, sys
from components.ui.menu_button import MenuButton

class GameOverMenu:

    def __init__(self, restart_function: callable, font: pygame.font.Font):
        """
        Initializes a GameOverMenu object

        Args:
            restart_function (callable): Function to call to restart the game.
            font (pygame.font.Font): The font used for rendering text.
        """
        self.m_font = font
        self.m_buttons: list[MenuButton] = [
            MenuButton(
                pygame.Rect(640 - 150, 370, 300, 75),
                (181, 9, 0),
                (219, 15, 4),
                (122, 7, 1),
                restart_function,
                (255, 255, 255),
                font,
                "Restart",
            ),

            MenuButton(
                pygame.Rect(640 - 150, 470, 300, 75),
                (181, 9, 0),
                (219, 15, 4),
                (122, 7, 1),
                self.quit,
                (255, 255, 255),
                font,
                "Quit"
            )
        ]


    def click(self) -> None:
        for btn in self.m_buttons:
            btn.click()

    def quit(self) -> None:
        """
        Quits the game and exits the application.
        """
        pygame.display.quit()
        pygame.quit()

    
    def render(self, window: pygame.Surface, game_won: bool) -> None:
        """
        Renders the game over menu on the given window surface.

        Args:
            window (pygame.Surface): The window surface to render on.
            game_won (bool): Whether the game was won or lost
        """
        # darken the background
        bg_overlay = pygame.Surface(
            (window.get_width(), window.get_height()), pygame.SRCALPHA
        )
        bg_overlay.fill((0, 0, 0, 155))
        window.blit(bg_overlay, (0, 0))

        if game_won:
            text = "YOU WON!"
            bg_color = (13, 196, 4, 100)
            for btn in self.m_buttons:
                btn.set_color(
                (9, 181, 0),
                (15, 219, 4),
                (7, 122, 1)
                )
        else:
            text = "GAME OVER"
            bg_color = (196, 13, 4, 100)
            for btn in self.m_buttons:
                btn.set_color(
                    (181, 9, 0),
                    (219, 15, 4),
                    (122, 7, 1)
                )

        background = pygame.Surface((500, 400), pygame.SRCALPHA)
        background.fill(bg_color)
        window.blit(
            background,
            (
                window.get_width() / 2 - background.get_width() / 2,
                window.get_height() / 2 - background.get_height() / 2,
            ),
        )

        game_end_text = self.m_font.render(text, True, (255, 255, 255))
        end_text_pos = (
            window.get_width() // 2 - game_end_text.get_width() // 2,
            window.get_height() // 2 - background.get_height() // 2 + 40
        )
        window.blit(game_end_text, end_text_pos)

        if game_won:
            reward_text = self.m_font.render("jolinat - to cook; azhat - to give", True, (255, 255, 255))
            reward_text_pos = (
                window.get_width() // 2 - reward_text.get_width() // 2,
                end_text_pos[1] + game_end_text.get_height() + 40
            )
            window.blit(reward_text, reward_text_pos)

        for btn in self.m_buttons:
            btn.render(window)
