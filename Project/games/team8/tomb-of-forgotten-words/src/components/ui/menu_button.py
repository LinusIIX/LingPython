import pygame
from utils.input.input_manager import InputManager


class MenuButton:
    """
    Represents a menu button in the game with hover and click effects.
    """

    def __init__(
        self,
        bounds: pygame.Rect,
        color: tuple[int, int, int],
        hover_color: tuple[int, int, int],
        click_color: tuple[int, int, int],
        function: callable,
        text_color: tuple[int, int, int],
        font: pygame.font.Font,
        text: str = "",
    ):
        """
        Initializes a MenuButton object.

        Args:
            bounds (pygame.Rect): The rectangular bounds of the button.
            color (tuple[int, int, int]): The default color of the button.
            hover_color (tuple[int, int, int]): The color of the button when hovered over.
            click_color (tuple[int, int, int]): The color of the button when clicked.
            function (callable): The function to call when the button is clicked.
            text_color (tuple[int, int, int]): The color of the button text.
            font (pygame.font.Font): The font used for the button text.
            text (str, optional): The text displayed on the button. Defaults to "".
        """
        self.m_bounds: pygame.Rect = bounds
        self.m_color: tuple[int, int, int] = color
        self.m_hover: tuple[int, int, int] = hover_color
        self.m_clicked: tuple[int, int, int] = click_color
        self.m_func: callable = function
        self.m_font: pygame.font.Font = font
        self.m_text_col: tuple[int, int, int] = text_color
        self.m_text: str = text
        self.m_input = InputManager()

    def click(self) -> None:
        """
        Checks if the button is clicked and calls the assigned function if it is.
        """
        mouse_pos = self.m_input.get_mouse_screen_pos()
        if self.m_bounds.collidepoint(mouse_pos[0], mouse_pos[1]):
            self.m_func()

    def set_color(self, color: tuple[int, int, int], hover_color: tuple[int, int, int],
                  click_color: tuple[int, int, int]) -> None:
        """
        Updates button colors.
        Args:
            color: Normal button color.
            hover_color: Color when button is hovered over.
            click_color: Color when button is clicked.
        """
        self.m_color = color
        self.m_hover = hover_color
        self.m_clicked = click_color

    def render(self, window: pygame.Surface) -> None:
        """
        Renders the button on the given window surface.

        Args:
            window (pygame.Surface): The window surface to render on.
        """
        color = self.m_color
        mouse_pos = self.m_input.get_mouse_screen_pos()
        if self.m_bounds.collidepoint(mouse_pos[0], mouse_pos[1]):
            if self.m_input.is_button_pressed(pygame.BUTTON_LEFT):
                color = self.m_clicked
            else:
                color = self.m_hover

        pygame.draw.rect(window, color, self.m_bounds)
        pygame.draw.rect(window, (255, 255, 255), self.m_bounds, width=2)
        text = self.m_font.render(self.m_text, True, self.m_text_col)
        window.blit(
            text,
            (
                self.m_bounds.centerx - text.get_width() / 2,
                self.m_bounds.centery - text.get_height() / 2,
            ),
        )
