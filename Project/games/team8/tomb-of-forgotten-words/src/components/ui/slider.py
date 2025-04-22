import pygame
from utils.input.input_manager import InputManager


class Slider:
    """
    Represents a slider UI component in the game.

    Attributes:
        m_value (float): The current value of the slider (0.0 to 1.0).
        m_length (int): The length of the slider.
        m_pos (int): The current position of the slider thumb.
        m_background (pygame.Rect): The background rectangle of the slider.
        m_filling (pygame.Rect): The filling rectangle of the slider.
        m_bg_col (tuple[int, int, int]): The background color of the slider.
        m_color (tuple[int, int, int]): The fill color of the slider.
        m_font (pygame.font.Font): The font used for rendering text.
        m_input (InputManager): The input manager to handle mouse input.
        m_drag_btn (pygame.Rect): The draggable button rectangle of the slider.
        m_dragging (bool): Indicates if the slider is currently being dragged.
        m_update_callback (callable): The callback function to call when the slider value changes.
    """

    @property
    def value(self):
        """
        Gets the current value of the slider.

        Returns:
            float: The current value of the slider.
        """
        return self.m_value

    def __init__(
        self,
        position: tuple[int, int],
        length: int,
        width: int,
        btn_size: int,
        fill_color: tuple[int, int, int],
        bg_color: tuple[int, int, int],
        font: pygame.font.Font,
        update_callback: callable,
        start_value: float = 1,
    ):
        """
        Initializes a Slider object.

        Args:
            position (tuple[int, int]): The position of the slider.
            length (int): The length of the slider.
            width (int): The width of the slider.
            btn_size (int): The size of the draggable button.
            fill_color (tuple[int, int, int]): The fill color of the slider.
            bg_color (tuple[int, int, int]): The background color of the slider.
            font (pygame.font.Font): The font used for rendering text.
            update_callback (callable): The callback function to call when the slider value changes.
            start_value (float, optional): The initial value of the slider. Defaults to 1.
        """
        self.m_value = min(max(0.0, start_value), 1.0)
        self.m_length = length
        self.m_pos = int(start_value * length)
        self.m_background = pygame.Rect(position[0], position[1], length, width)
        self.m_filling = pygame.Rect(position[0], position[1], self.m_pos, width)
        self.m_bg_col = bg_color
        self.m_color = fill_color
        self.m_font = font

        self.m_input = InputManager()
        self.m_drag_btn = pygame.Rect(position[0], position[1], btn_size, btn_size)
        self.m_drag_btn.centerx = self.m_filling.right
        self.m_drag_btn.centery = self.m_filling.centery
        self.m_dragging: bool = False
        self.m_update_callback = update_callback

    def click(self) -> None:
        """
        Handles click events for the slider.
        """
        mouse_pos = self.m_input.get_mouse_screen_pos()
        if self.m_drag_btn.collidepoint(mouse_pos[0], mouse_pos[1]):
            self.m_dragging = True

    def update(self) -> None:
        """
        Updates the slider's position and value based on mouse input.
        """
        mouse_pos = self.m_input.get_mouse_screen_pos()
        mouse_pressed = self.m_input.is_button_pressed(pygame.BUTTON_LEFT)
        current_val = self.m_value
        if not mouse_pressed:
            self.m_dragging = False
            return
        m_x = mouse_pos[0] - self.m_background.left
        self.m_pos = min(max(0, m_x), self.m_length)
        self.m_value = self.m_pos / self.m_length
        self.m_filling.width = self.m_pos
        self.m_drag_btn.centerx = self.m_filling.right
        if self.m_value != current_val:
            self.m_update_callback(self.m_value)

    def set_value(self, value: float) -> None:
        """
        Sets the value of the slider.

        Args:
            value (float): The new value of the slider (0.0 to 1.0).
        """
        self.m_value = min(max(0.0, value), 1.0)
        self.m_pos = int(value * self.m_length)
        self.m_filling.width = self.m_pos
        self.m_drag_btn.centerx = self.m_filling.right

    def render(self, window: pygame.Surface) -> None:
        """
        Renders the slider on the given window surface.

        Args:
            window (pygame.Surface): The window surface to render on.
        """
        mouse_pos = self.m_input.get_mouse_screen_pos()
        mouse_pressed = self.m_input.is_button_pressed(pygame.BUTTON_LEFT)
        if self.m_dragging:
            self.update()
        pygame.draw.rect(window, self.m_bg_col, self.m_background)  # draw the bar
        pygame.draw.rect(window, self.m_color, self.m_filling)
        pygame.draw.rect(window, (255, 255, 255), self.m_background, width=2)

        color = self.m_color
        if self.m_drag_btn.collidepoint(mouse_pos[0], mouse_pos[1]):
            if mouse_pressed:
                color = (102, 179, 171)  # TODO: replace with parameters
            else:
                color = (26, 217, 198)
        pygame.draw.rect(window, color, self.m_drag_btn)
        pygame.draw.rect(window, (255, 255, 255), self.m_drag_btn, width=2)

        valtext = self.m_font.render(f" {int(self.m_value * 100)}%", True, (255, 255, 255))
        window.blit(
            valtext, (self.m_background.right, self.m_background.centery - valtext.get_height() / 2)
        )
